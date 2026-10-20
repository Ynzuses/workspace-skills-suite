# Versioning and Git

## Why two coordinates are required

Semantic Versioning 2.0.0 describes compatibility of a versioned artifact. A review round, a user-visible draft, a Git commit, and a submitted baseline answer different questions. Record them separately:

| Coordinate | Answers | Example |
| --- | --- | --- |
| `version` | Which compatible artifact release is this? | `1.0.0` |
| `revision` | Which correction or review round is this? | `r3` |
| `git` | Which repository state produced it? | `main@abc1234` |
| `stable_id` | Which artifact family does it belong to? | `report:methods` |

Use a strict SemVer 2.0.0 value for `version`: `MAJOR.MINOR.PATCH`, with only the standard numeric or ASCII pre-release and build metadata forms. Do not put review-round text into the SemVer value. Write it in a separate `revision` or history field.

Apply SemVer to a released workspace artifact or coherent artifact family, such as a deliverable, workflow contract, template set, or public package. Do not invent a new SemVer for every scratch note, transient status edit, or cache file. Those files use their path, content hash, status timestamp, and optional Git coordinate; the owning artifact's version record explains which files belong to a released identity.

## Decide whose perspective controls the release identity

Before assigning a first or next version, record the work purpose as one of these modes:

### `receiver_delivery`

Use this when the work is being produced for a school, client, employer, journal, regulator, or another receiving party. The first artifact that the agent presents to the user after its internal preparation is the first receiver-facing version, even before the receiver confirms it. Give that artifact the first release identity (normally `1.0.0`). If the user sends it back for corrections, keep the same `version` across those rounds and increment `revision` (`r1`, `r2`, …). Preserve each returned artifact as a traceable revision when it matters; do not silently overwrite a submitted or circulated baseline.

Work that never reached the user before that first presentation is preparation. If such a draft was given a version label, use a pre-first release such as `0.1.0` or `0.0.1`; if it was prematurely labelled `1.0.0`, reclassify that draft in its own record, link the old label in history, and reserve `1.0.0` for the first receiver-facing artifact. Renaming a file is optional; correcting its version record and preserving the provenance is required.

### `owner_iteration`

Use this when the user is improving their own workspace, workflow, reusable template, or product contract. A user-requested iteration is a new release candidate. Apply SemVer compatibility rules to choose the bump: `PATCH` for a compatible defect correction, `MINOR` for a backward-compatible capability or rule addition, and `MAJOR` for an incompatible contract, authority, or behavior change. The words “first version” and “second version” describe release generations; they do not override SemVer. A second generation is `2.0.0` only when the change is actually breaking or the owner explicitly declares a new major contract.

If the purpose is ambiguous, stop version assignment, ask which party's acceptance defines the release identity, and record the answer in the status or version record. Do not infer the mode from the number of chat turns.

## First-version procedure

For a versioned artifact family:

1. Give the family a stable ID and identify its receiver or owner.
2. Record `purpose_mode`, `first_presented_version`, `release_version`, `revision`, and `compatibility_change` before handoff.
3. Treat internal agent edits before the first user presentation as one preparation phase; they do not create separate user-facing versions.
4. For `receiver_delivery`, keep the release version stable through requested corrections and advance only the revision field until the receiving assignment closes.
5. For `owner_iteration`, compare the new contract with the prior released artifact and bump exactly one SemVer component according to compatibility.
6. When an artifact is submitted or formally circulated, freeze its exact content hash, version, revision, and Git coordinate in status and the asset index.
7. Route later feedback to a new revision record. Never mutate a frozen identity in place.

The version record should use repository-relative paths and contain no private content. A minimal record is:

```text
stable_id: <artifact family>
purpose_mode: receiver_delivery | owner_iteration
first_presented_version: <SemVer>
release_version: <SemVer>
revision: r<number>
compatibility_change: patch | minor | major | same-release-correction
status: draft | candidate | submitted | accepted | superseded
content_sha256: <sha256 or pending>
git_coordinate: <repository-relative root>@<commit or detached>
supersedes: <stable id/revision or none>
```

## Startup Git read

Git is an optional recovery aid, not a prerequisite for ordinary work. At every new session, after locating the workspace root and before trusting a status or history claim:

1. Detect whether `git` is installed and whether the active root is inside a work tree.
2. If Git is available, run the local read-only inspector or the equivalent commands to capture the repository root, branch or detached state, `HEAD`, short status, recent history, and remote names.
3. Check for nested repository boundaries when the workspace contains separately owned products or public mirrors. Read each relevant repository from its own root; never treat a public mirror as the activity source.
4. Compare the result with the workspace rules, status, asset index, and recorded Git coordinate. Report drift before mutation.
5. Use commit history to reconstruct why and when a change occurred, while keeping current progress in the status file. Git history does not replace a current status panel.

If the command is missing, the root is not a repository, or a repository cannot be read, record `git_state: unavailable`, `not_repository`, or `read_error` with the reason and continue through the memory-only protocol. This condition must not block work or cause fabricated commit claims.

The inspector must not fetch, pull, push, commit, amend, reset, checkout, alter hooks, or write workspace files. Do not copy private remote URLs, commit bodies, paths, or history into reusable public memory. Persist only the minimum coordinate needed for resumption, normally repository-relative root, branch/detached state, short `HEAD`, a clean/dirty summary, and the verification time.

## Closure and drift

At closure, rerun the Git read when a tracked file, status, version record, or release candidate changed. Bind the final record to the post-edit `HEAD` and working-tree state; if the session did not commit, record `uncommitted` rather than inventing a commit. A clean tree is evidence about Git state only, not evidence that the scientific or editorial content is correct.

When a later session finds a different `HEAD`, changed tracked files, an unexpected branch, or a public mirror that diverged from its source, queue a reconciliation event. Verify the physical artifact first, then repair status, asset routes, version records, and history together. Do not copy a newer mirror back into the activity source without an explicit authority decision.

## Recommended command

The bundled inspector is dependency-free and read-only:

```text
python manage-workspace-memory/scripts/inspect_workspace_git.py --root workspace-root --format text
```

Use `--format json` when another local tool needs machine-readable output. A zero exit status includes the normal no-Git cases so an optional capability cannot block the workspace workflow; use `--require-git` only when a task explicitly requires repository evidence.

For a strict SemVer check and deterministic next-version calculation:

```text
python manage-workspace-memory/scripts/validate_workspace_version.py --version 1.0.0 --mode owner_iteration --change minor
```

The version helper does not edit files or choose the purpose mode. The agent must make that semantic decision from the user's objective and record the evidence.
