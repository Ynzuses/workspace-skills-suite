"""Regression tests for optional Git orientation and workspace SemVer policy."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SOURCE_ROOT = Path(__file__).resolve().parents[1]
GIT_SCRIPT = SOURCE_ROOT / "manage-workspace-memory" / "scripts" / "inspect_workspace_git.py"
VERSION_SCRIPT = (
    SOURCE_ROOT / "manage-workspace-memory" / "scripts" / "validate_workspace_version.py"
)


def run_script(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    )


def git_available() -> bool:
    return subprocess.run(
        ["git", "--version"], check=False, capture_output=True
    ).returncode == 0


@unittest.skipUnless(git_available(), "git is not installed")
class WorkspaceGitInspectorTests(unittest.TestCase):
    def test_non_repository_is_optional_and_require_mode_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="workspace-git-none-") as directory:
            root = Path(directory)
            optional = run_script(GIT_SCRIPT, "--root", str(root), "--format", "json")
            self.assertEqual(optional.returncode, 0, optional.stderr)
            payload = json.loads(optional.stdout)
            self.assertEqual(payload["state"], "not_repository")
            required = run_script(GIT_SCRIPT, "--root", str(root), "--require-git")
            self.assertEqual(required.returncode, 1)

    def test_reads_head_branch_status_and_nested_repository_without_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="workspace-git-read-") as directory:
            root = Path(directory)
            run = lambda *args: subprocess.run(
                ["git", *args], cwd=root, check=True, capture_output=True
            )
            run("init", "-q")
            run("config", "user.email", "test@example.invalid")
            run("config", "user.name", "Synthetic Test")
            (root / "tracked.txt").write_text("one\n", encoding="utf-8")
            run("add", "tracked.txt")
            run("commit", "-qm", "initial synthetic commit")
            nested = root / "public-repo"
            nested.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=nested, check=True)
            (root / "tracked.txt").write_text("two\n", encoding="utf-8")
            (root / "untracked.txt").write_text("new\n", encoding="utf-8")

            completed = run_script(GIT_SCRIPT, "--root", str(root), "--format", "json")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["state"], "available")
            self.assertGreaterEqual(len(payload["repositories"]), 2)
            primary = next(item for item in payload["repositories"] if item["relative_to_workspace"] == ".")
            self.assertTrue(primary["head"])
            self.assertFalse(primary["status"]["is_clean"])
            self.assertEqual(primary["status"]["counts"]["unstaged"], 1)
            self.assertGreaterEqual(primary["status"]["counts"]["untracked"], 2)
            self.assertTrue(any(item["relative_to_workspace"] == "public-repo" for item in payload["repositories"]))

    def test_missing_git_is_a_non_blocking_state(self) -> None:
        spec = importlib.util.spec_from_file_location("workspace_git", GIT_SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="workspace-git-missing-") as directory:
            with mock.patch.object(module.shutil, "which", return_value=None):
                payload = module.inspect_workspace(Path(directory))
            self.assertEqual(payload["state"], "unavailable")
            self.assertFalse(payload["git_available"])


class WorkspaceVersionTests(unittest.TestCase):
    def test_receiver_correction_keeps_release_version_and_uses_revision(self) -> None:
        completed = run_script(
            VERSION_SCRIPT,
            "--version",
            "1.0.0",
            "--mode",
            "receiver_delivery",
            "--change",
            "same-release-correction",
            "--format",
            "json",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["next_version"], "1.0.0")
        self.assertEqual(payload["next_coordinate"], "revision")

    def test_owner_iteration_bumps_only_the_requested_semver_component(self) -> None:
        completed = run_script(
            VERSION_SCRIPT,
            "--version",
            "1.4.2",
            "--mode",
            "owner_iteration",
            "--change",
            "minor",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("NEXT_VERSION: 1.5.0", completed.stdout)

    def test_invalid_semver_and_incompatible_mode_fail_without_editing(self) -> None:
        completed = run_script(
            VERSION_SCRIPT,
            "--version",
            "01.2.3",
            "--mode",
            "owner_iteration",
            "--change",
            "patch",
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("strict SemVer", completed.stderr)
        completed = run_script(
            VERSION_SCRIPT,
            "--version",
            "1.0.0",
            "--mode",
            "receiver_delivery",
            "--change",
            "minor",
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("keep the release version", completed.stderr)

    def test_version_file_is_single_line_and_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="workspace-version-") as directory:
            path = Path(directory) / "VERSION"
            path.write_text("0.1.0\n", encoding="utf-8")
            before = path.read_bytes()
            completed = run_script(
                VERSION_SCRIPT,
                "--file",
                str(path),
                "--mode",
                "owner_iteration",
                "--change",
                "patch",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("NEXT_VERSION: 0.1.1", completed.stdout)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
