"""Synthetic directory-pressure tests; no real user assets are classified."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


SCRIPT = (Path(__file__).resolve().parents[1] / "manage-workspace-memory"
          / "scripts" / "inspect_directory_layout.py")
spec = importlib.util.spec_from_file_location("directory_layout", SCRIPT)
assert spec and spec.loader
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)


def snapshot(root: Path) -> dict:
    return {str(path.relative_to(root)): path.read_bytes() if path.is_file() else None
            for path in root.rglob("*") if not path.is_symlink()}


def run(root: Path, *arguments: str) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "cp936"
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--format", "json", *arguments],
        capture_output=True, text=True, encoding="utf-8", env=environment, check=False,
    )


class DirectoryLayoutTests(unittest.TestCase):
    def test_nested_pressure_stable_unicode_output_and_no_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="目录 盘点 ") as directory:
            root = Path(directory)
            crowded = root / "project" / "历史 r1"
            crowded.mkdir(parents=True)
            for name in ("a.md", "b.MD", "binary.pdf", "opaque"):
                (crowded / name).write_bytes(b"\xff\x00not UTF-8")
            before = snapshot(root)
            first = run(root, "--direct-file-limit", "3")
            second = run(root, "--direct-file-limit", "3")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(snapshot(root), before)
            payload = json.loads(first.stdout)
            self.assertTrue(payload["complete"])
            self.assertEqual(payload["scanned_files"], 4)
            self.assertEqual(payload["review_signal_count"], 1)
            hotspot = payload["directories"][0]
            self.assertEqual(hotspot["path"], "project/历史 r1")
            self.assertEqual(hotspot["extensions"], {".md": 2, ".pdf": 1, "[no extension]": 1})
            self.assertNotIn(str(root), first.stdout)

    def test_excludes_tools_explicit_archive_and_nested_repositories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (".git", "node_modules", "archive", "public-copy", "scratch"):
                target = root / name
                target.mkdir()
                (target / "data.txt").write_text("synthetic", encoding="utf-8")
            (root / "public-copy" / ".git").write_text("gitdir: synthetic", encoding="utf-8")
            before = snapshot(root)
            completed = run(root, "--exclude", "archive")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["scanned_files"], 1)
            self.assertEqual({item["path"] for item in payload["directories"]}, {".", "scratch"})
            self.assertIn({"path": "public-copy", "reason": "nested_repository"}, payload["skipped"])
            self.assertEqual(snapshot(root), before)

    def test_limit_preserves_total_signals_and_empty_directory_is_not_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("first", "second"):
                (root / name).mkdir()
                (root / name / "one.txt").write_bytes(b"x")
            payload = layout.inspect_layout(root, 1, 1, [])
            self.assertEqual(payload["review_signal_count"], 2)
            self.assertEqual(payload["omitted_directory_rows"], 2)
            self.assertEqual(len(payload["directories"]), 1)
        with tempfile.TemporaryDirectory() as directory:
            payload = layout.inspect_layout(Path(directory), 30, 20, [])
            self.assertTrue(payload["complete"])
            self.assertEqual(payload["review_signal_count"], 0)

    def test_rejects_escape_root_exclusion_and_invalid_limits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            for value in ("../outside", ".", "/outside", "C:\\outside"):
                completed = run(Path(directory), "--exclude", value)
                self.assertEqual(completed.returncode, 2)
                self.assertFalse(json.loads(completed.stderr)["complete"])
            self.assertEqual(run(Path(directory), "--limit", "0").returncode, 2)
            self.assertEqual(run(Path(directory), "--direct-file-limit", "-1").returncode, 2)

    def test_missing_root_and_file_root_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file.txt").write_bytes(b"x")
            for bad in (root / "missing", root / "file.txt"):
                result = run(bad)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(json.loads(result.stderr)["complete"])

    def test_partial_read_is_not_reported_as_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "blocked").mkdir()
            original = os.scandir

            def guarded(path):
                if Path(path).name == "blocked":
                    raise PermissionError("synthetic unreadable directory")
                return original(path)

            with mock.patch.object(layout.os, "scandir", side_effect=guarded):
                payload = layout.inspect_layout(root, 30, 20, [])
            self.assertFalse(payload["complete"])
            self.assertEqual(payload["errors"], [{"path": "blocked", "error_type": "PermissionError"}])

    def test_windows_reparse_attribute_is_a_skip_signal(self) -> None:
        self.assertTrue(layout.is_link(SimpleNamespace(st_mode=0o040755, st_file_attributes=0x400)))
        self.assertFalse(layout.is_link(SimpleNamespace(st_mode=0o100644, st_file_attributes=0)))

    def test_does_not_follow_external_or_cyclic_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            root = parent / "root"
            root.mkdir()
            outside = parent / "outside"
            outside.mkdir()
            (outside / "private.bin").write_bytes(b"synthetic")
            try:
                (root / "external").symlink_to(outside, target_is_directory=True)
                (root / "cycle").symlink_to(root, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {type(exc).__name__}")
            payload = layout.inspect_layout(root, 30, 20, [])
            self.assertTrue(payload["complete"])
            self.assertEqual(payload["scanned_files"], 0)
            self.assertEqual({item["path"] for item in payload["skipped"]}, {"external", "cycle"})


if __name__ == "__main__":
    unittest.main()
