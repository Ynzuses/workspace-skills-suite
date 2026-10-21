# Persistent consent and remote scope

## Establish the two choices independently

Before setup, follow the first-use conversation in [SKILL.md](../SKILL.md). Show the user the actual scope and existing authorization, explain all three modes, and ask for both missing choices together. There is no preselected consent policy. An instruction for one task's commit cannot silently become a standing preference for whole-worktree snapshots. Initial `policy-set` requires both channel choices; remote `off` is a user choice to collect, not a value to invent when the user has only chosen local automation.

Read current user instructions, applicable repository rules and `policy-show` first. Reuse explicit standing authorization. If a choice is missing, ask whether **local whole-worktree snapshots** should be off, confirmed every time, or automatic; ask the same separately for **remote pushes**. Present both together if both are missing. Do not reinterpret “automatic commits” as permission to send data elsewhere. If “open source” is ambiguous, resolve the intended hosting repository, branch and public visibility before transmission.

Scope defaults to this physical repository/worktree and its current branch, not all repositories. If a user explicitly requests wider branch scope, enumerate those branches. No default global preference is created. If local mode is `off`, remote mode can still send an explicitly reviewed, already-existing commit; it cannot create new commits implicitly.

## Save only an actual choice

After explicit setup consent, use the entrypoint:

```bash
bash "<skill-dir>/scripts/git_workspace_closeout.sh" policy-set --local auto --remote off --evidence "User chose automatic local snapshots for this repository"
```

This example is not authorization. Replace its values/evidence with the user's real choices. `policy-show` must verify the record. If persistence fails, keep the choice in the active task/handoff if possible and report that durable setup is pending; do not claim it will survive future sessions.

For remote setup, confirm an existing destination, source branch, target branch and visibility. Review every commit reachable from the chosen baseline, including deleted secrets/private materials and redistribution rights. Then, only if explicitly authorized:

```bash
bash "<skill-dir>/scripts/git_workspace_closeout.sh" policy-set --remote ask --remote-name origin --target-branch main --visibility public --history-reviewed "<reviewed-commit>" --evidence "User chose per-push confirmation for this reviewed destination"
```

The helper binds the destination's fingerprint and exact source/target branch. It rejects credential-bearing HTTPS URLs and multiple/unsupported push destinations. It uses the actual push URL for both comparison and sending; an origin's distinct fetch URL is not assumed to be the destination. It does not configure remotes, authenticate a host or establish platform visibility.

## Execute under the saved mode

| Action | `off` | `ask` | `auto` |
| --- | --- | --- | --- |
| Local snapshot | Leave files and report disabled | Run `plan`, show paths/deletions and message, await reply, pass its `plan_id` to `commit --approve-plan` | Review/check current plan, run `commit` without a repeated consent question |
| Remote push | Do not send | Run `push-plan`, show destination/branch/visibility/history scope, await separate reply, pass its `plan_id` to `push --approve-plan` | Run `push-plan`, check saved scope and blockers, then `push` without a repeated consent question |

A confirmation is bound to the current content, HEAD, branch, policy and, for pushes, observed destination tip. Changed content or scope invalidates it. A local token cannot approve a remote plan. The plan token is a freshness guard, not evidence that a human approved it; the agent must wait for the real reply. A dry run or an affirmative reply about a different action is insufficient.

Changing `auto` to `ask` or `off` takes effect before the next action. Do not ask the user to reconfirm their old automatic choice when updating another field. Preserve the other channel unless they also change it. A failed preference write is not a successful revocation record: stop dependent mutations, retain the latest user instruction and repair persistence within permissions before continuing.

## Context and publication boundaries

An existing remote, paid hosting account, repository name or Full access does not authorize pushing. A saved scope cannot silently follow a renamed/replaced destination, different worktree or a copied repository. A public/private declaration must match user intent; if its actual hosting state is consequential and unknown, inspect through an available authorized read-only platform tool or obtain the missing fact before pushing. Do not describe a declaration as independently verified visibility.

User-approved baseline review covers all old reachable history. The helper checks that its lineage still applies, scans that baseline tree plus subsequent commits, and advances the scan anchor only after verified pushes. It does not claim an independent full-history audit of older commits. If initial history cannot be reviewed, keep remote mode off or pending; do not silently treat a clean tip as a safe history.

Creating a repository, making a private repository public, uploading releases, force pushes, deleting branches and opening external publication records are separate mutations, not enabled by `remote=auto`. Changes required by privacy, scope or hosting rules are concrete blockers, not excuses to ask for the same automation preference again.
