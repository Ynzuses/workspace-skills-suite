---
name: manage-workspace-memory
description: "Maintain durable project workspaces across sessions: authority and directory design, progressive memory, task-aware Skill/tool/MCP routing after phase changes or context recovery, historical-revision organization, status/index/DAG updates, SemVer identities, optional read-only Git recovery, and frozen handoffs. Compose with domain skills. Do not use for routine cleanup, one-off notes, isolated short-lived tasks, Git commits/pushes, or cloud/vector memory."
metadata:
  version: "1.0.1"
---

# Manage Workspace Memory

## Purpose

Make a long-running workspace recoverable without loading its entire history. Infer a minimal directory and authority blueprint from the project's deliverables, ownership, lifecycle, shared assets, privacy, computation, and release boundaries. Keep rules, current state, stable design, asset locations, topic knowledge, and historical decisions distinct but connected, so a new session can find the right authority and resume with a verified first action.

## Route the Task

Read only the references needed for the request:

- **Layer design, source-of-truth decisions, index routing, or conflicts:** read [architecture-and-authority.md](references/architecture-and-authority.md).
- **Session startup, in-session capture, closure, handoff, or compaction recovery:** read [session-lifecycle.md](references/session-lifecycle.md).
- **Capability selection, long-session task/phase changes, Skill/tool/MCP discovery, or restoring capability use after compaction:** read [capability-routing.md](references/capability-routing.md).
- **New workspace setup, restructuring, migration, portability, or integrity audit:** read [bootstrap-and-audit.md](references/bootstrap-and-audit.md).
- **Growing subdirectories, mixed current/history files, revision retirement, or scratch/source accumulation:** read [directory-lifecycle.md](references/directory-lifecycle.md).
- **Version assignment, first-release semantics, review revisions, or optional Git recovery:** read [versioning-and-git.md](references/versioning-and-git.md).
- **Approved deterministic bootstrap, manifest review, dry-run/apply, or bootstrap conflicts:** also read [bootstrap-manifest-contract.md](references/bootstrap-manifest-contract.md).

Read architecture, session lifecycle, and bootstrap references when establishing or substantially rebuilding a workspace memory system. Add directory lifecycle when existing assets need reclassification.

## Core Contract

Use a three-hop progressive read instead of loading every memory file:

1. **Rules and long-term index:** learn constraints, authority boundaries, and where current work is routed.
2. **Current status:** establish what is active, what is blocked, and the first safe next action.
3. **Task evidence:** open only the stable design, asset records, topic memory, or primary artifacts required for the request.

Verify consequential state against physical artifacts before acting. An index is a route to evidence, not evidence that the target still exists or is current.

At every new session, perform the optional local Git read after locating the root and before trusting a status or history claim. If Git is absent or the root is not a repository, record the condition and continue with the same memory-only route.

## Establish the Scope

Before changing files:

1. Find applicable workspace rules and the current working scope.
2. Inventory existing memory, status, design, index, history, and topic files read-only.
3. Identify frozen archives, user-owned edits, private material, and files outside the allowed write boundary.
4. Detect the nearest Git repository and any separately owned nested repositories, when Git is available; keep their read-only coordinates separate.
5. For each versioned artifact family, identify the receiving party or owning user, the purpose mode, and the version/revision authority.
6. State which artifact is authoritative for each fact type; do not impose one universal precedence order on unlike facts.
7. Infer the workspace profile from project characteristics, then select the smallest control plane that can preserve continuity.
8. Produce a proposed blueprint and difference plan before restructuring an existing workspace.

Do not overwrite an existing scheme merely because its filenames differ from the templates. Map its roles first, then repair only missing or conflicting responsibilities. Prefer project or deliverable ownership over file-extension buckets; keep a shared authority once at the highest valid common scope.

## Automation Contract

Treat automation as active-session, event-driven maintenance—not as an unbounded background service.

