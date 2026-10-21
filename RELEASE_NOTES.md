# v1.0.1 — Workspace Skills Suite

This patch makes Git closeout's first-use choices and execution requirements explicit. The first stable v1.0.0 remains unchanged.

## What changed

- The Skill entrypoint and UI prompt introduce whole-worktree scope before changes, explain `off` / `ask` / `auto`, show applicable prior authorization, and ask for missing local-snapshot and remote-push choices together. No preference is preselected.
- README and the installation guide explain how consent, Git-metadata access, network, authentication and destination scope must match. Automatic consent does not grant operating-system permissions; Full access does not grant action consent.
- The permission guide carries forward the dated successful macOS narrow-profile test and its untested client/platform boundaries. Full access is not a general requirement.
- Windows users can call the existing Python driver directly; Bash and a `python3` alias are needed only for the optional shell entrypoints. The deterministic consent/runtime implementation is unchanged.

## Install or update

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.1 --skill "*" --agent codex
```

Requires Node.js 22.20.0+ and npm/npx for this installer, plus Git for repository downloads. Project scope is the default; add `--global` for user scope or `--copy` where links are unavailable. Review existing copies before replacing them. See [INSTALL.md](INSTALL.md) for both members, exact paths, runtime dependencies, the consent/permission matrix and removal.

## Compatibility and verification

Members remain `manage-workspace-memory` and `git-workspace-closeout`; command interfaces, stored policy schemas and repository boundaries are unchanged. Upgrade complete Skill directories; existing private repository preferences remain in Git metadata. Installation does not create policy, configure permissions or install background automation. See [MIGRATION.md](MIGRATION.md), [STABILITY.md](STABILITY.md), and [VALIDATION.md](VALIDATION.md).

Portable helper tests do not prove that every future agent invokes the Skill or that every client accepts a permission profile. The inherited profile experiment has its own date and platform; it is not claimed as a new cross-platform run.

## Downloads, license and feedback

Assets: `workspace-skills-suite-1.0.1.zip` and `workspace-skills-suite-1.0.1.zip.sha256`. Compare the ZIP's SHA-256 with its companion file before extraction. The custom ZIP contains `SHA256SUMS` and `RELEASE_MANIFEST.json`; GitHub's automatic Source code archives have their own packaging bytes.

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE); retained terms in [NOTICE](NOTICE). Use [CONTRIBUTING.md](CONTRIBUTING.md) and GitHub Issues for synthetic, reproducible reports without private data.
