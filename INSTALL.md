# Workspace Skills Suite: installation and deployment

This guide uses the Vercel `skills` CLI behind [skills.sh](https://skills.sh/docs/cli). Commands pin the installer to `skills@1.7.4`; the product tag is `v1.0.0`. These are independent versions. Remote commands require the repository and tag to have been published. Before that, use the local-directory route below.

## 1. Prepare the environment and inspect existing installations

CLI 1.7.4 requires **Node.js 22.20.0 or later** and npm/npx. For Git-source installs, prepare Git and access to the source host. Check:

```sh
node --version
npm --version
git --version
npx skills@1.7.4 list --agent codex
npx skills@1.7.4 list --agent codex --global
```

The first npx run may ask to download the CLI. Inspect existing Skills with the same names, including manual, plugin, and legacy-directory installations. Preserve local changes before replacing an entry. The CLI defaults to project scope; run it from the intended project root.

## 2. Inspect members, then install

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --list
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

Expect **2** members: `manage-workspace-memory`, `git-workspace-closeout`. `--skill "*"` selects this group's members. Avoid `--all` here because it also selects all agents. Review the destination and installation method in the interactive prompts.

To select one member or install the group for your user account:

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill manage-workspace-memory --agent codex
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex --global
```

`--global` makes the installation available across projects; omitting it selects the current project. Keep double quotes around the star in PowerShell and common Unix shells. `/tree/v1.0.0` selects the Git tag. Do not append `@1.0.0` to a repository shorthand to mean a product version: the CLI also uses `@` to select a Skill.

## 3. Choose an agent and installation method

| Target | Option | Project directory | User directory |
| --- | --- | --- | --- |
| Codex | `--agent codex` | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `--agent claude-code` | `.claude/skills/` | `~/.claude/skills/` |

See the [supported-agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) for other targets. Discovery roots can differ with host versions, plugins, or legacy installations; a directory in this table is not proof that a particular client loaded it.

The CLI supports symbolic links and copies. Add `--copy` when links are unavailable, including on restricted Windows setups. Copying Skill files does not itself require Full access. After reviewing the intended installation, `--yes` can skip installer prompts; it does not authorize Git commits, account connections, or publication. Keep each complete Skill directory, including its supporting files.

## 4. Use a release ZIP or local checkout

Download `workspace-skills-suite-1.0.0.zip`, verify it against the companion `.sha256` file, and extract it. A complete checkout of the fixed tag also works. Install the member directories rather than treating the whole repository as one Skill. Replace this example with the actual extracted group directory:

```sh
npx skills@1.7.4 add "./workspace-skills-suite" --list
npx skills@1.7.4 add "./workspace-skills-suite" --skill "*" --agent codex --copy
```

Run from the target project root and use the correct relative or absolute source path. This avoids fetching the product repository, but obtaining the CLI through npm can still require a network connection. For fully offline use, prepare a trusted CLI cache in advance or manually copy complete member directories to the host's verified discovery root.

The custom asset contains `SHA256SUMS` and `RELEASE_MANIFEST.json`. GitHub's automatically generated Source code archives reflect the tagged tree and do not promise to include these packaging-generated files.

## 5. Prepare runtime dependencies

Memory management works without Git. The Git helper requires Python 3.10+, Git, and Bash. On Windows, Git for Windows supplies Bash. See the policy and permission guidance below before using repository-wide closeout.

The CLI installs member directories. It does not run pip, install Office, connect accounts, or copy group-root support kits. Retain the full checkout or extracted group when using root-level requirements files and test kits. Select execution tools from the actual task environment.

## Git first use and diagnosis

Ask the agent explicitly:

> Use $git-workspace-closeout to inspect this physical repository's policy and status read-only. Read existing explicit instructions, ask only for missing local-snapshot and remote-push choices, and do not commit or push yet.

| Channel | `off` | `ask` | `auto` |
| --- | --- | --- | --- |
| Repository-wide local snapshot | Do not create a snapshot | Approve each concrete plan | Review and execute within the saved scope |
| Single-branch remote push | Do not transmit | Separately approve each push plan | Execute only to the bound, reviewed destination |

Choose the channels independently. Ask for missing choices and do not inherit them across repositories. Installation does not save policy. Reuse existing explicit authorization only within its original scope; unconfigured remote operation cannot become automatic. `ask` requires a real current reply. Full access, silence, and installer `--yes` do not provide that reply.

From the target repository, run these read-only commands after replacing `<skill-dir>` with the actual installed directory:

```sh
python "<skill-dir>/scripts/git_closeout.py" policy-show
python "<skill-dir>/scripts/git_closeout.py" session-status
python "<skill-dir>/scripts/git_closeout.py" audit
```

`policy: null` and `needs_initial_choices: true` mean no policy is saved for that repository; explicit project-file authorization may still exist. `session: null` means no active helper session is saved and does not establish how every historical commit was made. Policy stays in that physical worktree's Git metadata, not in the public Skill.

**Why might a commit happen without another question?** A saved `auto` choice or an explicit standing instruction may already cover the action. Ordinary task-scoped staging or committing is also outside this Skill's repository-wide closeout. In contrast, a new repository with no choices or applicable authorization should not receive an automatic whole-worktree commit through this Skill. Check actual Skill loading, policy/session output, and operation scope rather than relying on installed files alone.

### When Full access may matter

Local commits write Git metadata. If a client protects `.git`, inspect the actual Git directory, effective permissions, and allowed approval mechanism. Prefer an available command-specific approval or a separately authorized and tested profile that grants write access to one repository's Git directory. If neither is available and unattended writes are required, the user may need to choose Full access in that client. Managed environments retain their administrator requirements.

Full access broadens file and network access. Repository code, hooks, and mistaken commands can affect unrelated assets. It does not authorize pushes, remote-repository creation, or publication. The Skill neither changes permissions automatically nor bypasses denials. Read its `references/permissions.md` and the [OpenAI permissions documentation](https://learn.chatgpt.com/docs/permissions) before reviewing any configuration.

## 6. Verify discovery and invocation

```sh
npx skills@1.7.4 list --agent codex
```

Add `--global` for a user-wide installation. Then inspect the target agent's available Skills and explicitly invoke `$manage-workspace-memory` for a small task without external side effects. Confirm that the agent read the expected `SKILL.md`. Codex detects Skill changes; refresh or restart according to the host's instructions if an entry does not appear. Installer output does not prove agent discovery or correct workflow behavior.

If an entry is missing, inspect scope, working directory, agent selection, complete files, and duplicate legacy entries. Review project-level `.agents/skills` changes before sharing them. Keep personal runtime directories and credentials out of public repositories.

## 7. Update, roll back, or remove

```sh
npx skills@1.7.4 check
npx skills@1.7.4 remove manage-workspace-memory --agent codex
```

Add `--global` when removing a user-wide installation. Remove only the intended member. `check` inspects upstream state; it does not establish compatibility. For a pinned tag, review the new release, then explicitly run `add` against its new `/tree/vX.Y.Z` URL using the same scope. Retain the previous ZIP, lock file, and local changes for rollback. Branch-tracking users can review and run `npx skills@1.7.4 update <skill-name> --project` or `--global`; automatic updates are not a version pin.

## Privacy, license, and help

The CLI is a separate third-party tool. Its [troubleshooting and telemetry documentation](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md) describes `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1`; choose according to your environment. These settings do not make npm or Git downloads offline.

This group uses [Apache-2.0](LICENSE), with retained terms in [NOTICE](NOTICE) and [PROVENANCE.md](PROVENANCE.md). Commands follow the [Vercel CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md), checked on 2026-10-20. See [README.md](README.md) for scope and examples.
