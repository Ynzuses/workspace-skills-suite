#!/usr/bin/env python3
"""Validate a workspace SemVer and calculate a non-mutating next coordinate.

This helper deliberately does not edit VERSION files.  The agent records the
purpose mode and chooses the release identity before using the arithmetic here.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def configure_utf8_streams() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")


def parse_semver(value: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.fullmatch(value)
    if match is None:
        return None
    return tuple(int(match.group(index)) for index in (1, 2, 3))


def bump_version(value: str, change: str) -> str:
    parsed = parse_semver(value)
    if parsed is None:
        raise ValueError(f"not strict SemVer 2.0.0: {value!r}")
    major, minor, patch = parsed
    if change == "major":
        return f"{major + 1}.0.0"
    if change == "minor":
        return f"{major}.{minor + 1}.0"
    if change == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unsupported compatibility change: {change!r}")


def read_version(version: str | None, path: Path | None) -> tuple[str, str | None]:
    if version is not None:
        return version, None
    target = (path or Path("VERSION")).resolve()
    try:
        content = target.read_text(encoding="utf-8", errors="strict")
    except OSError as exc:
        raise ValueError(f"cannot read version file {target}: {exc}") from exc
    lines = content.splitlines()
    if len(lines) != 1 or not lines[0].strip():
        raise ValueError(f"version file must contain exactly one non-empty line: {target}")
    return lines[0].strip(), target.as_posix()


def build_result(
    value: str, *, mode: str, change: str | None, source: str | None
) -> dict[str, Any]:
    parsed = parse_semver(value)
    if parsed is None:
        raise ValueError(f"not strict SemVer 2.0.0: {value!r}")
    if mode == "receiver_delivery":
        effective_change = change or "same-release-correction"
        if effective_change != "same-release-correction":
            raise ValueError(
                "receiver_delivery corrections keep the release version; "
                "use --change same-release-correction and increment revision separately"
            )
        next_value = value
        coordinate = "revision"
    else:
        effective_change = change
        if effective_change is None:
            raise ValueError("owner_iteration requires --change patch, minor, or major")
        if effective_change == "same-release-correction":
            raise ValueError(
                "owner_iteration must use a SemVer patch, minor, or major change"
            )
        next_value = bump_version(value, effective_change)
        coordinate = "version"
    return {
        "valid": True,
        "semver": value,
        "mode": mode,
        "change": effective_change,
        "next_version": next_value,
        "next_coordinate": coordinate,
        "source": source,
    }


def render_text(result: dict[str, Any]) -> str:
    lines = [
        f"SEMVER: {result['semver']}",
        f"MODE: {result['mode']}",
        f"CHANGE: {result['change']}",
        f"NEXT_VERSION: {result['next_version']}",
        f"NEXT_COORDINATE: {result['next_coordinate']}",
    ]
    if result.get("source"):
        lines.append(f"SOURCE: {result['source']}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--version")
    source.add_argument("--file", type=Path)
    parser.add_argument(
        "--mode", choices=("receiver_delivery", "owner_iteration"), required=True
    )
    parser.add_argument(
        "--change", choices=("same-release-correction", "patch", "minor", "major")
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_utf8_streams()
    args = parse_args(argv)
    try:
        value, source = read_version(args.version, args.file)
        result = build_result(value, mode=args.mode, change=args.change, source=source)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
