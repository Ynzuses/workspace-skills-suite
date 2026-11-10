# Bootstrap and Audit

## Choose Bootstrap or Refactor

For a new workspace, create the smallest sufficient role set and connect it to the startup entry. For an existing workspace, inventory first and map current files to roles. Refactor only after distinguishing:

- missing responsibility;
- duplicated authority;
- stale route;
- mixed lifecycle;
- naming preference with no functional defect.

A different filename or directory scheme is not itself a defect.

For an existing workspace whose issue is accumulated outputs or mixed revisions, use [directory-lifecycle.md](directory-lifecycle.md) rather than rebuilding its whole control plane. Inspect the affected children, preserve coherent conventions, and design the next batch's destination as well as the historical grouping.

## Read-Only Inventory

Before writing, collect:

1. applicable agent or collaborator rules;
2. README and project-management entry points;
3. memory, status, design, index, history, DAG, and audit files;
4. active project directories and frozen archives;
5. authoritative data, code, document, and result locations;
6. Git availability, repository roots, branches, `HEAD`, work-tree state, nested repository boundaries, and ignore rules;
7. local-only, private, generated, or externally stored assets;
8. version records, release identities, review revisions, and frozen baselines;
9. broken links, missing targets, duplicated names, and contradictory status claims.

Inspect physical artifacts where the inventory affects decisions. Preserve unrelated changes in a dirty workspace.

## Four-Phase Build Procedure

### 1. Discover read-only

Inventory the workspace and characterize:

- projects, research questions, products, and deliverables;
- authority owners and teams;
- shared versus project-specific assets;
- active, generated, cached, externally owned, and frozen lifecycles;
- privacy, version-control, publication, and write boundaries;
- local, remote, container, or HPC execution roots;
- available Git repositories and their synchronization direction;
- existing entry points and coherent conventions worth preserving.

Do not create directories during discovery.

### 2. Propose a blueprint and difference plan

1. Infer lean, standard, or federated architecture from the characteristics above.
2. Assign each fact type and authoritative asset to one owning scope.
3. Map existing paths to needed roles before proposing new names.
4. Decide which party controls each versioned artifact family and choose `receiver_delivery` or `owner_iteration` before assigning a release version.
5. List exact keep, create, link, merge, move, retire, and unresolved actions with reasons.
6. Separate safe control-plane creation from high-impact asset moves or governance changes that need confirmation.
7. Use [capability-routing.md](capability-routing.md) to inspect current Skill metadata and advertised tool discovery surfaces, including third-party and plugin capabilities. Match relevant methods/executors to project task types and propose concise routes with composition, exclusions, and refresh triggers; distinguish installed/configured from callable or access-verified.
8. When safe control-plane creation should be repeatable, render an exact pending manifest from `assets/BOOTSTRAP_MANIFEST.json.template`: list only selected missing directories and Markdown control files, the real instruction entry and managed-block content, the complete frozen-path inventory, and SHA-256 for every rendered payload.

Use `assets/WORKSPACE_BLUEPRINT.md.template` when the reasoning must persist.
The manifest is a mechanical projection of the approved blueprint, not a place to infer one. Keep `approval.state` pending and do not run the helper while any target, authority, frozen boundary, or rendered content remains unresolved.

### 3. Apply within authority

1. Adapt only the role templates the blueprint requires.
2. Seed facts checked against artifacts or explicit decisions; mark unknowns and provisional items.
3. Safely merge startup, task-routing, and closure rules into the actual discoverable entry. Never replace an existing `AGENTS.md` or equivalent wholesale.
4. Link the entry to long-term memory, status, and task-specific authorities.
5. Populate the capability route table from currently observed relevant Skills and tool families, with discovery evidence and refresh triggers. Combine current trigger boundaries with project authorities, keep the table non-exhaustive, and never hard-code unavailable sibling Skills into an independently installed template. Persist a checkpoint for task/phase changes and compaction/resume in the real entry.
6. Add the optional Git read and version-record route to the startup contract without making Git a prerequisite.
7. Create project or deliverable directories only after their ownership and lifecycle are clear.
8. For a deterministic bootstrap, record the exact approving role, decision ID, and time-zone-aware approval time only after the full create-and-merge plan is authorized and the frozen inventory is complete. Validate every content hash, then run the helper without `--apply` and review its JSON change manifest before applying the unchanged manifest. The agent still owns all semantic design; the helper only executes the declared create-and-managed-block operations.
9. Stop on any manifest, path, frozen-boundary, existing-content, or managed-block conflict. Re-inventory and obtain renewed approval if the targets or rendered content change; never weaken the manifest or edit around the conflict.
10. Do not move, delete, overwrite, unfreeze, publish, or install background automation without applicable explicit authority; honor authority already supplied by the task or standing rules. The bootstrap helper has no operation for any of them.

Follow [bootstrap-manifest-contract.md](bootstrap-manifest-contract.md) for the exact schema, fixed markers, dry-run/apply commands, and stop conditions.

### 4. Verify drift and resumption

1. If the deterministic helper was used, compare observed post-write hashes with planned hashes, then run the same apply command again and confirm it reports only existing or unchanged objects while the workspace remains byte-identical.
2. Run the read-only audit script and review its findings semantically.
3. Reconcile links, authority conflicts, status claims, and frozen identities against physical artifacts.
4. Run the Git inspector when available and verify the recorded repository coordinate, branch/detached state, and clean/dirty summary.
5. Run the SemVer helper against each active version record and confirm the purpose mode agrees with the work objective.
6. Run a fresh-session task with only the root entry and a user-like request.
7. Run a no-change closure and confirm memory-file hashes remain unchanged.
8. After restructuring memory, check the final bytes rather than the plan: the saved original snapshot and its hash, a topic or event locator that leads back to it, open constraints and pending decisions carried into the new current entry, and a fresh-session task that resumes from that entry. A shorter file is not, on its own, a passing result.
9. Record remaining risks and the event that should trigger the next review.
10. Use representative tasks without naming the expected specialist, then change phase/format/system after a handoff or compressed context. Observe current third-party Skill instruction reads and relevant tool discovery, alongside a no-specialist control and an unavailable-connector case. Treat plans, observed execution, and actual long-context reliability as distinct evidence.

