# v1.0.0 — Workspace Skills Suite

Durable project memory, authority and directory design, resumable handoffs and separately authorized Git closeout.

本组首个稳定版本，面向「项目工作区与版本管理」。适合软件、写作、运营及科研等持续项目：整理唯一维护来源、恢复上下文、建立交接，或在明确授权下完成整个仓库的 Git 收尾。

## 本版提供

- `manage-workspace-memory`
- `git-workspace-closeout`

按用途独立安装；其他产品组是可选组合。记忆管理可在没有 Git 的项目中使用。Git 助手需要 Python 3.10+、Git 和 Bash；Windows 可使用 Git for Windows 提供的 Bash。首次策略选择与权限边界见下文及安装指南。

## 安装

```sh
npx skills@1.7.4 add https://github.com/Ynzuses/workspace-skills-suite/tree/v1.0.0 --skill "*" --agent codex
```

默认项目范围，跨项目加 `--global`，仅选一项用 `--skill <成员名>`。先核对 Node/npm/Git 与现有安装；完整部署、依赖和卸载见 [安装指南](INSTALL.md)。

本地整仓快照与远程推送分别选择 `off/ask/auto`，仅询问缺失选择。已有明确项目授权可复用；任务级提交不属于整仓收尾。受限客户端可能需要具体审批或经授权的权限配置；Full access 仅在适用条件下考虑，不能代替操作授权。详见安装指南的 Git 诊断与权限部分。

## 从旧版本迁移

见 [MIGRATION.md](MIGRATION.md)。旧版与旧标签保留；升级不会自动卸载旧安装、安装其他组或迁移本地设置。`1.0.0` 标记首个稳定契约，内部审阅轮次不进入正式版本号。

## 验证与限制

Skill 通过代理调用运行，不是后台自动提交服务。策略授权、Skill 是否被调用及工具是否允许执行是三个独立条件。 适用的结构、脚本和入口检查见 [VALIDATION.md](VALIDATION.md)；未来代理自动触发、真实应用验收和外部连接不由静态检查保证。

## 下载与校验

自定义资产：`workspace-skills-suite-1.0.0.zip`，配套 `workspace-skills-suite-1.0.0.zip.sha256`。解压后含逐文件 `SHA256SUMS` 和 `RELEASE_MANIFEST.json`。GitHub 的 Source code 归档由标签树自动生成，与自定义 ZIP 的字节和打包清单不同。

Windows 可用 `Get-FileHash <zip路径> -Algorithm SHA256`，macOS 用 `shasum -a 256 <zip路径>`，Linux 用 `sha256sum <zip路径>`，对照配套校验值。签名、平台收录和原生应用验收均只在实际完成后声明。

Copyright 2026 Ynzuses. [Apache-2.0](LICENSE)，保留条款见 [NOTICE](NOTICE)。
