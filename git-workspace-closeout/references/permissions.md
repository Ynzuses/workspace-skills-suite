# Codex permissions and bounded recovery

User consent controls **whether** the action is wanted. Sandbox/approval policy controls **whether the command can run**. Keep both checks: a saved automatic preference does not grant OS access, and Full access does not grant publication consent.

**Full access is not required by this Skill.** A local commit needs writable Git metadata; a remote push additionally needs permitted network access and working host authentication. Default workspace file access alone can leave `.git` read-only, so policy persistence, staging and committing can fail even when editing ordinary files succeeds. An allowed approval for the same command or a separately authorized project profile can provide the missing access without removing every sandbox boundary.

## Existing verification: reuse before repeating

The source-side verification record dated **2026-10-15** reports a macOS ordinary-repository test with **Codex CLI 0.162.0-alpha.17.2**. The built-in `:workspace` profile rejected `.git/index.lock` writes. A named profile extending `:workspace`, granting only that repository's actual Git directory write access, retaining `.codex`/`.agents`/`.aws` read-only, and disabling network allowed the helper to save policy and create a one-file commit. Independent Git status was clean; protected-directory writes, an owned file outside the workspace, and a loopback bind remained blocked. Those sandbox commands did not use Full access.

This is inherited, dated test evidence, not a new test of every receiver. Native Windows, linked worktrees, managed policies, actual approval services and an IDE's automatic selection of the profile were not established by that experiment. Check client support and the effective profile before promising unattended operation. The public package contains the reusable method, not the original machine's private configuration.

## Diagnosis and next action

1. Resolve the physical root and actual Git metadata path, including linked worktrees. Read the current environment's permission/approval instructions; never assume an elevation tool exists.
2. Under default `workspace-write`, `.git` and resolved Git pointer targets are protected as read-only. Extra writable roots do not, by themselves, prove Git metadata is writable. Do not use an `os.access` result as proof that the enclosing sandbox permits writes.
3. Attempt only the already authorized bounded operation through the available tool. If it reports a metadata permission boundary, use that tool's permitted command-specific authorization for the **same command**, if available. This is an execution permission request; explain that it does not reopen the saved local/remote choice.
4. If the policy forbids escalation or offers none, stop that mutation and report the exact permission gap. Re-running in the same sandbox, a retry shell, manual staging, another program or moving metadata cannot solve an intentional restriction. Never route around a review rejection.
5. A service timeout is different from a denial. Inspect whether Git started and whether the effect happened; an allowed transient tool request may be retried at most twice after checking state. A explicit denial is not transient. The compatibility retry script no longer blindly loops on exit 77.

For users who want fewer platform interruptions, explain the client's supported bounded command approval/rule options. A trusted wrapper rule must bind the audited entrypoint and relevant scope; never suggest blanket permission for `git`, `bash` or `python`. Do not install any rule, hook or permission setting without concrete authorization.

## Authorized alternative: a workspace profile with one Git directory writable

Recent Codex clients support named permission profiles. With an explicit request to configure Git permissions, prepare a project-specific profile instead of modifying the built-in `workspace-write` implementation. For an ordinary repository, this is an example for its trusted project `.codex/config.toml`:

```toml
default_permissions = "project-git-local"

[permissions.project-git-local]
extends = ":workspace"

[permissions.project-git-local.filesystem]
"/absolute/path/to/this/repository/.git" = "write"

[permissions.project-git-local.filesystem.":workspace_roots"]
".codex" = "read"
".agents" = "read"
".aws" = "read"

[permissions.project-git-local.network]
enabled = false
```

Replace the example path with the verified physical Git directory; never grant a home directory or every project's metadata. Review and preserve existing configuration. The explicit read rules retain the other protections across profile implementations. Network is disabled for this local-only example; remote work needs separately authorized network settings and remote consent.

Inspect the installed version and managed requirements first. Named permission profiles and legacy `sandbox_mode` / `sandbox_workspace_write` are alternative configuration systems; do not combine them in one session. A client-selected sandbox or managed requirements may determine the effective policy. Do not remove managed restrictions or silently migrate global settings. Select the profile in a supported client/new session and verify its effective behavior. Where supported, test with `codex sandbox -C "<repository>" -P project-git-local -- <command>`. Command-line overrides with quoted/dotted path keys can parse differently; prefer a reviewed TOML file or one complete inline profile table over splitting those keys across overrides.

For linked worktrees, inspect `git rev-parse --absolute-git-dir` and `git rev-parse --path-format=absolute --git-common-dir`. The pointer file and shared metadata need separate scope review; this ordinary-repository example is not a tested linked-worktree recipe. Do not recursively grant the parent repository just to make a worktree succeed.

Validate a disposable repository first: default profile rejects metadata writes, the selected custom profile permits an authorized snapshot, protected settings and an owned path outside the workspace remain unwritable, and network restrictions remain effective. Then verify the actual project operation independently. A filesystem grant allows **any executed command** to write that Git directory, including config, hooks and history; it is not a Git-subcommand allowlist. Existing hooks remain executable project code. This retains useful sandbox boundaries but does not make destructive Git actions safe or authorized.

This configuration is an explicit setup workflow, never an automatic reaction to a denied command. Do not launch a less restricted profile or nested agent to evade the active environment's prohibition.

## When Full access may be required

If neither a supported, authorized narrow profile nor a suitable command-level permission mechanism is available, unattended Git metadata writes may require the user to choose Full access in their client, where allowed. Do not claim that every client requires it, nor that it fixes all Git failures.

Full access removes filesystem and network sandbox boundaries. Commands, untrusted repository code and hooks may read/modify unrelated assets or access services. Repository checks, approval modes and backups remain necessary, but instructions are not a replacement for system isolation. The skill never changes permissions itself, never enables a bypass mode and never broadens the task after a user changes permissions.

For a managed client, administrator requirements still apply. If Full access is forbidden, report that limitation; do not change requirements or other configuration. With platform approval configured as never and protected metadata remaining read-only, there is no legitimate automatic escalation to invent.

## Evidence and limitations

These official pages were checked again on 2026-10-21; current client policy and CLI flags must still be inspected:

- [OpenAI: Permissions](https://learn.chatgpt.com/docs/permissions): named profiles, inheritance, exact-path overrides, configuration precedence and managed restrictions.
- [OpenAI: Sandbox](https://learn.chatgpt.com/docs/sandboxing): filesystem/network boundaries, approval policy, command exceptions and Full access risks.
- [OpenAI: Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security): protected `.git` paths, pointer targets, interactive approvals and administrator controls.
- [OpenAI: Config basics](https://learn.chatgpt.com/docs/config-file/config-basic): separate sandbox/approval controls and configuration constraints.

A Skill cannot guarantee that a platform reviewer will approve a command or that every future agent turn invokes the closeout flow. Do not advertise reliable unattended commits in a restricted client until that client's permitted execution path is actually tested.
