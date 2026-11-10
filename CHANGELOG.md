# Changelog

## 1.1.0 - 2026-11-11

Made maintenance part of the workspace lifecycle in `manage-workspace-memory`: after batch output, a version supersession or a phase close, the affected entries and directories are handled in the same task and each scope closes as applied, retained, awaiting a stated user decision, or blocked. Added `references/retention-and-cleanup.md`, which judges value by role, consumers, uniqueness, frozen state, rebuild cost and recovery evidence rather than by name, age, size or duplicate hash; requires recovery proof that covers the current bytes; separates technical permission (such as Full access) from deletion authority; honours scope-specific instructions without re-asking; and executes only exact, rechecked sets. Recovery points are replaced in place while live constraints carry forward and the original wording stays retrievable. Added a declared-scope mode to the read-only audit (`--entry` and `--exclude`) that reports what was not checked. `git-workspace-closeout` gained Claude Code permission guidance and states that a clean tree and its `auto` modes never authorize deletion. Also added a startup reading budget to `manage-workspace-memory`: startup documents replace superseded statements, displaced snapshots move to history at closure, and the read-only audit reports a status document, root instruction entry or memory index file above a UTF-8 byte budget (`STARTUP_FILE_OVER_BUDGET`; 32 KiB by default, `--startup-budget-bytes` to change, `0` to disable). Added a placement rule and a register for tools, runtimes and host configuration outside the workspace root, with a matching asset-index section. Compatible addition; no member-ID, policy-schema, Git helper or existing option changes. An audit that passed before can now report an over-budget startup file; without the new options its scope and other checks are unchanged.

## 1.0.1 - 2026-10-21

Clarified Git first-use scope, independent preference selection, prior authorization disclosure and the interaction between consent and execution permissions. Documented the inherited successful macOS narrow-profile test with its limits and the existing direct Python route for Windows. No runtime, policy-schema or member-ID changes. Preserved published v1.0.0 bytes and tag.

## 1.0.0 - 2026-10-21

First stable Workspace Skills Suite group; 2 declared members. See MIGRATION.md and RELEASE_NOTES.md.

## Pre-stable history

### Release documentation preparation (2026-10-20, before publication)

Added scope and task examples, pinned skills.sh setup and removal instructions, dependency guidance, and release notes. The public version remains 1.0.0; documentation preparation alone does not establish release publication or deployment.

### English public documentation (2026-10-21, before the stable release)

Standardized README, installation, release notes, and changelog prose in English. Existing runtime behavior, Skill IDs, and the first-stable 1.0.0 contract are unchanged.

### Community reporting before stable publication

Added a structured bug-report form and completed the contribution guidance for the stable repository.
