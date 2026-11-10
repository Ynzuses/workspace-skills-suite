# v1.1.0 — Workspace Skills Suite

This minor release turns workspace maintenance into a routine part of finishing work, keeps a long-running workspace cheap to resume and portable between machines, and covers Claude Code alongside Codex. Earlier tags remain unchanged.

## What changed

- **Maintenance at the boundary where clutter appears.** After batch output, a version supersession or a phase close, `manage-workspace-memory` handles the affected entries and directories as part of that work instead of waiting for a cleanup request. Each affected scope closes as *applied*, *retained* (with a reason), *awaiting decision* (put to the user in the conversation with candidates, evidence, size and recovery route), or *blocked*. A session with nothing to do writes nothing.
- **Retention and cleanup decisions.** A new reference decides what stays, moves to history or leaves the workspace from each item's role, consumers, uniqueness, frozen state, rebuild cost and recovery evidence. A `tmp` name, old date, zero size or duplicate hash is never enough on its own. Recovery evidence must cover the current bytes (a tracked path is not proof). Client Full access is capability, not consent; a scope-specific instruction to judge and delete is consent for items that pass the checks and is not requested again; archiving never implies deletion. Deletions run only on exact, rechecked sets and are verified afterwards.
- **Recovery points that keep their history.** A superseded current statement is replaced in place, live constraints carry forward, and the original wording stays retrievable with its link base. A shorter file or a clean Git tree is not accepted as proof of maintenance.
- **Declared-scope audit.** `audit_workspace_memory.py --entry AGENTS.md --exclude history` checks only the declared active route, leaves history snapshots, templates and third-party copies unread, and reports what was not reached or excluded. Without these options the audit behaves as before.
- **Claude Code guidance for Git closeout.** `git-workspace-closeout` documents Claude Code's permission rules, modes, protected `.git` handling and sandbox limits next to the Codex profile method, including why a `git push` ask rule cannot see a push made inside the helper. A clean tree after a snapshot, and the Skill's `auto` modes, never authorize deleting files.
- **Startup reading budget.** `manage-workspace-memory` now treats the instruction entry, the memory index and the current status as documents with a reading budget. A superseded statement is replaced, not kept beside its successor; the displaced snapshot moves to history at session closure and leaves one route line.
- **Audit signal.** `audit_workspace_memory.py` reports `STARTUP_FILE_OVER_BUDGET` when a status document, a root instruction entry or a memory index file exceeds a UTF-8 byte budget. The default is 32 KiB. `--startup-budget-bytes N` sets another value and `0` turns the check off. A public README is not counted.
- **Dependencies outside the root.** A placement rule decides whether a tool travels inside the workspace or is installed at a machine-level location, and every dependency outside the root is registered with its caller, identity, check and rebuild route. The asset-index template has a section for this register.
- `git-workspace-closeout`'s helper and stored policy are unchanged.

## Install or update

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.1.0 --skill "*" --agent codex
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.1.0 --skill "*" --agent claude-code
```

Requires Node.js 22.20.0+ and npm/npx for this installer, plus Git for repository downloads. Project scope is the default; add `--global` for user scope or `--copy` where links are unavailable. Review existing copies before replacing them. See [INSTALL.md](INSTALL.md) for both members, exact paths, runtime dependencies, the consent/permission matrix and removal.

## Compatibility and verification

Members remain `manage-workspace-memory` and `git-workspace-closeout`; existing command options, stored policy schemas and repository boundaries are unchanged. The audit gains the `--startup-budget-bytes`, `--entry` and `--exclude` options, a `scope` field in its JSON output, and one issue code, so a workspace that passed before can now exit with status 1 when a startup document is over budget. Retire superseded text to history, raise the budget, or pass `--startup-budget-bytes 0` to keep the earlier behavior. Upgrade complete Skill directories. See [MIGRATION.md](MIGRATION.md), [STABILITY.md](STABILITY.md), and [VALIDATION.md](VALIDATION.md).

The audit measures size and link structure only. It cannot tell whether the text that remains is current, and it does not move or delete anything. A blind comparison of this version with the previous candidate on six synthetic maintenance scenarios found no regression; both versions handled all six correctly, so it does not demonstrate an improvement. See [VALIDATION.md](VALIDATION.md).

## Downloads, license and feedback

Assets: `workspace-skills-suite-1.1.0.zip` and `workspace-skills-suite-1.1.0.zip.sha256`. Compare the ZIP's SHA-256 with its companion file before extraction. The custom ZIP contains `SHA256SUMS` and `RELEASE_MANIFEST.json`; GitHub's automatic Source code archives have their own packaging bytes.

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE); retained terms in [NOTICE](NOTICE). Use [CONTRIBUTING.md](CONTRIBUTING.md) and GitHub Issues for synthetic, reproducible reports without private data.
