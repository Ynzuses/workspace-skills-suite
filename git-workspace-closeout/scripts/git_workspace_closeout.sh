#!/usr/bin/env bash
set -euo pipefail

# Stable entrypoint; all mutations pass through the same persisted policy gates.
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! command -v python3 >/dev/null 2>&1; then
  echo 'CLOSEOUT_ERROR=python3_10_or_newer_required' >&2
  exit 69
fi
if [[ "$#" -eq 0 ]]; then
  set -- audit
fi
exec python3 "$script_dir/git_closeout.py" "$@"
