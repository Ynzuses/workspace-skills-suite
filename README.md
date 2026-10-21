# Workspace Skills Suite

Durable project memory, authority and directory design, resumable handoffs and separately authorized Git closeout.

For continuing software, writing, operations, and research projects that need a clear maintenance authority, recoverable context, useful handoffs, or explicitly authorized repository-wide Git closeout.

## Included Skills

| Skill | Purpose |
| --- | --- |
| [manage-workspace-memory](manage-workspace-memory/SKILL.md) | Project authority and directory design, progressive memory, three-hop recovery, capability routing and resumable handoff. |
| [git-workspace-closeout](git-workspace-closeout/SKILL.md) | Whole-worktree snapshots and optional single-branch pushes under separate persistent local and remote consent. |

## Before your first Git closeout

The agent explains the **whole-worktree** scope, reads your repository rules and saved policy, shows any applicable prior authorization, and asks for missing preferences before making changes. Choose **local snapshots** and **remote pushes** independently:

| Choice | What it means |
| --- | --- |
| `off` | Keep this action disabled |
| `ask` | Review and approve each current action plan |
| `auto` | Reuse this repository's saved, authorized scope without repeated consent questions |

There is no preselected consent policy. Installation starts no service and chooses no preference. A task-specific commit instruction does not silently become whole-worktree automation. Existing explicit choices are reused within their scope and explained; ordinary task-scoped commits and release publishing use separate workflows. See [first-use setup](INSTALL.md#git-first-use-and-diagnosis).

**Full access is not a general requirement.** The action must match both your consent and the client's execution permissions. An `auto` choice cannot write a read-only `.git`; Full access cannot enable an `off` choice. A permitted command approval or separately authorized narrow profile can allow local commits while retaining other sandbox limits. Pushes also require network access, authentication and the reviewed destination. See the [consent/permission matrix](INSTALL.md#how-consent-and-execution-permissions-match) and [dated profile evidence](git-workspace-closeout/references/permissions.md#existing-verification-reuse-before-repeating).

## Install with skills.sh

Run this from the project where you want to use the group:

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.1 --skill "*" --agent codex
```

This selects every member for Codex and defaults to the current project. Add `--list` to inspect available members or `--global` for user-wide installation. Use `--skill <skill-name>` to select one member, or choose another supported target such as `--agent claude-code`. Keep the first installation interactive so you can review its destination. Use `--copy` if symbolic links are unavailable.

See **[INSTALL.md](INSTALL.md)** for prerequisites, pinned versions, individual installation, discovery paths, dependencies, updates, and removal. Verify discovery and an actual invocation in the target agent after installing the files.

## Example requests

> Use $manage-workspace-memory to read the existing rules and status, verify source ownership and directory roles, and update the recovery entry for this task.

> Use $git-workspace-closeout to inspect this repository's policy and status read-only. Ask only for missing local-snapshot and remote-push choices; do not commit or push yet.

These are requests to an agent. Codex supports explicit `$skill-name` invocation; other agents use their own invocation interface.

## Requirements and scope

Memory management works without Git. The Git driver requires Python 3.10+ and Git. Bash is needed only for the optional shell entrypoints; on Windows, the direct Python driver avoids shell/Python-name differences. See the policy and permission guidance below before using repository-wide closeout.

A Skill runs through an agent; it is not a background commit service. User consent, actual Skill invocation, and permission to execute are separate conditions.

## Versions, support, and license

`1.0.0` is this group's first stable contract. Read [MIGRATION.md](MIGRATION.md) before replacing an older installation and [RELEASE_NOTES.md](RELEASE_NOTES.md) for this release. Compatibility and verification limits are documented in [STABILITY.md](STABILITY.md) and [VALIDATION.md](VALIDATION.md).

Optional companion groups: `research-skills-suite`, `office-authoring-suite`. They are independent distributions and are not installed with this group. When reporting a problem, include agent/CLI versions, reproducible steps, errors, and a synthetic example. Remove credentials, personal data, and unpublished material.

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE). See [NOTICE](NOTICE) and [PROVENANCE.md](PROVENANCE.md) for attribution and retained component terms.

For proposed changes and reproducible reports, see [CONTRIBUTING.md](CONTRIBUTING.md).
