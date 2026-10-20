# Long sessions, checkpoints and recoverable closure

## Track an active task

Once the repository's choices are saved, use `session-start "<stable-task-id>"`. It stores the active task and starting HEAD privately in the worktree's Git directory. On later sessions read `session-status` alongside the saved policy. Do not replace a pending different task with a new one; first recover its verified, blocked or waiting state.

With explicit project-integration authorization, `install-routing --evidence "<actual instruction>"` appends one managed Git startup/closure route to `AGENTS.md`. Existing unrelated bytes remain unchanged, an identical repeat is a no-op, and a different/partial managed block stops for review. It does not install a hook, watcher, timer or service. Do not silently add repository governance just because the user asked for one commit.

## Invoke at durable boundaries

Keep a `Git closeout pending` item in the active task immediately when persistent work starts. Evaluate it:

- after a meaningful phase is verified, when a recoverable checkpoint is useful;
- before context compaction, a planned pause, or handing work to the next session;
- after final memory/index updates and before the final response;
- at the next startup when a prior pending record is found.

A checkpoint follows the same local and remote consent modes as final closure. Under `auto`, do not repeat the preference question. Under `ask`, wait for a current action approval. Under `off`, accurately record that no action was wanted. Phase boundaries do not authorize committing half-finished changes belonging to a different task in a shared directory.

## Verify both channels separately

Local success requires the intended commit and independent worktree inspection. Remote success requires the bound target reference to match the exact sent commit. Local success leaves a remote-enabled workflow in `remote_due`; remote verification clears that phase. Failed commands retain a blocked record when it can be written. If metadata protection prevents even the private record, report that persistence gap and carry it in an authorized task handoff instead of inventing durable state.

Do not call a clean worktree proof that all task outputs were committed: files may be ignored or outside the repository. Compare the intended output set and exclusions with the snapshot. Before the final response, call `session-finish`: it detects a missed local commit or outstanding remote update instead of silently marking the task closed. With both modes off, it closes the task as intentionally uncommitted. A long session should finish with explicit outcomes for local, remote and remaining work; `awaiting confirmation` and `blocked` are valid states, not success.

One invocation creates at most one commit. If new changes arrive during/after it, report them. Only run another checkpoint under its own current policy and plan; do not create an unbounded background loop or repeatedly capture another session's live output.

## Limits

This is active-session maintenance. A forced shutdown, crash, cancelled turn or missed invocation can prevent closure. Private pending state and a discoverable project rule make the next active turn recoverable; they are not an always-running enforcement mechanism. Stronger host-level hooks or supervised automation require a separate reviewed installation and the same consent gates.
