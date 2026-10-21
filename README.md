# Workspace Skills Suite

Durable project memory, authority and directory design, resumable handoffs and separately authorized Git closeout.

For continuing software, writing, operations, and research projects that need a clear maintenance authority, recoverable context, useful handoffs, or explicitly authorized repository-wide Git closeout.

## Included Skills

| Skill | Purpose |
| --- | --- |
| [manage-workspace-memory](manage-workspace-memory/SKILL.md) | Project authority and directory design, progressive memory, three-hop recovery, capability routing and resumable handoff. |
| [git-workspace-closeout](git-workspace-closeout/SKILL.md) | Whole-worktree snapshots and optional single-branch pushes under separate persistent local and remote consent. |

## Install with skills.sh

After the `v1.0.0` tag is published, run this from the project where you want to use the group:

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

This selects every member for Codex and defaults to the current project. Add `--list` to inspect available members or `--global` for user-wide installation. Use `--skill <skill-name>` to select one member, or choose another supported target such as `--agent claude-code`. Keep the first installation interactive so you can review its destination. Use `--copy` if symbolic links are unavailable.

See **[INSTALL.md](INSTALL.md)** for prerequisites, pinned versions, individual installation, discovery paths, dependencies, updates, and removal. Verify discovery and an actual invocation in the target agent after installing the files.

## Example requests

> Use $manage-workspace-memory to read the existing rules and status, verify source ownership and directory roles, and update the recovery entry for this task.

> Use $git-workspace-closeout to inspect this repository's policy and status read-only. Ask only for missing local-snapshot and remote-push choices; do not commit or push yet.

These are requests to an agent. Codex supports explicit `$skill-name` invocation; other agents use their own invocation interface.

## Requirements and scope

Memory management works without Git. The Git helper requires Python 3.10+, Git, and Bash. On Windows, Git for Windows supplies Bash. See the policy and permission guidance below before using repository-wide closeout.

A Skill runs through an agent; it is not a background commit service. User consent, actual Skill invocation, and permission to execute are separate conditions.

## Git policy and execution permissions

On the first **repository-wide closeout invocation**, the agent reads applicable repository rules and saved policy, then asks only for missing choices. Local snapshots and remote pushes independently use `off`, `ask`, or `auto`. `auto` reuses the saved authorized scope; `ask` requires approval of each concrete plan. Installation creates neither a policy nor a background service.

An explicit standing project instruction may already authorize a specific action. Task-scoped staging or committing is outside this Skill's repository-wide closeout entrypoint. A commit without a prompt therefore does not, by itself, prove either a failed Skill or an active automatic policy. Inspect the read-only `policy-show` and `session-status` output; see [first-use diagnosis](INSTALL.md#git-first-use-and-diagnosis).

A restricted client may protect `.git`. Prefer an allowed command-specific approval or a separately authorized, verified permission profile for one repository. If neither is available and unattended metadata writes are required, the user may need to select Full access. It broadens file and network access; it does not authorize commits, pushes, or publication. The Skill does not change permissions. See the [permission reference](git-workspace-closeout/references/permissions.md).

## Versions, support, and license

`1.0.0` is this group's first stable contract. Read [MIGRATION.md](MIGRATION.md) before replacing an older installation and [RELEASE_NOTES.md](RELEASE_NOTES.md) for this release. Compatibility and verification limits are documented in [STABILITY.md](STABILITY.md) and [VALIDATION.md](VALIDATION.md).

Optional companion groups: `research-skills-suite`, `office-authoring-suite`. They are independent distributions and are not installed with this group. When reporting a problem, include agent/CLI versions, reproducible steps, errors, and a synthetic example. Remove credentials, personal data, and unpublished material.

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE). See [NOTICE](NOTICE) and [PROVENANCE.md](PROVENANCE.md) for attribution and retained component terms.

For proposed changes and reproducible reports, see [CONTRIBUTING.md](CONTRIBUTING.md).
