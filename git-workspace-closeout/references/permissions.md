# Client permissions and bounded recovery

User consent controls **whether** the action is wanted. Sandbox/approval policy controls **whether the command can run**. Keep both checks: a saved automatic preference does not grant OS access, and Full access does not grant publication consent.

**Full access is not required by this Skill.** A local commit needs writable Git metadata; a remote push additionally needs permitted network access and working host authentication. Default workspace file access alone can leave `.git` read-only, so policy persistence, staging and committing can fail even when editing ordinary files succeeds. An allowed approval for the same command or a separately authorized narrow configuration can provide the missing access without removing every sandbox boundary.

Clients express these controls differently. The sections below cover Codex named permission profiles and Claude Code permission rules and modes. For another client, read its current permission documentation and apply the same principles: approve the same bounded command, keep pushes separately gated, and never widen access silently.

## Codex

### Existing verification: reuse before repeating

The source-side verification record dated **2026-10-15** reports a macOS ordinary-repository test with **Codex CLI 0.162.0-alpha.17.2**. The built-in `:workspace` profile rejected `.git/index.lock` writes. A named profile extending `:workspace`, granting only that repository's actual Git directory write access, retaining `.codex`/`.agents`/`.aws` read-only, and disabling network allowed the helper to save policy and create a one-file commit. Independent Git status was clean; protected-directory writes, an owned file outside the workspace, and a loopback bind remained blocked. Those sandbox commands did not use Full access.

This is inherited, dated test evidence, not a new test of every receiver. Native Windows, linked worktrees, managed policies, actual approval services and an IDE's automatic selection of the profile were not established by that experiment. Check client support and the effective profile before promising unattended operation. The public package contains the reusable method, not the original machine's private configuration.

### Diagnosis and next action

1. Resolve the physical root and actual Git metadata path, including linked worktrees. Read the current environment's permission/approval instructions; never assume an elevation tool exists.
2. Under Codex's default `workspace-write`, `.git` and resolved Git pointer targets are protected as read-only. Extra writable roots do not, by themselves, prove Git metadata is writable. Do not use an `os.access` result as proof that the enclosing sandbox permits writes.
3. Attempt only the already authorized bounded operation through the available tool. If it reports a metadata permission boundary, use that tool's permitted command-specific authorization for the **same command**, if available. This is an execution permission request; explain that it does not reopen the saved local/remote choice.
4. If the policy forbids escalation or offers none, stop that mutation and report the exact permission gap. Re-running in the same sandbox, a retry shell, manual staging, another program or moving metadata cannot solve an intentional restriction. Never route around a review rejection.
5. A service timeout is different from a denial. Inspect whether Git started and whether the effect happened; an allowed transient tool request may be retried at most twice after checking state. A explicit denial is not transient. The compatibility retry script no longer blindly loops on exit 77.

For users who want fewer platform interruptions, explain the client's supported bounded command approval/rule options. A trusted wrapper rule must bind the audited entrypoint and relevant scope; never suggest blanket permission for `git`, `bash` or `python`. Do not install any rule, hook or permission setting without concrete authorization.

### Authorized alternative: a workspace profile with one Git directory writable

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

## Claude Code

Claude Code separates **permission rules** from **permission modes**. Rules in its settings files (`permissions.allow`, `ask`, and `deny`) are evaluated deny first, then ask, then allow, and the first match decides: a matching ask rule prompts even when a narrower allow rule also matches. The mode decides what happens to calls that no rule settles. Its documentation lists `.git` among the protected paths: such writes are prompted in Manual and `acceptEdits` modes, reviewed by a classifier in auto mode, denied in `dontAsk`, and allowed without a prompt only in `bypassPermissions`. Shell commands such as `git commit` go through the Bash or PowerShell permission flow; the documentation does not state that the protected-path rule applies to them, so check the current behavior rather than assuming either way.

Where the sandbox matters:

