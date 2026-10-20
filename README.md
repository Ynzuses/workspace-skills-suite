# Workspace Skills Suite

Durable project memory, authority and directory design, resumable handoffs and separately authorized Git closeout.

**项目工作区与版本管理**：适用于软件、写作、运营和科研项目的工作区记忆、目录与权威管理、会话恢复及 Git 收尾。

适合软件、写作、运营及科研等持续项目：整理唯一维护来源、恢复上下文、建立交接，或在明确授权下完成整个仓库的 Git 收尾。

## 包含哪些 Skills

| Skill | Purpose |
| --- | --- |
| [manage-workspace-memory](manage-workspace-memory/SKILL.md) | Project authority and directory design, progressive memory, three-hop recovery, capability routing and resumable handoff. |
| [git-workspace-closeout](git-workspace-closeout/SKILL.md) | Whole-worktree snapshots and optional single-branch pushes under separate persistent local and remote consent. |

## 通过 skills.sh 安装

正式 `v1.0.0` 发布后，在需要使用的项目根目录执行：

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

这会为 Codex 安装本组成员，默认仅当前项目。先查看成员可加 `--list`；跨项目使用可加 `--global`。可改用 `--skill <成员名>` 只选一项，或将 `--agent codex` 换成 `--agent claude-code` 等 CLI 支持的目标。首次使用保留交互选择；遇到符号链接限制可加 `--copy`。

完整的前置条件、固定版本、单项安装、部署路径、依赖、升级与卸载见 **[INSTALL.md](INSTALL.md)**。安装文件不等于目标代理已发现或实际调用了 Skill；请按指南核对。

## 使用示例

> 使用 $manage-workspace-memory，读取现有规则和状态，核对源码权威与目录，再更新本次任务的恢复入口。

> 使用 $git-workspace-closeout，先只读检查当前仓库的策略和状态；仅询问缺失的本地快照、远程推送选择，暂不提交。

以上是发给代理的任务示例。Codex 支持 `$skill-name` 显式指定；其他代理使用其自身调用方式。

## 环境与范围

记忆管理可在没有 Git 的项目中使用。Git 助手需要 Python 3.10+、Git 和 Bash；Windows 可使用 Git for Windows 提供的 Bash。首次策略选择与权限边界见下文及安装指南。

Skill 通过代理调用运行，不是后台自动提交服务。策略授权、Skill 是否被调用及工具是否允许执行是三个独立条件。

## Git 策略与运行权限

首次**调用仓库级收尾**时，会读取该物理仓库的现有规则和已保存策略；仅询问缺失的选择。本地快照与远程推送分别可选 `off`、`ask`、`auto`。`auto` 复用已授权范围，`ask` 每次确认具体计划；安装本身不建立策略，也不启用后台服务。

已有明确项目约定可被复用。仅暂存/提交本任务文件属于任务级操作，不是本 Skill 的仓库级收尾入口。因此，某次提交未询问，单凭这一点不能判断 Skill 失效或自动策略已生效。可用只读 `policy-show`、`session-status` 核对；详见 [安装与诊断](INSTALL.md#git-首次选择与诊断)。

受限客户端可能保护 `.git`。优先使用客户端允许的具体命令审批或经授权的单仓库权限配置；无法提供这些机制而又要求无人值守写入时，可能需要用户选择 Full access。它会扩大文件和网络访问范围，不代表同意提交、推送或公开。Skill 不更改权限设置；详见 [权限说明](git-workspace-closeout/references/permissions.md)。

## 版本、帮助与许可

`1.0.0` 是本组首个稳定契约版本。迁移旧安装请读 [MIGRATION.md](MIGRATION.md)；本版内容见 [RELEASE_NOTES.md](RELEASE_NOTES.md)。兼容边界见 [STABILITY.md](STABILITY.md)，验证范围见 [VALIDATION.md](VALIDATION.md)。

按任务可组合其他组：`research-skills-suite`, `office-authoring-suite`。这些均为独立发行，不会随本组自动安装。报告问题时附代理/CLI 版本、复现步骤、错误和合成示例；请移除凭据、个人数据和未发表材料。

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE)。来源与保留条款见 [NOTICE](NOTICE)、[PROVENANCE.md](PROVENANCE.md)。
