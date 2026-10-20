# Capability Routing Across Long Sessions

Workspace memory preserves what the task needs; current environment discovery establishes what can perform it. Reconnect those two at meaningful work boundaries so an earlier phase's choices do not silently govern the rest of a long conversation.

## Reassess at Work Boundaries

After reading workspace rules and current status, identify the next bounded action: purpose, artifact or system, owning authority, needed operation, validation, and allowed side effects. Match that action to currently available capabilities before implementing it. Do this again when:

- a new request changes the deliverable, format, data source, application, or operation;
- work moves between research, analysis, drafting, document engineering, verification, or delivery;
- context is compacted, a session resumes, or a handoff replaces the working context;
- a selected capability fails, disappears, changes policy/schema, or cannot meet the next action;
- repeated manual work suggests a relevant installed specialist was overlooked.

For an unchanged step, keep using its already read instructions and current tool schema. Do not reload the whole catalog on every message, timer, or tool call. A quick match check can conclude that ordinary reasoning or a built-in tool is sufficient. Do not force workspace-memory administration onto an isolated task with no durable workspace event.

## Discover What Is Available Now

Use the current session's advertised Skill metadata and callable tool catalog first, including user-maintained, third-party, system, and plugin-provided capabilities. A workspace route table is a useful shortlist, not an allowlist. Search beyond it when the task changes. Ownership or preparation for public release is not a reason to prefer one capability for execution; fit, current instructions, target surface, and permissions decide. Redistribution/license review remains a separate task.

For a plausible Skill, read its actual `SKILL.md` through the access mechanism declared by its catalog entry. Read only the relevant supporting references. A name mentioned in a plan is not evidence that its instructions were used. Preserve scope, exclusions, composition requirements, and explicit-only or disabled invocation policy; do not modify that policy to make selection easier. For overlapping names, identify the provider/namespace and target surface before choosing. Choose the smallest set that covers distinct responsibilities; include required companion Skills when their instructions demand them.

If metadata is missing or shortened and there is a concrete reason to expect a matching installed Skill, make a bounded metadata search in the host's declared discovery roots or use its advertised Skill listing/search facility. Read names, descriptions, location, and invocation policy first. A directory found elsewhere, a manager cache, an old version, or a previous machine's catalog does not establish active registration. Do not scan the entire disk, read all Skill bodies, or change installation/configuration as part of discovery. If a verified local instruction package is relevant but registration is unknown, describe it as a manually consulted local workflow, not as proven implicit activation.

For tools, use the host's advertised search/list/schema mechanism when present. Search by the required action and system; inspect only matching definitions and their supported operations. For example, a live-document connector may require listing sessions and reading that session's tool schema before an operation. Follow the provider's actual protocol instead of assuming a universal `tool_search` command or inventing tool names. Use MCP resource listing/reading only where that provider exposes resources and permits that route; an app/connector with its own tools is not automatically a generic MCP resource server.

Do not call accounts, documents, or external services merely to inventory them. Verify access when the current task needs that specific target. Do not read credential stores or copy configuration values to memory. A configured server, installed plugin, remembered endpoint, or past successful call does not prove the current tool is exposed, authenticated, permitted, or useful for this target.

## Make the Selection Concrete

Use a compact working decision, not a large new administrative artifact:

| Question | Decision evidence |
| --- | --- |
| What is the next task and authoritative target? | Current user intent, workspace route, actual artifact/system |
| Which method applies? | Current matching Skill instructions, including relevant third-party options |
| Which executor can act here? | Advertised built-in/local/MCP/connector operation and current schema |
| What must compose? | Distinct method, access, engineering, or validation responsibilities |
| What is allowed now? | Current task and standing rules; actual provider access/policy |
| What demonstrates completion? | Observed artifact, read result, render, calculation, or other required verification |

A Skill can supply the method while an MCP tool accesses or edits the authoritative system. A tool's availability does not replace the method's required checks; a Skill does not create a missing tool or access grant. Prefer the target's supported interface when appropriate. A local export is not a substitute authority for an active cloud document, and a cloud connector is unnecessary for a bounded local-file task.

Read and apply the chosen Skill before custom implementation or bulk execution. If a relevant specialist was skipped, consult it, assess which completed outputs need rechecking, and continue from the verified checkpoint rather than restarting the whole task. State meaningful selections or changes briefly to the user; do not narrate every catalog comparison.

## Keep Routes and Handoffs Useful

During an authorized setup or maintenance task, merge a small routing checkpoint into the actual discoverable workspace instruction entry. A reference stored in an unused directory cannot influence a later session. Keep project routes by task intent and authoritative target rather than copying the machine's entire catalog. Include the discovery source, last check or invalidation trigger, matching method, executor family, boundaries, and fallback only where useful.

Persist only durable changes to task routes, capability requirements, known access blockers, or the next action. Keep transient selection in working context. For unfinished work that crosses a context boundary, add a small capability continuation block to the existing status/handoff:

```text
next action and authoritative input: ...
method/Skill: provider-qualified name and discoverable instruction location
executor: required tool family/operation; observed availability state
checks already completed: instruction read, schema/access check, actual result (distinguish each)
recheck on resume: current catalog/policy/schema/target access as needed
fallback or blocker: ...
```

Do not persist tokens, private endpoints, complete schemas, account inventories, tool transcripts, or a growing list of every capability used. Mark remembered availability as historical. On compaction/resume, reread the root routing contract and the active action, compare against current metadata, then reload only missing or changed instructions/schemas. Do not assume a compressed summary retained them.

## Recover Without Inventing Success

If discovery returns no match, use a suitable built-in or local method and state the material limitation. If a relevant deferred schema can be retrieved, retrieve it before declaring the tool unavailable. If a tool is unavailable, unsupported, or lacks access, change to an equivalent authorized route or leave the exact blocker; do not retry the unchanged failing call indefinitely. Recheck after a meaningful state change, not after every subsequent step.

If new installation, account connection, permission change, private upload, sending, or publication is needed, first determine whether existing instructions authorize that action. Ask only for missing authority after preparing the concrete work that is already possible. Autonomous capability selection grants no additional execution permissions. Do not silently install plugins, enable Skills/MCP servers, expand access, or send messages merely because a useful capability was found.

## Acceptance Evidence

Use realistic tasks that do not name the expected specialist. Include a phase change after noisy history or a compressed summary, a relevant third-party Skill absent from the project shortlist, an overlapping local/cloud/live-app surface, a deferred or disconnected connector, and a simple task where no specialist is needed. Observe instruction reads and actual tool/schema use where possible, output correctness, bounded fallbacks, and unchanged permissions. Plans show routing reasoning only; they do not prove a live MCP call, tool success, or reliability after a truly long context. Record those limits.
