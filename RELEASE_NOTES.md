# v1.0.0 — Workspace Skills Suite

Durable project memory, authority and directory design, resumable handoffs and separately authorized Git closeout.

This is the group's first stable release. For continuing software, writing, operations, and research projects that need a clear maintenance authority, recoverable context, useful handoffs, or explicitly authorized repository-wide Git closeout.

## Included in this release

- `manage-workspace-memory`
- `git-workspace-closeout`

Install members by task; other groups are optional companions. Memory management works without Git. The Git helper requires Python 3.10+, Git, and Bash. On Windows, Git for Windows supplies Bash. See the policy and permission guidance below before using repository-wide closeout.

## Installation

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

Project scope is the default. Add `--global` for user-wide use or select one member with `--skill <skill-name>`. Check Node/npm/Git and existing installations first. See the [installation guide](INSTALL.md) for complete setup, dependencies, and removal.

Local snapshots and remote pushes independently use `off`, `ask`, or `auto`; ask only for missing choices. Reuse explicit standing authorization within its scope. Task-scoped commits are outside repository-wide closeout. Restricted clients may require an allowed approval or separately authorized permission setup. Consider Full access only under the documented conditions; it does not replace action consent. See the guide for first-use diagnosis and permission limits.

## Migration

Read [MIGRATION.md](MIGRATION.md) before upgrading. Existing tags and versions retain their identities. Upgrading does not automatically remove old installations, install companion groups, or migrate local settings. `1.0.0` marks the first stable contract; internal review rounds are not public version numbers.

## Validation and limits

A Skill runs through an agent; it is not a background commit service. User consent, actual Skill invocation, and permission to execute are separate conditions. See [VALIDATION.md](VALIDATION.md) for applicable structural, script, and entrypoint checks. Static checks do not guarantee future agent invocation, native application acceptance, or an external connection.

## Downloads and checksums

Custom assets: `workspace-skills-suite-1.0.0.zip` and `workspace-skills-suite-1.0.0.zip.sha256`. The extracted ZIP contains per-file `SHA256SUMS` and `RELEASE_MANIFEST.json`. GitHub's automatic Source code archives come from the tagged tree and have different packaging bytes and generated inventories.

Use `Get-FileHash <zip-path> -Algorithm SHA256` on Windows, `shasum -a 256 <zip-path>` on macOS, or `sha256sum <zip-path>` on Linux, then compare the companion checksum. Signatures, platform listings, and native application acceptance are reported only when actually completed.

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE). See [NOTICE](NOTICE) for retained terms.

## Feedback and contributions

Use GitHub Issues for synthetic reproductions and installation feedback. See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and validation expectations.
