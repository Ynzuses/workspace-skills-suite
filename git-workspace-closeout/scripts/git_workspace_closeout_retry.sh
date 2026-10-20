#!/usr/bin/env bash
set -euo pipefail

# Compatibility entrypoint: repeating a denied command cannot change its sandbox.
# The caller must use an available, allowed tool-level permission mechanism.
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec bash "$script_dir/git_workspace_closeout.sh" "$@"