- **Native Windows.** Claude Code runs shell commands unsandboxed there. There is no Git-directory profile to configure; whether a closeout command runs is decided by the rules and the mode. A user who wants client-level control keeps or adds rules; nothing else bounds the command.
- **macOS, Linux, and WSL2 with the sandbox enabled.** Sandboxed commands may write inside the working directory, but `hooks` and `config` inside `.git` stay write-denied, and in a linked worktree the shared `.git` is writable apart from those two entries. A commit that touches neither can run; a step that must change Git configuration cannot. Network access goes through a host allowlist that starts empty, so a push needs its remote host allowed, or it falls back to the mode's handling of non-allowed hosts.

With an explicit request to reduce prompts, prefer a narrow rule over a broader mode:

```json
{
  "permissions": {
    "allow": ["Bash(python \"/absolute/path/to/skill/scripts/git_closeout.py\" commit *)"],
    "ask": ["Bash(git push *)", "PowerShell(git push *)"]
  }
}
```

Rules match command text, so mind what they cannot see. An ask rule for `git push *` does not match a push that the helper performs from inside Python, nor a form such as `git -C . push`. Allow-listing the helper as a whole (`.../git_closeout.py *`) therefore also pre-approves its `push` subcommand at the client level; keep the allow rule on the local subcommand if client prompts for pushes are wanted. The helper's own remote-consent gate applies in every case. Put the rule in the project's local or shared settings file as the user chooses, preserve existing rules and managed settings, and verify the effect in a disposable repository first.

An auto-mode classifier approval is a client safety review, not the user's consent: a saved `off` or `ask` remote mode still governs. `bypassPermissions` removes prompts, including for protected-path writes, and carries the same risks as Full access below; the client's own documentation reserves it for isolated environments.

Dated observation, not a test of the helper: during this suite's 1.1.0 maintenance on native Windows 11 with the Claude Code VS Code extension (no sandbox available), ordinary `git add` and `git commit` from the agent's shell tools wrote Git metadata with no profile or extra configuration, while a project ask rule for `git push` and `gh` prompted as configured. The helper's unattended commit path, linked worktrees, the macOS and Linux sandbox, and managed settings were not tested under Claude Code.

## When Full access may be required

If neither a supported, authorized narrow profile nor a suitable command-level permission mechanism is available, unattended Git metadata writes may require the user to choose Full access in their client, where allowed. Do not claim that every client requires it, nor that it fixes all Git failures.

Full access removes filesystem and network sandbox boundaries. Commands, untrusted repository code and hooks may read/modify unrelated assets or access services. Repository checks, approval modes and backups remain necessary, but instructions are not a replacement for system isolation. The skill never changes permissions itself, never enables a bypass mode and never broadens the task after a user changes permissions.

For a managed client, administrator requirements still apply. If Full access is forbidden, report that limitation; do not change requirements or other configuration. With platform approval configured as never and protected metadata remaining read-only, there is no legitimate automatic escalation to invent.

## Evidence and limitations

These official pages were checked on the dates shown; current client policy and CLI flags must still be inspected:

- [OpenAI: Permissions](https://learn.chatgpt.com/docs/permissions) (2026-10-21): named profiles, inheritance, exact-path overrides, configuration precedence and managed restrictions.
- [OpenAI: Sandbox](https://learn.chatgpt.com/docs/sandboxing) (2026-10-21): filesystem/network boundaries, approval policy, command exceptions and Full access risks.
- [OpenAI: Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) (2026-10-21): protected `.git` paths, pointer targets, interactive approvals and administrator controls.
- [OpenAI: Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) (2026-10-21): separate sandbox/approval controls and configuration constraints.
- [Claude Code: Configure permissions](https://code.claude.com/docs/en/permissions) (2026-11-11): rule syntax, deny-ask-allow evaluation, wildcard matching and what Bash rules cannot see.
- [Claude Code: Permission modes](https://code.claude.com/docs/en/permission-modes) (2026-11-11): modes, protected paths including `.git`, and the VS Code extension's default mode.
- [Claude Code: Sandboxing](https://code.claude.com/docs/en/sandboxing) (2026-11-11): supported platforms, write scope and protected `.git` entries, network allowlist.

A Skill cannot guarantee that a platform reviewer will approve a command or that every future agent turn invokes the closeout flow. Do not advertise reliable unattended commits in a restricted client until that client's permitted execution path is actually tested.
