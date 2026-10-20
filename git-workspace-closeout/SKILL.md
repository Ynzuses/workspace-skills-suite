---
name: git-workspace-closeout
description: "Finish repository-wide Git snapshots and optional single-branch pushes under persistent, separate local and remote consent. Use for Git closeout, automation preferences, pending commits or permission failures; not for task-scoped staging, branch switching, repository creation or release publishing."
license: Apache-2.0
metadata:
  version: "1.0.0"
---

# Git Workspace Closeout

Close a whole worktree under the user's chosen policy. Support local-only users and users who explicitly want remote updates; do not import a particular project's local-only preference into other repositories. `git commit` records locally; `git push` sends history to a remote, whose visibility may be private or public. Creating a public repository, changing visibility, releasing software and uploading artifacts are separate tasks.

## Read and preserve consent first

Read applicable rules, current user instructions and the physical repository root. Use the stable entrypoint (or a verified thin project wrapper):

```bash
bash "<skill-dir>/scripts/git_workspace_closeout.sh" policy-show
bash "<skill-dir>/scripts/git_workspace_closeout.sh" session-status
bash "<skill-dir>/scripts/git_workspace_closeout.sh" audit
```

Read [authorization.md](references/authorization.md) for setup, preference changes or any remote operation. Resolve **local snapshots** and **remote pushes** independently as `off`, `ask` or `auto`. Reuse explicit prior choices for the same repository and scope; ask only for missing choices, not again for an already selected automatic mode. If the user chose per-action confirmation, obtain a new affirmative reply for each concrete action; silence, an old reply, permission escalation or Full access is not that reply. Current user revocation takes effect before further mutations.

Persist explicitly chosen modes with `policy-set`, including concise authorization evidence. Policy is private to this physical worktree's Git directory and is read again in later processes/sessions. Do not copy it into the public skill, another repository or global settings. Missing policy never authorizes automatic mutation; remote operations are disabled until explicitly configured. Verify successful persistence; do not claim memory was saved after a permission failure.

The helper cannot authenticate the human behind a CLI argument. Only pass `--evidence` for an actual user instruction or applicable explicit authorization, and `--approve-plan` after the user has approved that exact current plan. Never invent either to satisfy the gate.

## Local closeout

1. Resolve branch/HEAD, linked worktree, existing staging and ongoing operations. Audit is repository-wide even from a subdirectory; do not recursively close nested repositories. Whole-worktree consent includes ordinary existing changes, not arbitrary sibling repositories.
2. Review staged, unstaged and untracked paths, meaningful diffs, deletions and required checks. Run `plan`; it is read-only and returns a content-bound `plan_id`. Keep excluded material under justified project policy. Secret scanning is a limited guardrail, not proof of ownership, privacy or safety.
3. Under `auto`, run `commit "<accurate message>"` without repeating the consent question. Under `ask`, show the concrete paths, scope and message; wait for affirmative approval, then run `commit "<message>" --approve-plan "<plan_id>"`. A changed plan requires new approval. Under `off`, leave changes and report the selected disabled state.
4. Run a fresh `audit` and independent `git status --short --untracked-files=all`. Report commit IDs, file count and remaining paths. A single invocation makes at most one commit; new concurrent work is not silently folded into additional snapshots. An explicitly authorized later checkpoint has its own current plan.

The helper preserves hooks and locks, blocks partial staging instead of overriding it, and stops on detached HEAD, conflicts, ongoing operations, nested changes or unexpected content. Fix those through a separately scoped task. A failed commit can leave staged content; preserve and inspect it.

## Remote closeout

Read [authorization.md](references/authorization.md). Require an explicitly bound existing remote, source branch, target branch, declared visibility and reviewed baseline history. Run `push-plan`; it queries the actual push destination and scans the reviewed baseline tree plus every subsequent commit, including intermediate secrets removed from the tip. Human baseline review covers **all reachable prior history** and redistribution rights; the helper does not independently prove that review occurred.

`auto` authorizes only that saved destination and branch scope. `ask` requires a separate reply and the remote plan's own `--approve-plan`. Local confirmation never authorizes a push. Execute `push` only after its gate, then verify the target reference equals the exact pushed commit. Changed destinations, divergent/unknown remote history, scan limits and unavailable authentication stop the operation. Never silently fetch, pull, force, mirror, delete refs, push all branches/tags, create repositories or publish releases.

## Permission failures

Read [permissions.md](references/permissions.md) when metadata or network access is blocked. A saved automatic choice is user intent, not an operating-system permission grant. Prefer an available, allowed authorization mechanism for the **same bounded command**. Do not silently change Codex configuration, turn off the sandbox, install broad allow rules or bypass a denial. If the user explicitly requests permission configuration, the reference describes a supported named profile granting only the verified Git directory while retaining other workspace protections; review and test that setup separately. [recovery.md](references/recovery.md) distinguishes persistent permission boundaries, service failures, locks, hooks and unverified results.

If the environment supports neither an authorized narrow profile nor a permitted command-level approval path and the user requires unattended Git writes, explain that Full access may be necessary in that client and describe its risks before the user changes settings. Full access removes filesystem/network protection; this skill's instructions and checks cannot replace that protection or guarantee against harmful hooks or mistakes.

## Long sessions and resumption

Read [session-closeout.md](references/session-closeout.md) for long tasks, checkpoints and compaction. Once preferences exist, call `session-start "<task-id>"`, carry pending Git state in the active task, and check it after verified phases and before final responses/handoffs; use `session-finish` to detect an omitted closeout. With explicit project-integration authorization, `install-routing --evidence "<instruction>"` appends a minimal route to `AGENTS.md` without replacing existing rules. It installs no background hook or watcher.

A skill alone cannot guarantee execution after a crash, forced stop or a missed invocation. Persisted session state plus a discoverable startup/closure rule reduce omissions and make the next active session recover them. Report `disabled`, `awaiting confirmation`, `blocked` and `not verified` accurately instead of claiming completion.

## Branch and asset boundaries

Use [branching.md](references/branching.md) to judge ordinary history, alternate routes, frozen baselines and parallel work. This skill observes branch scope; it does not switch/create branches or worktrees. Different worktrees keep separate policies and indexes. Shared work directories are not isolated by assigning two branch names.

Even with Full access, do not reset, clean, stash, amend, rewrite history, delete locks, overwrite user assets or bypass hooks. Review hooks as trusted project execution before running them; do not alter or suppress them to get a successful receipt. Public extraction requires its own privacy, history and license review.

## Maintenance and validation

Keep one implementation in `scripts/git_closeout.py`; shell files are stable forwarding entrypoints. Python 3.10+, Bash and Git are required. Run `python3 "<skill-dir>/scripts/test_git_closeout.py"` in a permitted environment: tests use disposable local repositories and bare fixtures, never external services. Test semantic authorization and scope invariants; static validation does not prove future agent compliance or client approval reliability.