1. On an authorized bootstrap, merge a concise startup, routing, and closure contract into the workspace's actually discoverable instruction entry, such as `AGENTS.md`; never replace an existing entry wholesale.
2. Match the next bounded action to current advertised capabilities, including user-maintained, third-party, system, and plugin Skills plus built-in/local/MCP/connector tools. Read matching Skill instructions and discover relevant tool schemas through the host's actual mechanism. Project routes are a shortlist, not a capability allowlist.
3. Repeat this match at task/format/system/phase changes, compaction/resume, or a material capability failure; keep valid instructions for unchanged steps. Follow [capability-routing.md](references/capability-routing.md) to persist concise routes and unfinished-work requirements. Do not require the user to remind the agent to select a matching capability; verify selection with realistic tasks without naming the expected specialist.
4. Detect durable events while working, queue only the affected memory layers, and apply one minimal closure update after verifying artifacts. Before batch output, after revision/phase closure, and at materially changed handoff, reassess the affected directories, including crowded source, scratch, and archive children; resolve organization within authority or leave a concrete bounded plan.
5. At startup and closure, use the bundled Git inspector when a repository is available; it is read-only and best-effort.
6. If files change outside an active session, discover the drift at the next startup or explicit audit. Do not claim continuous monitoring.

Implicit invocation grants no additional write authority. Use these boundaries:

| May run read-only | Needs the current task or existing workspace rules to authorize writes | Needs explicit authority for the specific action |
| --- | --- | --- |
| discover rules; inventory; infer a profile; inspect links, directory growth, and drift; propose a blueprint | create missing control-plane files; update affected status, index, DAG, and history records; close a session; carry out local organization already covered by that authority | otherwise move, delete, or overwrite user assets; replace a governance entry; alter a frozen baseline; install watchers, hooks, or scheduled tasks; cloud sync; write outside scope; commit, push, or publish |

Check existing session and standing authorization before asking again. A request to improve a Skill using another project as an example does not authorize reorganizing that example project.

No durable event means no memory-file touch. Routine answers and read-only inspections must not generate administrative churn.

## Maintain Typed Authorities

Keep these roles separate:

| Layer | Answers | Must not become |
| --- | --- | --- |
| Workspace rules | What agents and collaborators may or must do | Project progress log |
| Long-term memory index | Which stable knowledge and active areas exist, and where to read next | A copy of every topic note |
| Current status | What is true now, what is blocked, and what happens next | Permanent design history |
| Stable design | What scope, definitions, contracts, and decisions remain in force | Daily activity journal |
| Asset index | Which artifact is authoritative, where it is, and how it was verified | Duplicate data storage |
| Topic or phase memory | What a bounded workstream has learned | Workspace-wide rulebook |
| Version record | Which artifact family, purpose mode, SemVer, review revision, frozen identity, and compatibility change are in force | Git history or a copy of the artifact |
| Dependency graph | How assets or stages depend on one another | Chronological history |
| History and version control | What changed, when, and why | Current-state authority |
| Audit archive | Closed evidence that must remain inspectable | Default startup context |

Use stable identifiers and repository-relative paths where practical. Point to one authoritative artifact rather than copying the same truth into multiple files.

## Operate the Memory Lifecycle

At session start:

1. read applicable rules and the long-term memory entry point;
2. resolve the active project or workstream;
3. detect and read the nearest relevant Git repository or record that Git is unavailable/not applicable;
4. read its current status;
5. follow indexes to only the task-relevant design, asset, version, and topic records, then match the next action to current Skill/tool capabilities;
6. verify referenced artifacts that will govern the work;
7. begin from the recorded first action or replace it with a reasoned, recorded correction.

During work, recheck capability fit at meaningful work boundaries using [capability routing](references/capability-routing.md); avoid freezing an early phase's tool choices for the entire conversation. Update memory only when a durable fact, decision, authority, dependency, blocker, or next action changes. Keep transient command output and closed detail in audit material, not in the startup path. Choose output destinations before generating batches; use [directory lifecycle](references/directory-lifecycle.md) when current work and historical material start mixing.

At session close:

1. verify the artifacts before summarizing them;
2. update current status and the next executable action; for unfinished multi-step work, retain the needed method/executor and the availability/schema/access checks that must be repeated on resume;
3. update version records when a release identity, review revision, compatibility classification, or frozen hash changed;
4. rerun the optional Git read for tracked changes and bind the handoff to the final `HEAD`/working-tree state;
5. update stable design or asset indexes only where their truth changed;
6. append consequential decisions to history with evidence and supersession links;
7. reassess affected directories, archive closed detail within authority, and keep current and historical routes distinct; record any exact deferred action;
8. test that a fresh session can resume through the three-hop read.

After changing status, indexes, README files, audit pointers, or deployment metadata, perform one final physical-artifact check and rebind every recorded hash to the post-update authoritative artifact. An audit created before the final metadata edit is historical evidence, not the current handoff record. If authoritative rendering timed out or was unavailable, preserve that limitation explicitly instead of inheriting an older page count.

When an artifact is submitted or formally circulated, freeze its exact identity in current status and the asset index. Route new feedback to a new revision rather than silently mutating the submitted baseline, and record the trigger that would reopen or supersede it.

## Resolve Disagreement by Fact Type

When memory, indexes, and artifacts disagree:

- For **existence, size, hash, content, and execution state**, inspect the physical artifact or primary system.
- For **declared scope, definitions, and approved contracts**, use the current stable design unless a newer authorized decision explicitly supersedes it.
- For **current progress and next action**, verify the status record against artifacts. Repair it when the current task or workspace rules authorize maintenance; otherwise report the exact discrepancy and proposed repair.
- For **locations and ownership**, confirm the target, then update the asset index and every inbound route.
- For **past reasoning**, use dated history or version control; never infer current state from chronology alone.
- For **release identity and compatibility**, use the version record and [versioning-and-git.md](references/versioning-and-git.md); Git commit count or review-round count is not a SemVer bump.
- For **rules, permissions, privacy, and frozen boundaries**, follow the most specific applicable current rule.

Record the reconciliation. Do not silently choose whichever file is easiest to edit.

## Bootstrap with Templates

Use these assets as role templates, not mandatory filenames:

- [AGENTS.md.template](assets/AGENTS.md.template)
- [WORKSPACE_RULES.md.template](assets/WORKSPACE_RULES.md.template)
- [WORKSPACE_BLUEPRINT.md.template](assets/WORKSPACE_BLUEPRINT.md.template)
- [MEMORY.md.template](assets/MEMORY.md.template)
- [STATUS.md.template](assets/STATUS.md.template)
- [STABLE_DESIGN.md.template](assets/STABLE_DESIGN.md.template)
- [ASSET_INDEX.md.template](assets/ASSET_INDEX.md.template)
- [DEPENDENCY_GRAPH.md.template](assets/DEPENDENCY_GRAPH.md.template)
- [HISTORY.md.template](assets/HISTORY.md.template)
- [VERSION_RECORD.md.template](assets/VERSION_RECORD.md.template)
- [BOOTSTRAP_MANIFEST.json.template](assets/BOOTSTRAP_MANIFEST.json.template)
- [BOOTSTRAP_MANIFEST.schema.json](assets/BOOTSTRAP_MANIFEST.schema.json)

Copy only the layers the workspace needs. Preserve project conventions and safely merge the selected routes into the actual startup entry point. A template stored elsewhere is not an active instruction.

The agent owns read-only discovery, project profiling, authority design, content rendering, frozen-boundary inventory, and confirmation of the exact plan. The apply helper owns none of those semantic decisions. Start from the pending manifest template, keep it non-executable until the exact create-and-merge plan is authorized, and follow the [manifest contract](references/bootstrap-manifest-contract.md).

Dry-run an approved manifest first:

```text
python scripts/apply_workspace_bootstrap.py --root workspace-root --manifest approved-manifest.json
```

Review the resolved root, approval metadata, targets, conflicts, and planned hashes. Apply that unchanged manifest only within the recorded authority:

```text
python scripts/apply_workspace_bootstrap.py --root workspace-root --manifest approved-manifest.json --apply
```

