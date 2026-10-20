# Git Workspace Closeout

A Git closeout Skill with durable, independent consent for local snapshots and optional remote pushes, maintained in Workspace Skills Suite 1.0.0. It requires Python 3.10+, Bash and Git. Start with [SKILL.md](SKILL.md).

## Choose once, remember per repository

Local commits and remote pushes each have three modes:

| Mode | Behavior |
| --- | --- |
| `off` | Do not perform this action |
| `ask` | Show a current plan and wait for affirmative approval every time |
| `auto` | Perform eligible actions within the saved scope without asking the same consent question again |

Neither channel enables the other. A one-time approval stays one-time. An explicit later preference change supersedes the saved choice; Full access never changes it. Missing preferences are resolved from actual user instructions and applicable rules, then requested once where still missing. They are never inferred from silence, an existing remote or this skill's author's local-only setup.

The private record is in the physical worktree's Git directory under `codex-closeout/`, outside tracked project content. Do not publish or transplant it. Remote consent binds one existing destination and one branch mapping; a different destination or branch is outside that grant. See [setup and consent](references/authorization.md).

## Codex permissions: read before enabling unattended automation

In the default `workspace-write` sandbox, `.git` metadata is protected as read-only. Writing normal project files does not ensure `git add` or `git commit` can succeed. Repeating the command does not remove this protection. Use an allowed, bounded command approval or trusted command rule. Where supported and explicitly requested, a named permission profile can retain workspace isolation while granting writes to **one verified repository's Git directory**; a local-only profile can keep network disabled. The [configuration example and verification procedure](references/permissions.md) explain beta support, legacy-setting conflicts, linked-worktree limits and the fact that this grants metadata writes to all executed commands.

**If your client/policy supports neither a suitable narrow profile nor a command-level permission path, and you want Git to run without platform prompts, you may need to select Full access yourself.** This removes filesystem and network sandbox boundaries and permits commands to reach unrelated files and services. Mistakes, malicious content or repository hooks can therefore affect assets outside the project. It is not a guarantee that Git will succeed: locks, identity, hooks, authentication and server rules can still fail.

Use a trusted, narrowly scoped workspace and suitable backups. The skill confines supported operations, checks roots and consent, retains hooks and locks, and prohibits destructive cleanup/history rewriting. These are workflow guardrails, not an OS sandbox. Its helper never enables Full access, changes client permissions, installs a watcher or approves itself. User-requested profile setup is a separate, reviewed configuration change. See [permission handling and official sources](references/permissions.md).

## What automation actually guarantees

The deterministic helper blocks an unapproved action unless the corresponding saved mode is `auto`, or a current single-action plan confirmation is supplied. Those arguments must reflect real user authorization; a shell helper cannot verify who gave a reply. Scope changes and concrete safety failures still stop automatic actions.

For long sessions, a private pending task record and an optional authorized `AGENTS.md` route support phase checkpoints and final/resumption checks. They reduce missed commits; they cannot guarantee execution after the agent is forcibly stopped or fails to invoke the skill. No always-running service is included.

## Supported scope and limits

Local snapshots cover the whole worktree, not a selected task subset. Branch creation/switching, history rewriting, remote setup, repository visibility changes and releases require separate workflows. Ordinary old-version selection and multiple deliverables do not themselves require branches.

Remote pushes update one explicit target branch without force or automatic tags. Before enabling them, review all baseline history and publication/redistribution rights. The helper then scans the baseline tree and each later commit; this is a credential-pattern guard, not a comprehensive privacy or license audit. It stops beyond 200 new commits, 10,000 distinct scanned blobs or a 64 MiB blob, and on submodule/symlink publication. Large or unusual repositories need a separately reviewed plan rather than quietly skipping checks. Git protocol does not reveal hosting visibility: the stored visibility is a user declaration, not an independently verified platform setting.

Run the [disposable-repository tests](scripts/test_git_closeout.py) to validate the helper in your environment. Hosting authentication, protected branches, current client permissions and real project hooks require their own checks. Installation or a local commit is not publication.
