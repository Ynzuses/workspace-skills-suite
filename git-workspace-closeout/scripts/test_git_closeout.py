#!/usr/bin/env python3
"""Behavioral checks in disposable repositories; no real remote services."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

SCRIPT = Path(__file__).with_name("git_closeout.py").resolve()
WRAPPER = SCRIPT.with_name("git_workspace_closeout.sh")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="git-closeout-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "work space"
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_TEMPLATE_DIR=str(self.base / "empty-template"))
        Path(self.env["GIT_TEMPLATE_DIR"]).mkdir()
        self.git("init", "-q", "--initial-branch=main")
        self.git("config", "user.name", "Fixture Author")
        self.git("config", "user.email", "fixture@example.invalid")

    def git(self, *args, cwd=None, check=True):
        result = subprocess.run(["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def cli(self, *args, code=0, cwd=None, env=None):
        result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd or self.repo, env=env or self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        data = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        self.assertTrue(data, result.stdout)
        return data[-1]

    def policy(self, local="auto", remote="off", **kwargs):
        args = ["policy-set", "--local", local, "--remote", remote, "--evidence", "Explicit fixture user choice"]
        for key, value in kwargs.items():
            args += ["--" + key.replace("_", "-"), value]
        return self.cli(*args)

    def file(self, name="file.txt", text="fixture\n"):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def head(self):
        return self.git("rev-parse", "HEAD").stdout.strip()

    def initial(self):
        self.policy()
        self.file()
        self.cli("commit", "Initial fixture")

    def remote(self, mode="ask", separate_fetch=False):
        self.initial()
        dest = self.base / "remote.git"
        self.git("init", "--bare", "-q", str(dest))
        self.git("symbolic-ref", "HEAD", "refs/heads/main", cwd=dest)
        self.git("remote", "add", "origin", str(dest))
        if separate_fetch:
            other = self.base / "fetch-only.git"
            self.git("init", "--bare", "-q", str(other))
            self.git("remote", "set-url", "origin", str(other))
            self.git("remote", "set-url", "--push", "origin", str(dest))
        self.policy(remote=mode, remote_name="origin", target_branch="main", visibility="public", history_reviewed=self.head())
        return dest

    def test_unconfigured_never_commits(self):
        self.file()
        self.assertTrue(self.cli("policy-show")["needs_initial_choices"])
        result = self.cli("commit", "Blocked", code=78)
        self.assertEqual(result["error"], "user_confirmation_required")
        self.assertFalse((self.repo / ".git/index").exists())

    def test_readonly_plan_does_not_create_private_state_or_index(self):
        self.file()
        self.cli("audit")
        self.cli("plan")
        self.assertFalse((self.repo / ".git/codex-closeout").exists())
        self.assertFalse((self.repo / ".git/index").exists())

    def test_ask_once_approval_and_stale_approval(self):
        self.policy(local="ask")
        self.file()
        plan = self.cli("plan")["plan"]["plan_id"]
        self.cli("commit", "No consent", code=78)
        self.cli("commit", "Confirmed fixture", "--approve-plan", plan)
        old = self.head()
        self.file(text="changed\n")
        self.cli("commit", "Old token", "--approve-plan", plan, code=78)
        self.assertEqual(self.head(), old)

    def test_changed_content_invalidates_confirmation(self):
        self.policy(local="ask")
        self.file()
        plan = self.cli("plan")["plan"]["plan_id"]
        self.file(text="different\n")
        self.cli("commit", "Changed plan", "--approve-plan", plan, code=78)
        self.assertFalse((self.repo / ".git/index").exists())

    def test_auto_persists_without_reasking(self):
        self.initial()
        first = self.head()
        self.file(text="second\n")
        self.cli("commit", "Second fixture")
        self.assertNotEqual(first, self.head())
        self.assertEqual(self.cli("policy-show")["policy"]["local"], "auto")

    def test_local_and_remote_independent(self):
        self.initial()
        self.cli("push", code=78)
        self.assertEqual(self.cli("policy-show")["policy"]["remote"], "off")

    def test_revocation_to_ask_takes_effect(self):
        self.initial()
        self.policy(local="ask")
        self.file(text="after revocation\n")
        self.cli("commit", "Must ask", code=78)

    def test_off_blocks_even_once_token(self):
        self.policy(local="off")
        self.file()
        plan = self.cli("plan")["plan"]["plan_id"]
        self.assertEqual(self.cli("commit", "Off", "--approve-plan", plan, code=78)["error"], "local_disabled")

    def test_policy_not_transferred_to_different_repository(self):
        self.initial()
        clone = self.base / "other"
        self.git("clone", "-q", str(self.repo), str(clone))
        store = clone / ".git/codex-closeout"
        store.mkdir()
        (store / "policy.json").write_bytes((self.repo / ".git/codex-closeout/policy.json").read_bytes())
        self.assertEqual(self.cli("policy-show", cwd=clone, code=78)["error"], "policy_repository_mismatch")

    def test_branch_change_does_not_expand_scope(self):
        self.initial()
        self.git("switch", "-q", "-c", "experiment")
        self.file(text="new branch\n")
        self.cli("commit", "Outside scope", code=78)

    def test_sensitive_filename_before_staging(self):
        self.policy()
        self.file("id_rsa")
        self.assertEqual(self.cli("commit", "Private", code=3)["error"], "credential_filename")
        self.assertFalse((self.repo / ".git/index").exists())

    def test_secret_pattern_not_echoed(self):
        self.policy()
        token = "gh" + "p_" + "A" * 30
        self.file(text=token)
        output = self.cli("commit", "Private", code=3)
        self.assertEqual(output["error"], "credential_pattern")
        self.assertNotIn(token, json.dumps(output))

    def test_scan_staged_content(self):
        self.initial()
        self.file(text="gh" + "p_" + "A" * 30)
        self.git("add", "file.txt")
        self.assertEqual(self.cli("plan", code=3)["error"], "credential_pattern")

    def test_partial_staging_preserved(self):
        self.initial()
        self.file(text="stage this\n")
        self.git("add", "file.txt")
        cached = self.git("diff", "--cached").stdout
        self.file(text="leave unstaged\n")
        self.assertEqual(self.cli("commit", "Partial", code=78)["error"], "partial_staging_requires_separate_decision")
        self.assertEqual(self.git("diff", "--cached").stdout, cached)

    def test_index_lock_preserved(self):
        self.policy()
        self.file()
        lock = self.repo / ".git/index.lock"
        lock.write_text("another operation")
        self.cli("commit", "Lock", code=73)
        self.assertEqual(lock.read_text(), "another operation")

    def test_hooks_not_bypassed(self):
        self.policy()
        self.file()
        hooks = self.repo / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o700)
        self.cli("commit", "Hook failure", code=70)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout.strip(), "file.txt")

    def test_unusual_filenames(self):
        self.policy()
        self.file("space name.txt")
        result = self.cli("commit", "Spaced fixture path")
        self.assertEqual(result["files"], 1)
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    @unittest.skipIf(os.name == "nt", "Windows filenames cannot contain newline characters")
    def test_newline_filename(self):
        self.policy()
        self.file("line\nbreak.txt")
        result = self.cli("commit", "Unusual fixture paths")
        self.assertEqual(result["files"], 1)
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    def test_noop_creates_no_commit(self):
        self.initial()
        old = self.head()
        self.assertEqual(self.cli("commit", "Nothing")["local"], "noop")
        self.assertEqual(self.head(), old)

    def test_external_symlink_not_followed(self):
        self.policy()
        target = self.base / "private.txt"
        target.write_text("private fixture")
        try:
            (self.repo / "link.txt").symlink_to(target)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows symlink creation privilege is unavailable")
            raise
        self.assertEqual(self.cli("commit", "External link", code=3)["error"], "external_symlink_requires_review")
        self.assertEqual(target.read_text(), "private fixture")

    def test_detached_head_blocked(self):
        self.initial()
        self.git("checkout", "-q", "--detach", "HEAD")
        self.file(text="detached\n")
        self.cli("commit", "Detached", code=78)

    def test_remote_ask_requires_separate_confirmation(self):
        dest = self.remote()
        plan = self.cli("push-plan")["plan"]
        self.cli("push", code=78)
        self.cli("push", "--approve-plan", plan["plan_id"])
        self.assertEqual(self.git("rev-parse", "refs/heads/main", cwd=dest).stdout.strip(), self.head())

    def test_remote_auto_and_noop(self):
        self.remote("auto")
        self.cli("push")
        self.assertEqual(self.cli("push")["remote"], "already_at_target")
        self.file(text="future automatic change\n")
        self.cli("commit", "Future fixture")
        self.assertEqual(self.cli("session-status")["session"]["phase"], "remote_due")
        self.cli("push")
        self.assertEqual(self.cli("session-status")["session"]["phase"], "remote_verified")

    def test_ask_does_not_change_to_auto_after_one_push(self):
        self.remote()
        plan = self.cli("push-plan")["plan"]
        self.cli("push", "--approve-plan", plan["plan_id"])
        self.file(text="future change\n")
        self.cli("commit", "Future fixture")
        self.cli("push", code=78)
        self.assertEqual(self.cli("policy-show")["policy"]["remote"], "ask")

    def test_remote_destination_changed_blocks(self):
        self.remote("auto")
        other = self.base / "other.git"
        self.git("init", "--bare", "-q", str(other))
        self.git("remote", "set-url", "origin", str(other))
        self.assertEqual(self.cli("push", code=78)["error"], "remote_destination_changed")

    def test_distinct_push_url_is_verified(self):
        dest = self.remote("auto", separate_fetch=True)
        self.cli("push")
        self.assertEqual(self.git("rev-parse", "refs/heads/main", cwd=dest).stdout.strip(), self.head())

    def test_removed_secret_in_unpublished_history_blocks_push(self):
        self.remote("auto")
        self.file(text="gh" + "p_" + "A" * 30)
        self.git("add", "file.txt")
        self.git("commit", "-q", "-m", "Unsafe fixture intermediate")
        self.file(text="clean tip\n")
        self.git("add", "file.txt")
        self.git("commit", "-q", "-m", "Clean fixture tip")
        self.assertEqual(self.cli("push", code=3)["error"], "credential_pattern")

    def test_remote_history_review_is_mandatory(self):
        self.initial()
        dest = self.base / "remote.git"
        self.git("init", "--bare", "-q", str(dest))
        self.git("remote", "add", "origin", str(dest))
        self.cli("policy-set", "--remote", "auto", "--remote-name", "origin", "--visibility", "public", "--evidence", "User fixture", code=78)
        self.assertEqual(self.cli("policy-show")["policy"]["remote"], "off")

    def test_pending_session_survives_new_process(self):
        self.policy()
        self.cli("session-start", "long-task")
        self.file()
        status = self.cli("session-status")
        self.assertEqual(status["session"]["phase"], "active")
        self.assertFalse(status["audit"]["clean"])
        self.cli("session-start", "unrelated-task", code=78)
        self.cli("commit", "Finish fixture")
        self.cli("session-start", "next-task")

    def test_wrapper_uses_same_policy_gate(self):
        self.file()
        result = subprocess.run(["bash", str(WRAPPER), "commit", "No consent"], cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 78)
        self.assertFalse((self.repo / ".git/index").exists())

    def test_routing_append_preserves_existing_rules_and_is_idempotent(self):
        self.policy()
        original = "# Fixture project\n\nKeep user assets.\n"
        entry = self.file("AGENTS.md", original)
        self.cli("install-routing", "--evidence", "User requested project integration")
        self.assertTrue(entry.read_text().startswith(original))
        first = entry.read_bytes()
        self.cli("install-routing", "--evidence", "Same choice")
        self.assertEqual(entry.read_bytes(), first)

    def test_existing_changed_routing_block_not_overwritten(self):
        self.policy()
        entry = self.file("AGENTS.md", "<!-- git-workspace-closeout:begin -->\nCustom rule\n")
        original = entry.read_bytes()
        self.cli("install-routing", "--evidence", "User requested integration", code=78)
        self.assertEqual(entry.read_bytes(), original)

    def test_post_commit_changes_not_chased(self):
        self.policy()
        self.file()
        hooks = self.repo / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        hook = hooks / "post-commit"
        hook.write_text("#!/bin/sh\nprintf 'later\\n' > later.txt\n")
        hook.chmod(0o700)
        self.assertEqual(self.cli("commit", "One approved checkpoint", code=75)["error"], "concurrent_changes_remain")
        self.assertEqual(self.git("rev-list", "--count", "HEAD").stdout.strip(), "1")
        self.assertTrue((self.repo / "later.txt").exists())

    def test_permission_and_lock_classifications_differ(self):
        spec = importlib.util.spec_from_file_location("closeout_fixture", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.classify(b"Unable to create index.lock: Operation not permitted").code, 77)
        self.assertEqual(module.classify(b"Unable to create index.lock: File exists").code, 73)
        self.assertNotEqual(module.classify(b"hook rejected content").code, 77)

    def test_first_configuration_requires_both_channel_choices(self):
        self.cli("policy-set", "--local", "auto", "--evidence", "Only local stated", code=78)
        self.assertFalse((self.repo / ".git/codex-closeout/policy.json").exists())

    def test_changing_local_mode_preserves_remote_choice_and_evidence(self):
        self.remote("auto")
        before = self.cli("policy-show")["policy"]
        self.cli("policy-set", "--local", "ask", "--evidence", "User changed only local consent")
        after = self.cli("policy-show")["policy"]
        self.assertEqual(after["remote"], "auto")
        self.assertEqual(after["remote_evidence"], before["remote_evidence"])
        self.assertEqual(after["destination_id"], before["destination_id"])

    def test_automatic_tag_and_mirror_config_cannot_expand_push(self):
        dest = self.remote("auto")
        self.git("tag", "-a", "fixture-tag", "-m", "Fixture tag")
        self.git("branch", "other-branch")
        self.git("config", "push.followTags", "true")
        self.git("config", "remote.origin.mirror", "true")
        self.cli("push")
        refs = self.git("for-each-ref", "--format=%(refname)", cwd=dest).stdout.splitlines()
        self.assertEqual(refs, ["refs/heads/main"])

    def test_diverged_remote_is_not_force_updated(self):
        dest = self.remote("auto")
        self.cli("push")
        clone = self.base / "other writer"
        self.git("clone", "-q", str(dest), str(clone))
        self.git("config", "user.name", "Other Fixture", cwd=clone)
        self.git("config", "user.email", "other@example.invalid", cwd=clone)
        (clone / "remote.txt").write_text("remote change\n")
        self.git("add", ".", cwd=clone)
        self.git("commit", "-q", "-m", "Other fixture commit", cwd=clone)
        self.git("push", "-q", "origin", "main", cwd=clone)
        before = self.git("rev-parse", "main", cwd=dest).stdout
        self.file(text="local divergent change\n")
        self.cli("commit", "Local divergence fixture")
        self.cli("push", code=78)
        self.assertEqual(self.git("rev-parse", "main", cwd=dest).stdout, before)

    def test_session_finish_detects_missed_commit(self):
        self.policy()
        self.cli("session-start", "long-task")
        self.file()
        self.assertEqual(self.cli("session-finish", code=78)["error"], "local_closeout_pending")
        self.cli("commit", "Finish fixture")
        self.assertEqual(self.cli("session-finish")["session"], "closed_and_verified")

    def test_disabled_git_does_not_prevent_task_closure(self):
        self.policy(local="off")
        self.cli("session-start", "no-git-task")
        self.file()
        self.assertEqual(self.cli("session-finish")["session"], "closed_with_git_disabled")
        self.assertFalse((self.repo / ".git/index").exists())
        self.cli("session-start", "next-task")


if __name__ == "__main__":
    unittest.main()