The helper is root-bound and create-only except for appending its single managed block to the real instruction entry. It does not infer a layout, move or delete assets, replace existing control files, edit a different managed block, invoke Git or network services, or install background automation. A conflict stops the bootstrap for re-inventory and renewed approval; do not edit around it. Re-run the same apply command to verify a byte-identical no-op, then audit the resulting workspace.

For deterministic read-only checks, run:

```text
python scripts/audit_workspace_memory.py --root workspace-root --format text
```

The audit is a triage aid, not semantic proof. Review reported authority conflicts and status claims against physical artifacts before editing.

When Git is available, orient the session with:

```text
python scripts/inspect_workspace_git.py --root workspace-root --format text
```

Validate a version without changing it with:

```text
python scripts/validate_workspace_version.py --file workspace-root/VERSION --mode owner_iteration --change minor
```

## Safety and Privacy

- Default to local, file-based memory. Do not send private workspace contents to vector databases, cloud memory services, or public examples without explicit authorization and a privacy review.
- Do not store secrets, raw sensitive records, or reversible individual-level data in prose memory. Store access rules and safe pointers instead.
- Treat frozen archives as read-only; migrate lessons into a new active location.
- Preserve unrelated user changes and inspect before bulk rewrites, moves, or renames.
- After a move or rename, update routes, links, rules, scripts, and indexes, then check for stale paths and missing targets.
- Separate productizable methods from project facts. A reusable Skill may contain generalized workflow, never private names, paths, results, credentials, or unpublished text.

## Compose with Other Skills

This Skill applies to software, writing, operations, and research projects. Research-specific examples below are optional companions from separate groups, not installation requirements. Select the actual domain method from the current environment; use the same authority and recovery model without a research orchestrator for an ordinary project. `git-workspace-closeout` is bundled in Workspace Skills Suite, but Git and its mutation policy remain optional and separately authorized.

- Use `rigorous-research-workflow` only when an upstream authority change invalidates multiple linked artifacts or one traceable lifecycle/release transition must govern several deliverables; ordinary specialist work may persist directly without orchestration.
- Use `reproducible-computational-research` for workflow provenance, checkpoints, scheduler diagnosis, and computational handoff evidence; this skill owns how those records are routed across sessions.
- Use `research-document-delivery` for Word, Markdown, or PDF engineering; this skill records authority and synchronization state but does not edit binary documents.
- Use domain Skills to judge scientific content. This skill preserves and routes those judgments; it does not replace them.
- Use the current official `skill-creator` when packaging generalized memory practice as a Skill.

## Completion Gate

Do not call the memory system complete until:

- a fresh session can locate rules, current status, and task evidence in at most three routing hops;
- the directory blueprint is justified by project characteristics rather than copied mechanically from a template;
- the discoverable workspace entry routes matching tasks and closure events without requiring repeated user reminders;
- task/phase changes and context recovery re-evaluate current Skills and tools, include relevant third-party capabilities beyond the project shortlist, and distinguish remembered availability from current access or observed success;
- every active pointer resolves, and high-risk status claims have been checked against artifacts;
- each fact type has one clear authority, with duplicates marked as mirrors or historical snapshots;
- every versioned artifact family records its purpose mode, strict SemVer, revision, compatibility change, and frozen identity where applicable;
- Git state is read at startup and closure when available, or the unavailable/not-repository outcome is recorded without blocking work;
- current status contains a concrete next action, blockers, and last verification time;
- final status and asset records point to the post-update hashes and do not rely on a pre-metadata-edit audit;
- submitted or formally circulated artifacts are frozen by identity, and later work has an explicit revision route;
- stable design is separated from transient progress and history;
- moves, supersessions, and archived detail remain traceable;
- affected subdirectories have been reassessed after batches, revision replacement, and phase closure; current artifacts are easy to identify, and any deferred organization has a concrete plan;
- privacy, frozen-archive, and public-release boundaries are explicit;
- a no-change session leaves memory artifacts untouched, and read-only audits do not mutate the workspace;
- no placeholder, secret, personal path, or project-specific content remains in reusable outputs.