When several projects share assets, keep shared authorities once at the common scope and reference them. Keep project-specific state inside the owning project. If an existing unusual layout already provides unambiguous ownership, routing, and lifecycle separation, preserve and map it instead of renaming for aesthetics.

## Migration and Rename Procedure

1. Resolve exact source and destination paths and frozen boundaries.
2. Identify the authoritative copy and duplicates before moving anything.
3. Prefer recoverable, staged changes; do not destructively clean broad directories.
4. Update startup rules, READMEs, memory routes, asset indexes, scripts, dependency graphs, ignore rules, and document links.
5. Search for the old path and stale identifier.
6. Compare file counts and, for authoritative assets, content hashes.
7. Record the migration and any intentional compatibility alias.
8. Re-run the three-hop startup test.

If physical assets and indexes disagree, physical inspection establishes location and content; the repaired index then becomes the routing authority.

## External Dependencies and Placement

A workspace is portable only when a reader can tell which of its tools travel with the directory and which must be rebuilt on another machine. Decide the placement of each tool, runtime, or host configuration when it is introduced, and record every dependency that lives outside the workspace root.

| Situation | Placement |
| --- | --- |
| used by this workspace only and runnable without an installer | inside the workspace, in its tools location, so that copying the directory carries it |
| needs an installer, is shared by several workspaces, or is too large to copy with the project | the machine-level location that the workspace rules designate |
| runtime state that a client or host keeps for itself | where the client keeps it; register it, do not relocate it |

Follow the workspace's own rules on drives, quotas, and privacy when they are stricter. Do not let a default installer destination decide placement.

For each dependency outside the root, record in the asset index or the workspace's environment record:

- its name, purpose, and which script, configuration file, or Skill calls it;
- its location, written as a machine path in the environment record and as a symbolic root anywhere reusable;
- its version or other identity, and a command or check that proves it is usable;
- how to rebuild it on a new machine, including the installer source and any configuration that must be registered again;
- whether task content leaves the machine through it, and under which rule that is allowed.

Update the record in the same session that installs, moves, upgrades, or removes the dependency. After copying a workspace to another machine, rebuild from this record and run each check before relying on a remembered route.

## Integrity Audit

Audit at four levels:

### Structural

- expected entry points exist;
- every active status has a parent route;
- every important asset has an owner and authority state;
- topic memories are reachable without being loaded by default;
- history and audits are outside active-status prose;
- startup-path documents are within the reading budget described in [session-lifecycle.md](session-lifecycle.md#startup-budget).

### Referential

- Markdown and declared file links resolve;
- stable IDs are unique;
- paths use the intended root convention;
- moved or retired assets have no unexplained active references;
- mirrors and derivatives state their upstream authority.

### Semantic

- status matches physical artifacts;
- stable design is internally consistent and explicitly superseded where changed;
- Git coordinates and version records match the final physical artifacts when those capabilities are available;
- receiver-delivery corrections retain one release identity while owner iterations use the SemVer compatibility bump;
- next actions are executable and blockers have clearance conditions;
- missing output is distinguished from a verified zero result;
- duplicated claims do not create competing truths.

### Privacy and Portability

- no secret, credential, personal identifier, private URL, or sensitive record is embedded unnecessarily;
- local absolute paths are isolated from reusable products;
- every tool, runtime, or host configuration outside the workspace root is registered with its identity, check, and rebuild route;
- private assets are excluded from public version control and examples;
- frozen archives remain unchanged;
- public templates contain placeholders, not project facts.

The deterministic audit reports inspectable signals; it does not decide scientific truth, authority ownership, or whether a status statement is factually current. Resolve those against primary artifacts and explicit decisions.

Audit the active route separately from historical material. Pass the actual startup entries with `--entry` and declare history snapshots, templates, and third-party copies with `--exclude`; the report then lists what was not reached or excluded and which active links point into excluded directories. A historical snapshot's relative links resolve against the location it was written in, which its history index should record; judge them there instead of rewriting the snapshot. Report "the declared active route passed" rather than a workspace-wide pass, and list the unchecked scope. Volume, mixed topics, several current-looking statements, and repeated rules are signals to explain, not findings the script can settle.

Git and maintenance answer different questions. A clean working tree means tracked changes are committed; it says nothing about ignored or untracked material, unique evidence in scratch areas, or unresolved clutter. Never use a clean tree as the acceptance evidence for maintenance.

## Public Product Extraction

When generalizing the method for publication:

1. extract the workflow rule, not the incident narrative;
2. replace names, counts, paths, results, and unpublished wording with neutral abstractions;
3. use synthetic examples;
4. document public influences and licenses;
5. validate the clean exported package independently;
6. scan both current files and history before release;
7. publish from a separate clean repository, not from a private working tree.

## Acceptance Evidence

Retain a compact audit record containing:

- inventory scope and date;
- authority map;
- files created or changed;
- conflicts resolved and evidence used;
- link and stale-path results;
- privacy and portability results;
- fresh-session test prompt and observed outcome;
- for maintenance: the outcome of each affected scope, the exact set removed or moved with before/after identities, and the retained items whose hashes were rechecked;
- what was not checked, and which results are behavioral observations rather than script results;
- remaining risks and next review trigger.
