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

## Closure Protocol

Close only after inspecting the outputs that the handoff will claim.

1. List created, changed, retired, and merely inspected artifacts.
2. Validate existence, content, hashes, render, or execution state in proportion to risk.
3. Rerun the optional Git read if tracked files, status, version records, or release candidates changed; record the final `HEAD` and clean/dirty state without claiming a commit that did not occur.
4. Resolve the queued durable events and update only their owning layers.
5. Update current status with a concrete first action that can be executed without reconstructing the session.
6. Record blockers with the condition that would clear each one.
7. Update version records when release identity, compatibility, review revision, or frozen identity changed. Keep receiver-delivery correction rounds on the same SemVer and increment `revision`; apply SemVer bump rules to owner iterations.
8. Update stable design only for durable approved changes; distinguish provisional decisions.
9. Update asset routes and synchronization directions.
10. Append a dated history entry for consequential decisions and state what it supersedes.
11. Reassess affected directories and resolve organization as applied/verified, justified as useful, or a concrete deferred action. Move closed detail out of active context within authority and leave an archive route; see [directory-lifecycle.md](directory-lifecycle.md).
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

## Compaction and Recovery

When chat context is compressed or lost, do not reconstruct from memory alone. Re-enter through the same startup protocol. Trust persisted authorities over conversational recollection, then verify artifacts.

Re-enter the actual instruction entry and its capability checkpoint too. Compare the active next action with the current advertised capability catalog; retrieve only the instructions/schemas that are missing or changed. A summary saying a Skill or MCP was available earlier neither loads its instructions nor proves current access.

If work stopped unexpectedly:

1. inspect the current status and latest history entry;
2. verify recent artifacts and partial outputs;
3. distinguish complete, incomplete, stale, and true zero-result states;
4. record the recovered state and safest rerun or continuation point;
5. avoid deleting ambiguous artifacts until ownership and recoverability are known.

## Staleness Controls

- Put `last verified` on status and high-risk asset entries.
- Store the verifier or method, not only a date.
- Mark provisional claims and expiry conditions.
- Prefer event-driven updates over meaningless routine touches.
- When a status claim is wrong, repair it immediately and record the reason if consequential.
- Archive completed phases so they do not remain in the default startup path.

## Fresh-Session Test

Give a reader only the workspace entry point and a user-like task. The system passes if the reader can, without prior chat:

1. discover constraints;
2. identify the active scope;
3. find verified current state;
4. locate the right authority;
5. state the next action and major risk;
6. avoid loading unrelated topic memory.
7. choose and consult fitting current capabilities without being told their names, and reselect when a later phase changes the needed method or executor.
