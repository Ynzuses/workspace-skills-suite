# Directory Lifecycle

Keep a long-running workspace easy to browse as its contents grow. Initial scaffolding is only a starting point: revisit the affected directories when their use or lifecycle changes, including inside an already classified project.

## When to Reassess

During an active task, inspect the owning directory and the subdirectories that received outputs:

- before generating a batch, so new outputs have a useful destination;
- after a revision supersedes a candidate, a review round closes, or a phase completes;
- when unrelated purposes accumulate in one folder, current files become hard to identify, or a source/scratch/archive folder itself becomes crowded;
- at materially changed session closure; at startup only when the active scope shows drift or a deferred organization action is due.

Do not scan every project after every command. Reuse the current inventory until another relevant batch or lifecycle event changes it. Finish necessary work, then resolve the affected directory before handoff; do not wait for another user request to notice the problem.

The optional read-only helper inventories directory metadata:

```text
python scripts/inspect_directory_layout.py --root owning-scope --format text
```

It ranks folders by direct file count and reports extension counts, child directories, excluded areas, nested repositories, and incomplete reads. Its default `--direct-file-limit 30` is a configurable review signal, not an acceptance threshold. Twenty mixed revisions may need work while hundreds of indexed, homogeneous source snapshots may be appropriate. The helper cannot decide authority, redundancy, retention, or whether anything is safe to move or delete. Counts below the limit do not clear semantic problems.

Use repeatable `--exclude relative-directory` for declared frozen, external, private, or generated trees that need no inspection. Defaults omit common tool/cache directories; links and reparse points are skipped and nested repositories are reported without descent. Run separately inside a separately owned repository only when relevant. Output contains local path metadata; keep private inventories local.

## Classify by Actual Use

Check the current status, asset/version records, scripts, and references before classifying files. Names, modification dates, a matching extension, or an old revision number alone do not establish obsolescence.

| Role | Treatment |
| --- | --- |
| Current authority and its required editable/export formats | Keep together at an obvious current entry; name the exact version/revision |
| Required evidence, inputs, or reproducibility dependencies | Preserve and route from the consuming artifact, even if old or rarely opened |
| Superseded draft or closed review/verification bundle | Archive as a coherent revision or phase with a successor pointer |
| Submitted, sent, published, or otherwise frozen baseline | Preserve exact bytes and identity; retain its existing path unless relocation is explicitly allowed |
| Temporary extraction, rendering, download, or intermediate output | Isolate by task/run; retain anything needed to reproduce or verify the current result |
| Ownership, authority, or dependency still uncertain | Leave in place and record the specific unresolved classification |

Before new work, choose the destination by purpose and lifecycle. Put transient render/extraction output in a bounded task/run area rather than adding it beside the deliverable. Promote a scratch script used by the maintained workflow into the owning code area and update callers; a `tmp` label does not prove disposability.

## Use the Smallest Useful Split

Within the owning project, separate current work, retained evidence, closed revisions, and scratch only where that distinction helps retrieval. Preserve the project's names and conventions. Keep an artifact family together across Markdown, editable documents, exports, comments, and its relevant verification record; extension-only buckets break that relationship.

Reassess the destination too. A single flat `history/`, `sources/`, or `tmp/` can recreate the original problem. Split it further by the dimension people actually retrieve: artifact family plus revision, closed phase, source subject/collection batch, or task/run. Use dates when time is the retrieval key. Do not add empty categories, arbitrary depth, or one folder per file to satisfy a count. An indexed homogeneous collection can remain flat.

For example, a report may keep its current editable/export set in `report/current/`, a closed review bundle in `report/history/r1/`, sources in `report/evidence/`, and page renders in `scratch/report-r2/`. These are examples, not required names. Maintain one current entry and one archive route, rather than listing every historical file in default startup memory.

## Plan and Apply Within Existing Authority

First produce a concrete difference plan: exact source and destination, role, reason/successor, dependencies, authorization, and verification. Reuse the existing asset or migration record; create a separate ledger only for a move batch that needs one. Do not copy private incident details into reusable examples.

The current task or standing workspace rules may already authorize local organization. Honor that authority without repeatedly asking. Implicit Skill invocation alone supplies none. If asset moves are outside the current authority, finish the read-only classification and reviewable plan, record the bounded pending action, and request only the missing authorization. Deletion, frozen-content changes, cross-owner moves, and external publication require their own applicable authority; archiving does not imply deletion.

For an authorized move:

1. Resolve source/destination paths inside the allowed owning scope; check frozen paths, user changes, repository boundaries, links/reparse points, and destination collisions. Do not move an entire mixed folder while any child is unresolved.
2. Record old/new relative paths and integrity evidence in one batch record. Hash unique, frozen, or consequential assets; use a proportionate count/size/hash check for reproducible scratch. Preserve exact bytes where required and avoid overwrite.
3. Move the coherent bundle using recoverable operations. Keep submitted bytes unchanged and leave frozen baselines in place unless relocation was authorized.
4. Update current entry points, asset/status/version routes, live links, scripts/configuration, and affected dependency/ignore rules. Preserve the meaning of historical paths and hashes; use the move map or a compact redirect rather than rewriting frozen documents or old audit evidence.
5. Search live consumers for old paths, verify targets and content identities, and reopen the current artifact through its normal entry. If validation fails, restore from the move map or mark the migration incomplete; do not claim tidy completion.

## Closure Result

Resolve each affected scope as: organization applied and verified; existing layout remains useful with a concrete reason; or a bounded pending action with exact blocker/authority and next step. Persist this only when the finding changes durable state; an unchanged healthy inspection creates no administrative files.

The next reader must be able to find the current artifact without comparing filenames, open a retained revision through an archive route, and follow current dependencies without a broken path. A clean root with a crowded child or an archive that still serves as the default current entry has not met that outcome.
