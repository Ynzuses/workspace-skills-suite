# Session Lifecycle

## Startup Protocol

The goal of startup is verified orientation, not exhaustive reading.

1. **Locate scope.** Confirm the actual working directory and discover the most specific applicable rules.
2. **Read the entry layer.** Read workspace rules and the long-term memory index completely.
3. **Resolve active work.** Identify the project, phase, or workstream that owns the request.
4. **Read Git when available.** Run the read-only inspector for the nearest repository and any separately owned nested repository. Record `unavailable`, `not_repository`, or `read_error` without blocking the session.
5. **Read current status.** Capture objective, last verified state, blockers, and recorded first action.
6. **Route by task.** Open only the stable design, asset index, version record, topic memory, dependency graph, or audit record needed.
7. **Verify before mutation.** Check consequential locations and state against physical artifacts or primary systems.
8. **Start or correct.** Follow the recorded next action if still valid; otherwise record why it changed.

Before implementing that action, perform the [capability routing checkpoint](capability-routing.md): match current intent and target to advertised Skills and tools, read selected instructions, and obtain any needed current schema/access evidence. Stored routes and earlier success are hints, not proof of present availability.

If the entry layer and physical workspace disagree, inspect the workspace first and repair the route before continuing.

## In-Session Capture

Update the appropriate layer when one of these events occurs:

| Event | Update |
| --- | --- |
| policy, permission, or privacy boundary changes | rules |
| durable cross-project lesson or route changes | long-term memory index |
| progress, blocker, or next action changes | current status |
| scope, definition, input contract, or approved method changes | stable design plus history |
| authoritative artifact is created, replaced, moved, or retired | asset index plus affected links |
| release identity, purpose mode, compatibility class, review round, or frozen hash changes | version record plus status/asset index |
| durable bounded-domain lesson emerges | topic memory and parent route |
| dependency or execution order changes | DAG or workflow map |
| consequential decision closes | history with evidence and supersession |
| artifact is submitted or formally circulated | freeze its identity in status and asset index; route later feedback to a new revision |
| detailed investigation closes | audit archive, then link from the owning record |
| output batch, revision supersession, phase closure, or mixed/crowded directory appears | reassess the affected directories using [directory-lifecycle.md](directory-lifecycle.md); update asset routes/history only for actual changes or a durable deferred action |

Maintain a small event queue during the task. Coalesce repeated events affecting the same authority, verify the final artifact, and update each affected layer once near closure. Do not write memory for every command. Preserve durable meaning: what became true, why it matters, where the evidence is, and what should happen next.

Do not touch memory files when no durable event occurred. A read-only answer, an unchanged audit, or a transient failed command is not by itself a memory event.

Re-evaluate capability fit when a request changes the task, output format, system, or operation; when work changes phase; after compaction/resume; or after a material capability failure. Include relevant installed third-party methods and current MCP/connector tools, not just the first phase's selected Skills. Keep this check in working context unless a durable route, blocker, or next action changes. Do not reread unchanged instructions or reload every tool on every command.

Plan output locations before generating batches. Reassess the owning directory and affected children after supersession or phase closure, including an existing archive/source/scratch folder. This check belongs to the work itself; do not defer noticing accumulation until the user asks for cleanup. Distinguish current, dependency, historical, frozen, and uncertain material from authority records rather than filenames or age. Apply authorized organization with route/integrity checks; if authority is missing, prepare the exact plan and bounded next action.

Carry maintenance in the same event queue as the task: the affected scope, the triggering event, and what remains to decide. It stays in working context while the session runs. Write it into the existing status or handoff only when the session ends or is interrupted with the item still open, so that the next session knows which scope is pending, what is missing, and what would clear it.

## Closure Protocol

Close only after inspecting the outputs that the handoff will claim.

