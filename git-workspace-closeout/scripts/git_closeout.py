#!/usr/bin/env python3
"""Policy-gated local snapshots and explicit single-branch pushes. Python 3.10+."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import urlsplit

SCHEMA = 1
MODES = ("off", "ask", "auto")
SECRET = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{35}")
SENSITIVE = re.compile(r"^(?:\.env(?:\..*)?|\.envrc|\.netrc|\.git-credentials|credentials\.json|secrets\.json|id_rsa|id_dsa|id_ecdsa|id_ed25519|.*service-account.*\.json|.*\.(?:pem|key|p12|pfx|jks|keystore|kdbx))$", re.I)
SAFE_ENV = {".env.example", ".env.template", ".env.sample"}
MAX_BLOB = 64 * 1024 * 1024
MAX_HISTORY_COMMITS = 200
MAX_HISTORY_BLOBS = 10000
ROUTING_BLOCK = """<!-- git-workspace-closeout:begin -->
## Git closeout routing

At session start, use $git-workspace-closeout to read this repository's saved
local/remote preferences and pending session state. Current user instructions
override saved choices; persist an explicitly requested preference change first.
After persistent work, keep a pending task record, consider a checkpoint at a
verified phase boundary, and check Git closeout before the final response or
handoff. Respect off/ask/auto independently for local commits and remote pushes;
never treat local automation or Full access as publication authorization.
Audit/plan are read-only. Mutations use the skill's policy-gated entrypoint;
report a disabled, waiting, blocked or unverified outcome instead of claiming
completion. No background hooks, watchers or permission changes are installed.
<!-- git-workspace-closeout:end -->
"""


class Blocked(Exception):
    def __init__(self, reason, code=70, **details):
        super().__init__(reason)
        self.reason, self.code, self.details = reason, code, details


def emit(**values):
    print(json.dumps(values, ensure_ascii=True, sort_keys=True), flush=True)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def classify(stderr, default="git_failed"):
    message = stderr.decode(errors="replace").lower()
    if "index.lock" in message and ("file exists" in message or "already exists" in message):
        return Blocked("existing_index_lock", 73)
    if any(s in message for s in ("permission denied", "operation not permitted", "read-only file system")):
        return Blocked("permission_boundary", 77, action="use_allowed_command_permission_or_report_boundary")
    return Blocked(default)


class Repo:
    def __init__(self):
        # Ignore inherited alternate indexes/worktrees: the physical cwd owns the scope.
        self.env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
        for key in list(self.env):
            if key in {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_COUNT"} or re.match(r"GIT_CONFIG_(KEY|VALUE)_\d+$", key):
                del self.env[key]
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], env=self.env, capture_output=True)
        if result.returncode:
            raise Blocked("not_a_git_worktree", 69)
        self.root = Path(os.fsdecode(result.stdout).rstrip("\n")).resolve()
        self.gitdir = Path(self.text("rev-parse", "--absolute-git-dir")).resolve()
        self.store = self.gitdir / "codex-closeout"
        self.policy_path = self.store / "policy.json"
        self.session_path = self.store / "session.json"

    def run(self, *args, check=True, timeout=30):
        try:
            result = subprocess.run(["git", *args], cwd=self.root, env=self.env, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise Blocked("command_timeout_result_unverified", 75)
        if check and result.returncode:
            raise classify(result.stderr)
        return result

    def text(self, *args, **kwargs):
        return os.fsdecode(self.run(*args, **kwargs).stdout).strip()

    def read(self, path):
        if self.store.is_symlink() or path.is_symlink():
            raise Blocked("private_state_symlink", 73)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            raise Blocked("invalid_private_state", 78)

    def save(self, path, value):
        if self.store.is_symlink() or path.is_symlink():
            raise Blocked("private_state_symlink", 73)
        self.store.mkdir(mode=0o700, exist_ok=True)
        temp = self.store / (path.name + ".tmp-" + str(os.getpid()))
        try:
            with temp.open("x", encoding="utf-8") as stream:
                json.dump(value, stream, sort_keys=True, ensure_ascii=True, indent=2)
                stream.write("\n")
            temp.chmod(0o600)
            os.replace(temp, path)
        finally:
            if temp.exists():
                temp.unlink()

    @contextlib.contextmanager
    def lock(self):
        if self.store.is_symlink():
            raise Blocked("private_state_symlink", 73)
        self.store.mkdir(mode=0o700, exist_ok=True)
        path = self.store / "operation.lock"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise Blocked("closeout_operation_in_progress", 73)
        try:
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            yield
        finally:
            # Only remove the lock this process itself created; never touch index.lock.
            path.unlink(missing_ok=True)

    def policy(self):
        policy = self.read(self.policy_path)
        if policy is None:
            return None
        if not isinstance(policy, dict):
            raise Blocked("invalid_policy", 78)
        if policy.get("schema") != SCHEMA or policy.get("root") != str(self.root) or policy.get("gitdir") != str(self.gitdir):
            raise Blocked("policy_repository_mismatch", 78)
        if policy.get("local") not in MODES or policy.get("remote") not in MODES:
            raise Blocked("invalid_policy", 78)
        if not isinstance(policy.get("branches"), list) or not policy["branches"] or not all(isinstance(b, str) for b in policy["branches"]):
            raise Blocked("invalid_policy", 78)
        return policy

    def head(self):
        result = self.run("rev-parse", "--verify", "HEAD", check=False)
        return result.stdout.decode().strip() if result.returncode == 0 else None

    def branch(self):
        return self.text("symbolic-ref", "--quiet", "--short", "HEAD", check=False) or None

    def preflight(self):
        if not self.branch():
            raise Blocked("detached_head", 78)
        if self.run("ls-files", "-u").stdout:
            raise Blocked("unmerged_paths", 78)
        for name in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply", "sequencer", "index.lock"):
            if (self.gitdir / name).exists():
                raise Blocked("existing_index_lock" if name == "index.lock" else "git_operation_in_progress", 73, operation=name)

    def paths(self, *args):
        return [os.fsdecode(p) for p in self.run(*args).stdout.split(b"\0") if p]

    def audit(self):
        staged = set(self.paths("diff", "--cached", "--name-only", "-z"))
        unstaged = set(self.paths("diff", "--name-only", "-z"))
        untracked = set(self.paths("ls-files", "--others", "--exclude-standard", "-z"))
        raw_status = self.run("status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
        return {"staged": sorted(staged), "unstaged": sorted(unstaged), "untracked": sorted(untracked), "paths": sorted(staged | unstaged | untracked), "clean": not raw_status}

    def validate_blob(self, path, data):
        base = Path(path).name.lower()
        if SENSITIVE.fullmatch(base) and base not in SAFE_ENV:
            raise Blocked("credential_filename", 3, path=path)
        if len(data) > MAX_BLOB:
            raise Blocked("blob_requires_manual_review", 3, path=path)
        if SECRET.search(data):
            raise Blocked("credential_pattern", 3, path=path)

    def local_plan(self):
        self.preflight()
        audit = self.audit()
        if set(audit["staged"]) & set(audit["unstaged"]):
            raise Blocked("partial_staging_requires_separate_decision", 78)
        files = {}
        for path in audit["paths"]:
            physical = self.root / path
            base = Path(path).name.lower()
            if SENSITIVE.fullmatch(base) and base not in SAFE_ENV:
                raise Blocked("credential_filename", 3, path=path)
            if physical.is_symlink():
                target = os.readlink(physical)
                if Path(target).is_absolute() or not (physical.parent / target).resolve().is_relative_to(self.root):
                    raise Blocked("external_symlink_requires_review", 3, path=path)
                files[path] = "symlink:" + target
            elif physical.is_file():
                if physical.stat().st_size > MAX_BLOB:
                    raise Blocked("blob_requires_manual_review", 3, path=path)
                data = physical.read_bytes()
                self.validate_blob(path, data)
                files[path] = hashlib.sha256(data).hexdigest()
            elif physical.exists():
                raise Blocked("nested_repository_or_nonregular_path", 78, path=path)
            else:
                files[path] = "deleted"
        # Also scan staged blobs; content may differ from the worktree.
        for path in audit["staged"]:
            blob = self.run("show", ":" + path, check=False)
            if blob.returncode == 0:
                self.validate_blob(path, blob.stdout)
        policy = self.policy()
        details = {"root": str(self.root), "branch": self.branch(), "head": self.head(), "files": files, "policy": policy,
                   "index_diff": hashlib.sha256(self.run("diff", "--cached", "--binary").stdout).hexdigest(),
                   "worktree_diff": hashlib.sha256(self.run("diff", "--binary").stdout).hexdigest()}
        return {"action": "local", "plan_id": digest(details), "branch": details["branch"], "head": details["head"],
                "paths": audit["paths"], "file_ids": files, "clean": audit["clean"], "scope": "whole-worktree"}

    def authorize(self, action, plan, approval):
        policy = self.policy()
        mode = (policy or {}).get(action, "ask" if action == "local" else "off")
        if mode == "off":
            raise Blocked(action + "_disabled", 78)
        if policy and self.branch() not in policy["branches"]:
            raise Blocked("branch_outside_saved_scope", 78)
        if mode == "ask" and approval != plan["plan_id"]:
            raise Blocked("user_confirmation_required", 78, action=action, plan_id=plan["plan_id"])
        if approval and approval != plan["plan_id"]:
            raise Blocked("approval_plan_changed", 78)
        return mode

    def note(self, phase, **data):
        state = self.read(self.session_path) or {"task": "closeout"}
        state.update(phase=phase, updated_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **data)
        self.save(self.session_path, state)

    def commit(self, message, approval):
        if not message or message.startswith("-"):
            raise Blocked("commit_message_required", 64)
        plan = self.local_plan()
        if plan["clean"]:
            emit(local="noop", head=self.head(), remaining=0)
            print("CLOSEOUT_COMMITS=0\nCLOSEOUT_FILES_TOTAL=0\nCLOSEOUT_REMAINING=0")
            return
        self.authorize("local", plan, approval)
        with self.lock():
            if self.local_plan()["plan_id"] != plan["plan_id"]:
                raise Blocked("plan_changed_before_staging", 75)
            self.note("local_pending", plan_id=plan["plan_id"])
            self.run("add", "-A", "--", ".")
            self.preflight()
            # Refuse concurrent worktree edits instead of chasing them with extra commits.
            if self.run("diff", "--name-only", "-z").stdout or self.run("ls-files", "--others", "--exclude-standard", "-z").stdout:
                raise Blocked("changes_during_staging", 75)
            staged = self.paths("diff", "--cached", "--name-only", "-z")
            if set(staged) != set(plan["paths"]):
                raise Blocked("staged_scope_changed", 75)
            for path in staged:
                blob = self.run("show", ":" + path, check=False)
                if blob.returncode == 0:
                    self.validate_blob(path, blob.stdout)
                    expected = plan["file_ids"][path]
                    if expected.startswith("symlink:"):
                        expected = hashlib.sha256(os.fsencode(expected.removeprefix("symlink:"))).hexdigest()
                    if hashlib.sha256(blob.stdout).hexdigest() != expected:
                        raise Blocked("staged_content_changed", 75, path=path)
                elif plan["file_ids"][path] != "deleted":
                    raise Blocked("staged_content_changed", 75, path=path)
            result = self.run("commit", "-m", message, check=False, timeout=60)
            if result.returncode:
                raise classify(result.stderr, "commit_identity_or_hook_failed")
            head = self.head()
            audit = self.audit()
            phase = "remote_due" if (self.policy() or {}).get("remote", "off") != "off" else "local_verified"
            self.note(phase if audit["clean"] else "remaining_changes", head=head, remaining=audit["paths"])
            emit(local="committed", commit=head, files=len(staged), remaining=len(audit["paths"]), paths=audit["paths"])
            print(f"CLOSEOUT_COMMIT={head}\nCLOSEOUT_COMMITS=1\nCLOSEOUT_FILES_TOTAL={len(staged)}\nCLOSEOUT_REMAINING={len(audit['paths'])}")
            if not audit["clean"]:
                raise Blocked("concurrent_changes_remain", 75)

    def push_url(self, name):
        if not name or name.startswith("-") or name not in self.text("remote").splitlines():
            raise Blocked("configured_remote_missing", 78)
        urls = self.text("remote", "get-url", "--push", "--all", name).splitlines()
        if len(urls) != 1 or urls[0].startswith("-") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*::", urls[0]):
            raise Blocked("multiple_or_unsupported_push_destinations", 78)
        url = urls[0]
        if "://" in url:
            parsed = urlsplit(url)
            if parsed.password or (parsed.scheme in {"http", "https"} and parsed.username) or parsed.query or parsed.fragment:
                raise Blocked("credential_bearing_remote_url", 3)
            if parsed.scheme not in {"http", "https", "ssh", "git", "file"}:
                raise Blocked("unsupported_remote_transport", 78)
        return url

    def destination(self, name):
        return digest(self.push_url(name))

    def remote_tip(self, policy):
        result = self.run("ls-remote", "--exit-code", "--", self.push_url(policy["remote_name"]), policy["target_ref"], check=False)
        if result.returncode == 2:
            return None
        if result.returncode:
            raise classify(result.stderr, "remote_access_or_authentication_failed")
        rows = result.stdout.decode().splitlines()
        if len(rows) != 1:
            raise Blocked("ambiguous_remote_reference", 78)
        return rows[0].split()[0]

    def scan_history(self, head, reviewed):
        # Baseline consent covers all its reachable history; inspect its tree and each later commit.
        commits = self.text("rev-list", "--max-count=" + str(MAX_HISTORY_COMMITS + 1), reviewed + ".." + head).splitlines()
        if len(commits) > MAX_HISTORY_COMMITS:
            raise Blocked("history_scan_limit_manual_review_required", 3)
        commits.append(reviewed)
        seen = set()
        for commit in commits:
            for entry in self.run("ls-tree", "-r", "-z", commit).stdout.split(b"\0"):
                if not entry:
                    continue
                meta, rawpath = entry.split(b"\t", 1)
                mode, kind, oid = meta.decode().split()
                path = os.fsdecode(rawpath)
                if kind != "blob" or mode == "120000":
                    raise Blocked("published_submodule_or_symlink_requires_review", 3, path=path)
                base = Path(path).name.lower()
                if SENSITIVE.fullmatch(base) and base not in SAFE_ENV:
                    raise Blocked("history_credential_filename", 3, path=path)
                if oid in seen:
                    continue
                seen.add(oid)
                if len(seen) > MAX_HISTORY_BLOBS or int(self.text("cat-file", "-s", oid)) > MAX_BLOB:
                    raise Blocked("history_scan_limit_manual_review_required", 3)
                self.validate_blob(path, self.run("cat-file", "blob", oid).stdout)
        return len(commits), len(seen)

    def push_plan(self):
        self.preflight()
        policy = self.policy()
        if not policy or policy["remote"] == "off":
            raise Blocked("remote_disabled", 78)
        if self.branch() not in policy["branches"] or self.branch() != policy["source_branch"]:
            raise Blocked("branch_outside_saved_scope", 78)
        if self.destination(policy["remote_name"]) != policy["destination_id"]:
            raise Blocked("remote_destination_changed", 78)
        if not self.audit()["clean"]:
            raise Blocked("push_requires_clean_worktree", 78)
        head = self.head()
        if not head:
            raise Blocked("push_requires_commit", 78)
        reviewed = policy.get("history_reviewed_tip")
        if not reviewed or self.run("merge-base", "--is-ancestor", reviewed, head, check=False).returncode:
            raise Blocked("history_review_missing_or_lineage_changed", 78)
        anchor = policy.get("history_scan_tip", reviewed)
        if self.run("merge-base", "--is-ancestor", anchor, head, check=False).returncode:
            raise Blocked("history_scan_lineage_changed", 78)
        tip = self.remote_tip(policy)
        if tip == head:
            return {"action": "remote", "noop": True, "head": head, "plan_id": digest([head, tip, policy])}
        if tip and self.run("merge-base", "--is-ancestor", tip, head, check=False).returncode:
            raise Blocked("remote_diverged_or_history_not_available", 78)
        commits, blobs = self.scan_history(head, anchor)
        plan = {"action": "remote", "head": head, "remote_tip": tip, "remote_name": policy["remote_name"],
                "target_ref": policy["target_ref"], "visibility": policy["visibility"], "commits_scanned": commits,
                "blobs_scanned": blobs, "destination_id": policy["destination_id"], "noop": False}
        plan["plan_id"] = digest([plan, policy])
        return plan

    def push(self, approval):
        plan = self.push_plan()
        if plan["noop"]:
            self.note("remote_verified", head=plan["head"])
            emit(remote="already_at_target", head=plan["head"])
            return
        self.authorize("remote", plan, approval)
        with self.lock():
            if self.push_plan()["plan_id"] != plan["plan_id"]:
                raise Blocked("push_plan_changed", 75)
            self.note("remote_pending", plan_id=plan["plan_id"], head=plan["head"])
            # Explicit OID and one ref; no force, tags, mirrors, upstream/config changes or submodule pushes.
            endpoint = self.push_url(plan["remote_name"])
            if digest(endpoint) != plan["destination_id"]:
                raise Blocked("remote_destination_changed", 78)
            result = self.run("push", "--porcelain", "--no-follow-tags", "--recurse-submodules=no", endpoint,
                              plan["head"] + ":" + plan["target_ref"], check=False, timeout=60)
            if result.returncode:
                raise classify(result.stderr, "push_rejected_or_result_unverified")
            if self.remote_tip(self.policy()) != plan["head"]:
                raise Blocked("push_result_not_verified", 75)
            policy = self.policy()
            policy["history_scan_tip"] = plan["head"]
            policy["last_verified_push"] = plan["head"]
            self.save(self.policy_path, policy)
            self.note("remote_verified", head=plan["head"], target_ref=plan["target_ref"])
            emit(remote="pushed_and_verified", commit=plan["head"], target_ref=plan["target_ref"])

    def finish_session(self):
        policy = self.policy()
        if policy is None:
            raise Blocked("configure_preferences_before_session_tracking", 78)
        audit = self.audit()
        if not audit["clean"]:
            if policy["local"] == "off" and policy["remote"] == "off":
                self.note("closed_disabled", remaining=audit["paths"])
                emit(session="closed_with_git_disabled", remaining=audit["paths"])
                return
            raise Blocked("local_closeout_pending", 78, paths=audit["paths"])
        if policy["remote"] != "off":
            plan = self.push_plan()
            if not plan["noop"]:
                raise Blocked("remote_closeout_pending", 78, plan_id=plan["plan_id"])
            self.note("remote_verified", head=self.head())
        else:
            self.note("local_verified", head=self.head(), remaining=[])
        emit(session="closed_and_verified", head=self.head())


def set_policy(repo, args):
    if not args.evidence.strip():
        raise Blocked("explicit_user_authorization_evidence_required", 78)
    if SECRET.search(args.evidence.encode()):
        raise Blocked("authorization_evidence_contains_credential_pattern", 3)
    repo.preflight()
    old = repo.policy()
    if old is None and (args.local is None or args.remote is None):
        raise Blocked("initial_local_and_remote_choices_required", 78)
    local = args.local if args.local is not None else (old or {}).get("local", "ask")
    remote = args.remote if args.remote is not None else (old or {}).get("remote", "off")
    branches = args.branch or (old or {}).get("branches", [repo.branch()])
    for branch in branches:
        if repo.run("check-ref-format", "--branch", branch, check=False).returncode:
            raise Blocked("invalid_branch_scope", 64)
    policy = {"schema": SCHEMA, "root": str(repo.root), "gitdir": str(repo.gitdir), "local": local, "remote": remote,
              "branches": branches, "evidence": args.evidence.strip(), "updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    policy["local_evidence"] = args.evidence.strip() if args.local is not None else old.get("local_evidence")
    remote_changed = args.remote is not None or any([args.remote_name, args.target_branch, args.visibility, args.history_reviewed])
    policy["remote_evidence"] = args.evidence.strip() if remote_changed else old.get("remote_evidence")
    if remote != "off":
        name = args.remote_name or (old or {}).get("remote_name")
        target = args.target_branch or (old or {}).get("target_ref", "refs/heads/" + repo.branch()).removeprefix("refs/heads/")
        if repo.run("check-ref-format", "refs/heads/" + target, check=False).returncode:
            raise Blocked("invalid_remote_target", 64)
        reviewed = args.history_reviewed or (old or {}).get("history_reviewed_tip")
        if not reviewed or repo.run("merge-base", "--is-ancestor", reviewed, "HEAD", check=False).returncode:
            raise Blocked("explicit_history_review_required", 78)
        visibility = args.visibility or (old or {}).get("visibility")
        if visibility not in {"public", "private"}:
            raise Blocked("destination_visibility_declaration_required", 78)
        identity = repo.destination(name)
        if old and old.get("destination_id") != identity and not args.history_reviewed:
            raise Blocked("new_destination_requires_review", 78)
        source = repo.branch() if args.remote_name or args.target_branch or not old or old.get("remote") == "off" else old["source_branch"]
        policy.update(remote_name=name, target_ref="refs/heads/" + target, source_branch=source, visibility=visibility,
                      destination_id=identity, history_reviewed_tip=repo.text("rev-parse", "--verify", reviewed + "^{commit}"))
        if old and old.get("destination_id") == identity and old.get("target_ref") == policy["target_ref"] and old.get("history_reviewed_tip") == policy["history_reviewed_tip"]:
            for field in ("history_scan_tip", "last_verified_push"):
                if field in old:
                    policy[field] = old[field]
    with repo.lock():
        repo.save(repo.policy_path, policy)
    emit(policy_saved=True, local=local, remote=remote, branches=branches, location="Git-private codex-closeout/policy.json")


def install_routing(repo, evidence):
    if not evidence.strip() or repo.policy() is None:
        raise Blocked("project_routing_authorization_and_policy_required", 78)
    path = repo.root / "AGENTS.md"
    if path.is_symlink():
        raise Blocked("routing_entry_symlink_requires_review", 78)
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if "<!-- git-workspace-closeout:" in original:
        if ROUTING_BLOCK in original:
            emit(routing="already_installed")
            return
        raise Blocked("existing_routing_block_requires_review", 78)
    # Append one discoverable route; preserve all unrelated instructions byte-for-byte.
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags, 0o600), "a", encoding="utf-8") as stream:
        stream.write(("\n\n" if original else "") + ROUTING_BLOCK)
    emit(routing="installed", file="AGENTS.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit")
    sub.add_parser("policy-show")
    setup = sub.add_parser("policy-set")
    setup.add_argument("--local", choices=MODES)
    setup.add_argument("--remote", choices=MODES)
    setup.add_argument("--branch", action="append")
    setup.add_argument("--remote-name")
    setup.add_argument("--target-branch")
    setup.add_argument("--visibility", choices=("public", "private"))
    setup.add_argument("--history-reviewed")
    setup.add_argument("--evidence", required=True)
    sub.add_parser("plan")
    sub.add_parser("push-plan")
    commit = sub.add_parser("commit")
    commit.add_argument("message")
    commit.add_argument("--approve-plan")
    push = sub.add_parser("push")
    push.add_argument("--approve-plan")
    session = sub.add_parser("session-start")
    session.add_argument("task")
    sub.add_parser("session-status")
    sub.add_parser("session-finish")
    routing = sub.add_parser("install-routing")
    routing.add_argument("--evidence", required=True)
    repo = None
    try:
        args = parser.parse_args()
        repo = Repo()
        if args.command == "audit":
            audit = repo.audit()
            emit(audit=audit, branch=repo.branch(), head=repo.head())
            for key in ("staged", "unstaged", "untracked"):
                print(f"CLOSEOUT_AUDIT_{key.upper()}={len(audit[key])}")
            print(f"CLOSEOUT_AUDIT_TOTAL={len(audit['paths'])}")
        elif args.command == "policy-show":
            policy = repo.policy()
            emit(policy=policy, needs_initial_choices=policy is None)
        elif args.command == "policy-set":
            set_policy(repo, args)
        elif args.command == "plan":
            emit(plan=repo.local_plan())
        elif args.command == "commit":
            repo.commit(args.message, args.approve_plan)
        elif args.command == "push-plan":
            emit(plan=repo.push_plan())
        elif args.command == "push":
            repo.push(args.approve_plan)
        elif args.command == "session-start":
            if repo.policy() is None:
                raise Blocked("configure_preferences_before_session_tracking", 78)
            previous = repo.read(repo.session_path)
            if previous and previous.get("phase") not in {"local_verified", "remote_verified", "closed_disabled"} and previous.get("task") != args.task:
                raise Blocked("previous_session_pending", 78, task=previous.get("task"))
            repo.save(repo.session_path, {"task": args.task, "phase": "active", "start_head": repo.head()})
            emit(session_started=True, task=args.task)
        elif args.command == "session-status":
            emit(session=repo.read(repo.session_path), audit=repo.audit(), head=repo.head())
        elif args.command == "session-finish":
            repo.finish_session()
        elif args.command == "install-routing":
            install_routing(repo, args.evidence)
    except Blocked as error:
        if repo and args.command in {"commit", "push"} and repo.session_path.exists():
            try:
                phase = "awaiting_confirmation" if error.reason == "user_confirmation_required" else "blocked"
                repo.note(phase, error=error.reason)
            except (OSError, Blocked):
                pass
        emit(error=error.reason, **error.details)
        return error.code
    except OSError as error:
        # Avoid printing raw paths, hook output or credentials from diagnostics.
        emit(error="permission_boundary" if error.errno in {1, 13, 30} else "filesystem_failure", errno=error.errno)
        return 77 if error.errno in {1, 13, 30} else 70
    return 0


if __name__ == "__main__":
    sys.exit(main())
