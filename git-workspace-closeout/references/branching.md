# Branch decisions relevant to closeout

Use ordinary commits for a single sequence of accepted corrections, indexes, different deliverables that must coexist, or selecting an earlier finished file. File versions, topic counts and session changes do not themselves require branches.

Consider a separate topic/experiment branch when alternative solutions need to evolve independently, or when unverified changes must be isolated from an accepted baseline. Use distinct worktrees if both routes need simultaneous editing; branch names alone do not isolate a shared directory.

A branch at an old commit starts from the whole tracked repository snapshot. For one document in a multi-task repository, starting from the current baseline and restoring only that document plus compatible dependencies often preserves unrelated progress better. This skill does not perform either branch switching or restoration automatically.

Freeze submitted/circulated artifacts by exact identity and records. A Git tag marks a historical point but does not prove delivery, deployment or publication. DOCX/PPTX/images may require explicit selection, regeneration or native integration; a textual merge cannot establish their semantic correctness.

Closeout observes the current branch and saved scope. New branches, different worktrees or a different remote mapping require their own explicit scope; do not silently transplant policy records. Task-isolated staging and whole-worktree snapshots have different boundaries; this implementation handles the latter only.

Mechanism references: [Pro Git branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell), [workflows](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows), and [git worktree](https://git-scm.com/docs/git-worktree). These support the mechanics, not a universal mandatory branching strategy.