1. List created, changed, retired, and merely inspected artifacts.
2. Validate existence, content, hashes, render, or execution state in proportion to risk.
3. Rerun the optional Git read if tracked files, status, version records, or release candidates changed; record the final `HEAD` and clean/dirty state without claiming a commit that did not occur.
4. Resolve the queued durable events and update only their owning layers.
5. Update current status with a concrete first action that can be executed without reconstructing the session. Replace superseded statements instead of appending beside them, and retire displaced text as described in [Startup Budget](#startup-budget).
6. Record blockers with the condition that would clear each one.
7. Update version records when release identity, compatibility, review revision, or frozen identity changed. Keep receiver-delivery correction rounds on the same SemVer and increment `revision`; apply SemVer bump rules to owner iterations.
8. Update stable design only for durable approved changes; distinguish provisional decisions.
9. Update asset routes and synchronization directions.
10. Append a dated history entry for consequential decisions and state what it supersedes.
11. Reassess affected directories and entries, and resolve each scope as **applied** (changed and verified), **retained** (the existing state still serves, with the reason), **awaiting decision** (a specific question for the user), or **blocked** (a stated condition). Move closed detail out of active context within authority and leave an archive route; see [directory-lifecycle.md](directory-lifecycle.md) and, for anything that might leave the workspace, [retention-and-cleanup.md](retention-and-cleanup.md). Put every awaiting-decision item to the user in the closing message as well as in the handoff.
12. Re-run the startup route mentally or with a fresh reader: rules/index, Git state, status, task evidence.
13. After the status/index/audit-pointer edits are complete, rehash authoritative artifacts and re-run the hash-bound checks; do not leave the handoff pointing at an audit made before the final metadata edit.
14. If an artifact was submitted, mark the submitted hash, release version, revision, and Git coordinate as frozen and name the next revision identity or feedback trigger; do not leave the next session free to overwrite the baseline silently.

The final handoff should state outcome, authority, verification, unresolved risk, and next action. It should not require the next session to read the chat transcript.

## Handoff Record

A robust handoff contains:

- **Outcome:** what is now complete or materially changed;
- **Authority:** which artifact now governs each changed fact;
- **Version identity:** purpose mode, SemVer, review revision, compatibility change, frozen hash, and Git coordinate when applicable;
- **Evidence:** how the state was verified;
- **Open items:** blockers, provisional decisions, and unverified assumptions;
- **First action:** one concrete next step, including its input and expected output;
- **Routes:** links or stable IDs needed to continue.

For unfinished work, add only the capability requirements needed for its next action: provider-qualified method/Skill, instruction route, required executor/operation, which discovery/schema/access/result checks actually occurred, and what must be rechecked on resume. See [capability-routing.md](capability-routing.md). Do not copy catalogs, credentials, or full tool schemas into status.

Use timestamps with time zone when order matters. Avoid “continue the analysis” or “check results” as next actions; name the object and the acceptance condition.

When maintenance is still open at handoff, merge a short record into the existing status or task record; do not create a separate maintenance file for it:

```text
affected scope and trigger: ...
outcome so far: applied / retained / awaiting decision / blocked
reason and evidence route: ...
authority held, or the decision still missing: ...
next action and clearance condition: ...
```

Keep execution receipts in the audit layer and route to them. A healthy session with nothing pending writes none of this.

## Compaction and Recovery

When chat context is compressed or lost, do not reconstruct from memory alone. Re-enter through the same startup protocol. Trust persisted authorities over conversational recollection, then verify artifacts.

Re-enter the actual instruction entry and its capability checkpoint too. Compare the active next action with the current advertised capability catalog; retrieve only the instructions/schemas that are missing or changed. A summary saying a Skill or MCP was available earlier neither loads its instructions nor proves current access.

If work stopped unexpectedly:

1. inspect the current status and latest history entry;
2. verify recent artifacts and partial outputs;
3. distinguish complete, incomplete, stale, and true zero-result states;
4. record the recovered state and safest rerun or continuation point;
5. avoid deleting ambiguous artifacts until ownership and recoverability are known.

Resume pending maintenance from its persisted record, not from a summary. When the record shows that the user already authorized an action for a stated scope, and the authority has not been narrowed or withdrawn since, re-verify the scope, each item's current identity, and its consumers, then carry out the items that still qualify without asking again. Anything new, changed, or unknown since the record was written is reassessed and, if unresolved, kept and reported. A summary that says authorization existed is not enough; find where it was given or recorded.

## Staleness Controls

- Put `last verified` on status and high-risk asset entries.
- Store the verifier or method, not only a date.
- Mark provisional claims and expiry conditions.
- Prefer event-driven updates over meaningless routine touches.
- When a status claim is wrong, repair it immediately and record the reason if consequential.
- Archive completed phases so they do not remain in the default startup path.

## Startup Budget

The instruction entry, the long-term memory index, and the current status are read at the start of every session, so their length is a recurring cost. Each one states only what is in force now and should be readable in a single pass with room left for the task.

- **Replace, do not append.** When a statement in a startup document is superseded, the new statement takes its place. A paragraph labelled as historical or superseded does not belong in the startup path.
- **Retire displaced text at closure.** Move a superseded snapshot to history with its date and what replaced it, keeping its wording. Drop it instead when history, a version record, or version control already holds the same content. Leave at most one route line in the startup document.
- **Keep identities, not chronicles.** A frozen baseline keeps its current identity (path, hash, version) in status. Hashes of earlier revisions, per-round acceptance counts, and completed-work logs belong to history or the audit archive.
- **Measure it.** The deterministic audit reports a status document, root instruction entry, or memory index file above its byte budget (32 KiB of UTF-8 by default; `--startup-budget-bytes` sets another value and `0` turns the check off). A workspace whose host reads less in one pass should set a lower value in its rules.
- **Act on the signal within authority.** An over-budget report during a closing session is a durable event for that session: retire the oldest closed sections first, then verify that every inbound link still resolves and that the fresh-session test still passes. Moving text between a status document and its history is ordinary memory maintenance; deleting text that exists nowhere else is not.
- **Carry forward what is still in force.** A new recovery point replaces the old one but inherits its live constraints, open questions, and evidence routes. Losing an unresolved constraint to make a file shorter is a regression, not a cleanup.
- **Preserve before restructuring.** Before rewriting a long entry, save its original text where it can be verified (with its hash), and give the history index a locator by topic or event plus the original link base, so that relative links in the snapshot can still be followed from where they were written. A summary alone cannot answer a later question about why something was decided.
- **Report sizes honestly.** Bytes are not tokens. Report a token saving only when it was measured with the host's tokenizer; otherwise report bytes.

Dated section headings, successor notes, and repeated earlier hashes are the usual signs that a status document has started to serve as its own history.

The budget is a signal for structural review, not a truncation rule. A long file that is entirely current and needed is better than a short one that dropped a live constraint.

## Fresh-Session Test

Give a reader only the workspace entry point and a user-like task. The system passes if the reader can, without prior chat:

1. discover constraints;
2. identify the active scope;
3. find verified current state;
4. locate the right authority;
5. state the next action and major risk;
6. avoid loading unrelated topic memory.
7. choose and consult fitting current capabilities without being told their names, and reselect when a later phase changes the needed method or executor.
