# Retention, Retirement, and Cleanup

Use this reference when maintenance has to decide whether a file or directory stays, moves to history, or leaves the workspace. Four questions are kept apart because they fail in different ways: what the item is worth, who has authorized what, how the action is carried out, and how the result is proven. Settle them in that order. A cleanup that gets the order wrong usually deletes something unique or keeps asking for permission it already has.

## 1. Judge Value from Role, Not from Appearance

Decide from the item's future uses, current consumers, uniqueness, frozen state, rebuild cost, and recovery evidence. Read the records that state its role (status, asset or version record, README, script, test, manifest) before judging it.

A name such as `tmp`, an old date, zero bytes, an ignore rule, or a hash shared with another file is not enough on its own to show that an item is disposable. Each of these has common counterexamples: a `tmp` folder that holds the only acceptance screenshot, an empty file that is a required boundary-case test input, a duplicate that carries a frozen submission name.

| Role | Default decision |
| --- | --- |
| Original source, raw input, or the only copy of acceptance evidence | Keep. Route it from its consumer if it is hard to find. |
| Reproducibility dependency: a script, configuration, lock file, or input that a current result needs | Keep, or promote it from scratch into the owning code or data area and update callers. |
| Submitted, published, or otherwise frozen baseline | Keep its exact bytes and path unless relocation was explicitly allowed. |
| Copy with the same bytes as another file but a distinct role (a required delivery name, a mirror that a client reads) | Keep both, or propose an alternative that preserves every role. A duplicate hash is a lead, not a verdict. |
| Live client state: application lock files, sync or upload state, files held by a running program | Leave in place. Suggest an ignore rule if it pollutes version control. |
| Regenerable output: caches, bytecode, renders or extractions with recorded inputs and a working rebuild command | Cleanup candidate once the rebuild conditions actually hold and no active consumer reads it. |
| Retired working copy whose bytes are recoverable from an exact commit or a verified backup | Cleanup candidate once recovery is confirmed and no live route points to it. |
| Residue of a failed operation (an empty or partial download, an aborted export) | Cleanup candidate, but keep the record that the operation failed. Removing the residue does not complete the operation. |
| Role, owner, or dependency still unknown | Keep, and name the evidence that would decide it. |

The existence of a newer version does not by itself mean an older one has no further value. Earlier revisions answer questions about past decisions, and reviewers sometimes need them.

## 2. Confirm Recovery Before Retiring Unique Bytes

Recovery evidence must cover the bytes that exist now.

- **Git.** A tracked path is not proof that its current content is saved. Compare the working file with the blob in the exact commit you intend to rely on, for example by hashing both. Uncommitted edits, ignored files, and untracked files are outside that proof. The commit must stay reachable, and the item's dependencies must be recoverable too.
- **Independent backup.** Where Git is unavailable or not used, a backup counts after it has been read back and compared with the current bytes. Record its location and what was compared.
- **No recovery route.** Keep the item, or ask the user to choose between keeping it and accepting its loss. Do not create a repository or a backup solely to make a deletion look safe unless the user asks for that.

## 3. Establish Authority Before Acting

Technical permission and user intent are separate facts. A client running with Full access, an unrestricted sandbox, or a writable directory shows that a deletion is possible, not that it is wanted.

- **Read the current instruction and standing rules first.** An instruction such as "judge and delete whatever is certainly unused in this project" authorizes deleting items within that project that pass the checks above. Act on it without asking again for the same items. Items that fail a check stay where they are and go into the report.
- **Keep operation classes apart.** Authority to archive is not authority to delete. Authority to list candidates is not authority to remove them. A Git automation preference such as automatic local commits never extends to deleting files.
- **Respect the scope of standing preferences.** If the workspace records an automatic-maintenance preference, use only its stated scope, operation classes, exclusions, and expiry. Authority granted for one project or one directory does not transfer to another.
- **The latest instruction wins.** If the user narrows or withdraws authority, apply the new scope before the next write, even if an earlier message was broader.
- **Remember decisions to keep.** When the user has decided to keep an item, do not raise it again unless its identity, its dependencies, or the applicable rules change.

Never record an approval that the user did not give, and never widen a recorded approval to fit the work.

## 4. Tell the User What Needs a Decision

When an action needs a decision the user has not made, finish the authorized and independent work first, then present one consolidated request in the conversation:

- the exact candidates (paths, or a precise pattern with a count);
- why each one appears disposable, and the evidence;
- size or scope;
- how each could be recovered afterwards, or that it could not;
- what remains uncertain and what evidence would settle it.

A candidate list written only into a file the user may never open does not count as telling them. Keep the item in the persisted handoff as awaiting a decision so that a later session neither forgets it nor repeats a request that has already been answered.

## 5. Execute an Exact Plan

1. Write down the exact set: paths, file types, current identities (a hash for unique, frozen, or consequential items; size and count for regenerable caches), the role and reason, and the recovery source.
2. Immediately before acting, and again before each item, recheck the boundary, the current identity, user edits since the plan, links and Windows reparse points, and live consumers. An item whose identity changed leaves the plan and is reassessed.
3. Do not delete a directory as a whole while any child is unclassified. Do not use a broad wildcard or a recursive delete on a mixed folder, and do not follow links out of the scope.
4. Never remove Git metadata, repository history, lock files, or client state as part of cleanup.
5. Update live references (indexes, scripts, configuration) before removing their target, so that no current route points to nothing.
6. Afterwards, confirm that the removed set equals the planned set, that the identities of retained key items are unchanged, and that live routes still resolve. Report partial completion as partial.
7. Leave historical records in their original wording. Explain a retired path with a dated history note or a move map instead of rewriting old snapshots.

If work is interrupted, keep the record of what was done and what was not. On resume, reassess the remaining items from scratch. A new file that now sits at a planned path is a new item, not the one that was approved.

Routine maintenance of a few items needs no special tooling. Keep the plan and the result in the existing status or audit record, and create a separate ledger only when a batch is large enough to need one.

## 6. Close Each Affected Scope

Resolve every scope that maintenance touched to exactly one outcome:

| Outcome | Meaning | Record |
| --- | --- | --- |
| Applied | Changed and verified within authority | the action and how it was verified |
| Retained | The existing state is still right | the reason |
| Awaiting decision | A specific user decision is needed | the question as put to the user, and the candidates |
| Blocked | A stated condition prevents action | the condition that would clear it |

Persist an outcome only when it leaves durable work behind, such as a pending decision or a blocker. A healthy check with nothing to do creates no file.

A clean Git working tree answers a different question. It says that tracked changes are committed. It does not say that ignored or untracked material was classified, that unique evidence is safe, or that clutter was resolved. Do not report maintenance as complete on the strength of a clean tree or a shorter startup file.
