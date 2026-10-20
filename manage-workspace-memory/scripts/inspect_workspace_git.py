#!/usr/bin/env python3
"""Read-only, best-effort Git orientation for a workspace.

The inspector never fetches, writes, stages, commits, resets, or changes a
repository.  Missing Git and non-repository roots are normal outcomes unless
``--require-git`` is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
COMMAND_TIMEOUT_SECONDS = 5
SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "cache",
    "caches",
    "_core_audit",
}


def configure_utf8_streams() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")


def run_git(repo: Path, arguments: list[str]) -> tuple[int, str, str]:
    environment = os.environ.copy()
    # Git's machine-readable fields remain stable even on localized hosts.
    environment["LC_ALL"] = "C"
    environment["LANG"] = "C"
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *arguments],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, "", str(exc)
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    return completed.returncode, stdout, stderr


def find_repository_root(root: Path) -> Path | None:
    code, output, _error = run_git(root, ["rev-parse", "--show-toplevel"])
    if code != 0:
        return None
    candidate = Path(output.strip())
    try:
        return candidate.resolve(strict=True)
    except OSError:
        return None


def discover_nested_repository_roots(root: Path, primary: Path | None) -> list[Path]:
    discovered: set[Path] = set()
    try:
        walker = os.walk(root, topdown=True, followlinks=False)
        for directory, directory_names, file_names in walker:
            directory_path = Path(directory)
            has_git_directory = ".git" in directory_names
            has_git_file = ".git" in file_names
            directory_names[:] = [
                name
                for name in directory_names
                if name not in SKIP_DIRECTORIES
                and not (directory_path / name).is_symlink()
            ]
            if has_git_directory or has_git_file:
                try:
                    candidate = directory_path.resolve(strict=True)
                except OSError:
                    continue
                if primary is None or candidate != primary:
                    discovered.add(candidate)
                # Do not descend into a repository's implementation tree when
                # merely looking for repository boundaries.
    except OSError:
        return []
    return sorted(discovered, key=lambda path: (path.as_posix().casefold(), path.as_posix()))


def parse_status(output: str) -> dict[str, Any]:
    lines = output.splitlines()
    branch_line = lines[0] if lines and lines[0].startswith("##") else None
    entries = lines[1:] if branch_line is not None else lines
    counts = {"staged": 0, "unstaged": 0, "untracked": 0, "conflicted": 0}
    paths: list[str] = []
    for entry in entries:
        if len(entry) < 3:
            continue
        code = entry[:2]
        path = entry[3:]
        paths.append(path)
        if code == "??":
            counts["untracked"] += 1
            continue
        if "U" in code or code in {"AA", "DD"}:
            counts["conflicted"] += 1
        if code[0] not in {" ", "?"}:
            counts["staged"] += 1
        if code[1] not in {" ", "?"}:
            counts["unstaged"] += 1
    return {
        "branch_line": branch_line,
        "is_clean": not entries,
        "counts": counts,
        "changed_paths": paths,
    }


def inspect_repository(repo: Path, workspace_root: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "root": repo.as_posix(),
        "relative_to_workspace": _relative_or_symbolic(repo, workspace_root),
        "state": "read_error",
        "branch": None,
        "detached": None,
        "head": None,
        "status": None,
        "remote_names": [],
        "recent_commits": [],
        "errors": [],
    }

    code, output, error = run_git(repo, ["rev-parse", "--is-inside-work-tree"])
    if code != 0 or output.strip().lower() != "true":
        record["errors"].append(error.strip() or "not a work tree")
        return record
    code, output, error = run_git(repo, ["rev-parse", "--verify", "HEAD"])
    if code == 0:
        record["head"] = output.strip()
    # An initialized repository may be unborn and therefore have no HEAD yet.
    # That is a valid Git state, not an inspector failure.
    code, output, error = run_git(repo, ["symbolic-ref", "--quiet", "--short", "HEAD"])
    if code == 0:
        record["branch"] = output.strip()
        record["detached"] = False
    else:
        record["detached"] = True
    code, output, error = run_git(repo, ["status", "--porcelain=v1", "--branch"])
    if code == 0:
        record["status"] = parse_status(output)
    elif error.strip():
        record["errors"].append(error.strip())
    code, output, error = run_git(repo, ["remote"])
    if code == 0:
        record["remote_names"] = [line for line in output.splitlines() if line]
    elif error.strip():
        record["errors"].append(error.strip())
    code, output, error = run_git(
        repo,
        ["log", "-n", "5", "--date=iso-strict", "--format=%H%x09%ad%x09%s"],
    )
    if code == 0:
        record["recent_commits"] = [
            _parse_commit_line(line) for line in output.splitlines() if line
        ]
    elif record["head"] is not None and error.strip():
        record["errors"].append(error.strip())
    record["state"] = "available" if not record["errors"] else "read_error"
    return record


def _parse_commit_line(line: str) -> dict[str, str]:
    parts = line.split("\t", 2)
    if len(parts) != 3:
        return {"hash": line, "date": "", "subject": ""}
    return {"hash": parts[0], "date": parts[1], "subject": parts[2]}


def _relative_or_symbolic(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix() or "."
    except ValueError:
        return f"external:{path.as_posix()}"


def inspect_workspace(root_argument: Path) -> dict[str, Any]:
    try:
        root = root_argument.resolve(strict=True)
    except OSError as exc:
        return {
            "schema_version": SCHEMA_VERSION,
            "root": str(root_argument),
            "git_available": shutil.which("git") is not None,
            "state": "read_error",
            "repositories": [],
            "errors": [str(exc)],
        }
    if not root.is_dir():
        return {
            "schema_version": SCHEMA_VERSION,
            "root": root.as_posix(),
            "git_available": shutil.which("git") is not None,
            "state": "read_error",
            "repositories": [],
            "errors": ["root is not a directory"],
        }
    if shutil.which("git") is None:
        return {
            "schema_version": SCHEMA_VERSION,
            "root": root.as_posix(),
            "git_available": False,
            "state": "unavailable",
            "repositories": [],
            "errors": ["git executable was not found on PATH"],
        }

    primary = find_repository_root(root)
    nested = discover_nested_repository_roots(root, primary)
    repository_roots = ([primary] if primary is not None else []) + nested
    repositories = [inspect_repository(repo, root) for repo in repository_roots]
    if not repositories:
        state = "not_repository"
        errors = ["workspace root is not inside a Git work tree"]
    elif any(repo["state"] == "read_error" for repo in repositories):
        state = "read_error"
        errors = [
            f"{repo['root']}: {'; '.join(repo['errors'])}"
            for repo in repositories
            if repo["errors"]
        ]
    else:
        state = "available"
        errors = []
    return {
        "schema_version": SCHEMA_VERSION,
        "root": root.as_posix(),
        "git_available": True,
        "state": state,
        "repositories": repositories,
        "errors": errors,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        f"GIT_STATE: {payload['state']}",
        f"WORKSPACE: {payload['root']}",
        f"GIT_AVAILABLE: {str(payload['git_available']).lower()}",
    ]
    if payload.get("errors"):
        lines.extend(f"ERROR: {message}" for message in payload["errors"])
    for index, repo in enumerate(payload["repositories"], start=1):
        status = repo.get("status") or {}
        counts = status.get("counts", {})
        lines.extend(
            [
                f"REPOSITORY[{index}]: {repo['root']}",
                f"  RELATIVE_ROOT: {repo['relative_to_workspace']}",
                f"  STATE: {repo['state']}",
                f"  BRANCH: {repo['branch'] or '(detached or unavailable)'}",
                f"  HEAD: {repo['head'] or '(unborn or unavailable)'}",
                f"  CLEAN: {str(status.get('is_clean')).lower()}",
                "  CHANGES: "
                + ", ".join(
                    f"{key}={counts.get(key, 0)}"
                    for key in ("staged", "unstaged", "untracked", "conflicted")
                ),
                "  REMOTES: " + (", ".join(repo["remote_names"]) or "(none)"),
            ]
        )
        if repo.get("errors"):
            lines.extend(f"  ERROR: {message}" for message in repo["errors"])
        for commit in repo.get("recent_commits", []):
            lines.append(
                f"  COMMIT: {commit['hash'][:12]} {commit['date']} {commit['subject']}"
            )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--require-git", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_utf8_streams()
    args = parse_args(argv)
    payload = inspect_workspace(args.root)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    if args.require_git and payload["state"] != "available":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
