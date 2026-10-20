# Workspace Skills Suite 安装与部署

本指南使用 [skills.sh](https://skills.sh/docs/cli) 背后的 Vercel `skills` CLI。命令按 `skills@1.7.4` 固定；产品版本为 `v1.0.0`，两者独立。远程命令在该仓库及标签正式发布后使用；发布前可用下述本地目录方式。

## 1. 准备环境与检查已有安装

CLI 1.7.4 要求 Node.js **22.20.0 或更新版本**，并需要 npm/npx；Git 来源安装还应准备 Git 和对应网络访问。先运行：

```sh
node --version
npm --version
git --version
npx skills@1.7.4 list --agent codex
npx skills@1.7.4 list --agent codex --global
```

首次 npx 可能询问是否下载 CLI。检查是否已有同名 Skill，尤其是手工安装、插件和旧目录中的副本；不要盲目覆盖本地修改。CLI 默认安装到项目，安装时的当前目录应为目标项目根目录。

## 2. 先查看，再安装

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --list
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

本组应发现 **2** 项：`manage-workspace-memory`, `git-workspace-closeout`。`--skill "*"` 表示本组所有成员；不用 `--all`，以免扩大到所有代理。保留交互提示以检查目标和安装方法。

只安装一项，或安装到用户范围：

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill manage-workspace-memory --agent codex
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex --global
```

`--global` 跨项目使用；省略它仅安装到当前项目。PowerShell 和常见 Unix shell 均保留双引号包围星号。命令中的 `/tree/v1.0.0` 选择 Git 标签；不要把 `@1.0.0` 当作产品标签写在仓库简写后，`@` 在 CLI 来源语法中还用于选择 Skill。

## 3. 选择代理、链接或复制

| 目标 | 参数 | 项目目录 | 用户目录 |
| --- | --- | --- | --- |
| Codex | `--agent codex` | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `--agent claude-code` | `.claude/skills/` | `~/.claude/skills/` |

其他目标以 [CLI 当前支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) 为准。宿主暴露的 Skill 根目录可能因版本、插件或旧安装而异；本表不证明某个客户端已加载该位置。

CLI 支持符号链接和复制。Windows 无法创建链接时，加 `--copy` 复制完整目录；无需仅为复制 Skill 开启完全访问权限。经过核对的无人值守安装可加 `--yes`，它只跳过安装器的提示，不授予 Git 提交、网络服务连接或公开权限。保留每项 Skill 的 `SKILL.md` 与全部配套子目录。

## 4. 离线文件或发布 ZIP

下载本版自定义 Release 资产 `workspace-skills-suite-1.0.0.zip`，按配套 `.sha256` 校验并解压；或使用固定标签的完整 checkout。不要把仓库整体当作一个 Skill。把以下示例路径换成解压后的组目录：

```sh
npx skills@1.7.4 add "./workspace-skills-suite" --list
npx skills@1.7.4 add "./workspace-skills-suite" --skill "*" --agent codex --copy
```

在目标项目根目录运行，使用正确的相对或绝对源路径。此方式不需要访问产品远程仓库，但首次下载 CLI 仍需 npm 网络；完全离线应预先准备受信任的 CLI 缓存，或手动复制完整成员目录到宿主实际发现路径。

自定义资产含 `SHA256SUMS` 与 `RELEASE_MANIFEST.json`；GitHub 自动生成的 Source code ZIP 内容相同于标签树，但不承诺包含这两个打包时生成的文件。

## 5. 运行依赖

记忆管理可在没有 Git 的项目中使用。Git 助手需要 Python 3.10+、Git 和 Bash；Windows 可使用 Git for Windows 提供的 Bash。首次策略选择与权限边界见下文及安装指南。

CLI 安装成员目录，不会执行 pip、安装 Office、连接账号或复制组根目录的 support kit。需要组级依赖文件和测试时保留完整 checkout/解压目录。各任务仍按实际可用工具选择执行路径。

## Git 首次选择与诊断

在代理中明确要求：

> 使用 $git-workspace-closeout，只读检查当前物理仓库的策略与状态。读取已有明确约定，只询问缺失的本地快照/远程推送选择；暂不提交或推送。

| 渠道 | `off` | `ask` | `auto` |
| --- | --- | --- | --- |
| 本地整仓快照 | 不创建快照 | 每次批准具体计划 | 在已保存范围内审阅后执行 |
| 远程单分支推送 | 不发送 | 每次单独批准推送计划 | 仅向已绑定并审阅的目标执行 |

两项独立选择，缺失时需询问，不跨仓库继承。安装本身不写策略；已有明确授权只在原范围内复用。远程未配置时不能自动推送。`ask` 要等真实的本次答复；Full access、静默、安装器 `--yes` 均不是答复。

在目标仓库运行只读诊断，把 `<skill-dir>` 换成实际安装目录：

```sh
python "<skill-dir>/scripts/git_closeout.py" policy-show
python "<skill-dir>/scripts/git_closeout.py" session-status
python "<skill-dir>/scripts/git_closeout.py" audit
```

`policy: null` / `needs_initial_choices: true` 表示没有保存该仓库的策略；不会否认项目文件中可能存在的明确授权。`session: null` 表示当前没有该助手保存的活动会话，不能证明过去所有提交是否调用了 Skill。策略保存在该物理工作树的 Git 元数据中，不写入公开 Skill。

**为什么提交时可能没问？** 已保存 `auto` 或同范围明确项目约定可免重复询问；普通任务范围暂存/提交也不属于本 Skill 的整仓收尾。反之，新仓库没有选择、没有同范围授权，却由该 Skill 直接做整仓提交，属于需要排查的问题。依次核对代理是否实际读取 Skill、上述策略/会话输出及操作范围，不只看“文件已安装”。

### 何时涉及 Full access

本地提交会写 Git 元数据。客户端若保护 `.git`，先检查实际 Git 目录、当前权限和允许的审批机制。可用时优先具体命令审批，或由用户单独授权并验证仅对该仓库 Git 目录开放写入的配置。若这些机制不可用且需要无人值守写入，可能需要用户在客户端选择 Full access；受管理环境仍服从管理员限制。

Full access 会扩大文件和网络访问，仓库代码、钩子及错误命令也可能影响其他资产；它不授权推送、建远程仓库或发布。Skill 不自动切换权限，也不能绕过拒绝。具体配置与适用限制见 Skill 的 `references/permissions.md`，以及 [OpenAI 权限文档](https://learn.chatgpt.com/docs/permissions)。

## 6. 确认已发现并实际调用

```sh
npx skills@1.7.4 list --agent codex
```

用户范围安装则加 `--global`。然后在目标代理的可用 Skill 列表核对成员，显式调用 `$manage-workspace-memory` 做一个无外部副作用的小任务，并确认代理读取了对应 `SKILL.md`。Codex 会检测 Skill 变更；若未出现，按宿主说明刷新或重启。安装器列表成功不等于应用已发现，更不等于工作流行为已验证。

缺项时先核对安装范围、工作目录、代理参数、文件是否完整及同名旧副本。项目级 `.agents/skills` 若随项目共享，应审阅差异；个人环境目录和运行凭据不应加入公开仓库。

## 7. 更新、回退与卸载

```sh
npx skills@1.7.4 check
npx skills@1.7.4 remove manage-workspace-memory --agent codex
```

用户范围卸载加 `--global`。仅移除指定成员，不使用清空全部 Skill 的参数。`check` 用于查看上游状态，不证明目标版本兼容。固定标签安装要升级时，先审阅新版本说明，再对新的 `/tree/vX.Y.Z` 显式执行同范围 `add`；保留旧版 ZIP/锁文件和本地修改，便于回退。跟踪分支安装的用户可在审阅后运行 `npx skills@1.7.4 update <成员名> --project` 或 `--global`；不要把自动更新当作保持固定版本。

## 隐私、许可与更多帮助

CLI 是独立第三方工具。其 [故障排查与遥测说明](https://github.com/vercel-labs/skills/blob/main/docs/troubleshooting.md) 提供 `DISABLE_TELEMETRY=1` / `DO_NOT_TRACK=1` 选项；使用前按自己的环境选择。它们不表示 npm 下载或 Git 来源获取离线。

本组 [Apache-2.0](LICENSE)；组件条款见 [NOTICE](NOTICE) 与 [PROVENANCE.md](PROVENANCE.md)。安装命令与选项依据 [Vercel CLI 文档](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)，核对日期 2026-10-20。Skill 的适用范围和示例见 [README.md](README.md)。
