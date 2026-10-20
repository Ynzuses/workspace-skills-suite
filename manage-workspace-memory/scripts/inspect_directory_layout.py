#!/usr/bin/env python3
"""Read-only directory metadata inventory; never classifies files as obsolete."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys


DEFAULT_EXCLUDES = {
    ".git", ".hg", ".svn", ".agents", ".codex", ".venv", "venv",
    "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".cache",
}


def positive_integer(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def relative_exclusion(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ":" in value or ".." in path.parts or str(path) == ".":
        raise ValueError("exclusions must be non-root relative directories without '..'")
    return path.as_posix()


def is_link(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def inspect_layout(root: Path, direct_file_limit: int, limit: int,
                   exclusions: list[str]) -> dict:
    # Explicit roots are trusted scope selections; never follow links below them.
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be an existing directory")
    excluded = {relative_exclusion(value) for value in exclusions}
    directories: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        relative = directory.relative_to(root).as_posix()
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda item: (item.name.casefold(), item.name))
        except OSError as exc:
            errors.append({"path": relative, "error_type": type(exc).__name__})
            continue
        if directory != root and any(entry.name == ".git" for entry in entries):
            skipped.append({"path": relative, "reason": "nested_repository"})
            continue
        extensions: Counter[str] = Counter()
        child_directories = files = byte_count = 0
        for entry in entries:
            path = directory / entry.name
            entry_relative = path.relative_to(root).as_posix()
            try:
                info = entry.stat(follow_symlinks=False)
                if is_link(info):
                    skipped.append({"path": entry_relative, "reason": "link_or_reparse_point"})
                elif stat.S_ISDIR(info.st_mode):
                    child_directories += 1
                    if entry.name in DEFAULT_EXCLUDES or entry_relative in excluded:
                        skipped.append({"path": entry_relative, "reason": "excluded_directory"})
                    else:
                        pending.append(path)
                elif stat.S_ISREG(info.st_mode):
                    files += 1
                    byte_count += info.st_size
                    extensions[path.suffix.casefold() or "[no extension]"] += 1
            except OSError as exc:
                errors.append({"path": entry_relative, "error_type": type(exc).__name__})
        directories.append({
            "path": relative, "direct_files": files,
            "child_directories": child_directories, "direct_bytes": byte_count,
            "extensions": dict(sorted(extensions.items())),
            "review_signal": files >= direct_file_limit,
        })
    directories.sort(key=lambda item: (-item["direct_files"], item["path"].casefold(), item["path"]))
    return {
        "schema_version": 1, "complete": not errors,
        "direct_file_limit": direct_file_limit,
        "scanned_directories": len(directories),
        "scanned_files": sum(item["direct_files"] for item in directories),
        "review_signal_count": sum(item["review_signal"] for item in directories),
        "omitted_directory_rows": max(0, len(directories) - limit),
        "directories": directories[:limit],
        "skipped": sorted(skipped, key=lambda item: item["path"]),
        "errors": sorted(errors, key=lambda item: item["path"]),
        "interpretation": "Counts are review signals, not obsolete-file or move/delete decisions.",
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--direct-file-limit", type=positive_integer, default=30)
    parser.add_argument("--limit", type=positive_integer, default=20)
    parser.add_argument("--exclude", action="append", default=[], help="Root-relative directory; repeatable.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    arguments = parser.parse_args()
    try:
        payload = inspect_layout(arguments.root, arguments.direct_file_limit,
                                 arguments.limit, arguments.exclude)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"complete": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if arguments.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"DIRECTORY INVENTORY: {'complete' if payload['complete'] else 'incomplete'}")
        print(f"Scanned: {payload['scanned_directories']} directories, {payload['scanned_files']} files")
        print(f"Count signals: {payload['review_signal_count']}; omitted rows: {payload['omitted_directory_rows']}")
        for item in payload["directories"]:
            marker = "review" if item["review_signal"] else "inspect by use"
            print(f"{item['direct_files']:5} files | {item['child_directories']:3} child dirs | {item['path']} | {marker}")
            print(f"      extensions: {json.dumps(item['extensions'], ensure_ascii=False)}")
        for item in payload["skipped"]:
            print(f"SKIP {item['path']}: {item['reason']}")
        for item in payload["errors"]:
            print(f"ERROR {item['path']}: {item['error_type']}")
        print(payload["interpretation"])
    return 0 if payload["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
