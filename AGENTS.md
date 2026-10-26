# Starbook Agent Handoff / 必读入口

> **这是所有新 Agent、AI 编程窗口和新开发会话的第一入口。**
>
> 在修改任何代码、数据库、部署配置或产品体验之前，必须先完成本文规定的阅读顺序。不要仅凭旧对话、文件名或局部代码猜测当前架构。

## 1. 当前项目身份

- Project: **Starbook / 星屿之书**
- Current version: **1.6.0**
- Production branch: **`main`**
- Production deploy: **GitHub Pages via GitHub Actions**
- Runtime backend: **Supabase Anniversary Bridge**
- Current Book: **星屿之书** (`8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`)
- Current product preset:
  - relationship: `romantic`
  - theme: `magic-celestial`
  - experience: `world-map`
- Current delivery priority: **2026-10-29 周年纪念版稳定交付**

## 2. Agent 必读顺序

任何新 Agent 在开始工作前，按顺序阅读：

1. `AGENTS.md` —— 当前文件，确认协作规则。
2. `PROJECT_STATE.md` —— 当前真实状态、技术债、已验证能力、下一优先级。
3. `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md` —— 项目管理、开发、发布、部署、数据、回滚全链路。
4. `docs/ARCHITECTURE_EXTENSION_CONTRACT.md` —— 当前架构边界与未来扩展不可破坏约束。
5. `docs/DATA_LIFECYCLE.md` —— Supabase 数据生命周期、版本升级与迁移规则。
6. `CHANGELOG.md` —— 已完成的版本变化。
7. `ROADMAP.md` —— 未完成事项和后续方向。
8. 当前目标版本对应 `docs/releases/vX.X.X.md`。
9. 最后才读取与任务直接相关的源代码。

如果上述文件与旧聊天记录冲突，**以仓库当前文件为准**。

## 3. 修改前必须回答的 7 个问题

Agent 在动手前应自行确认：

1. 当前要修改的是哪一个版本？
2. 这次改动属于产品功能、稳定性、架构、数据、部署还是文档治理？
3. 是否影响 `SB.user / SB.book / SB.magicBook / SB.theme / SB.experience / SB.store` 的职责边界？
4. 是否影响 Supabase schema、RLS、Storage 或现有真实数据？
5. 是否影响 GitHub Actions、分支、PR、main 或 Pages？
6. 是否破坏多用户、多 Book、多关系、多 Theme、多 Experience 的未来兼容性？
7. 本次改动需要同步更新哪些版本记录？

如果不能回答，不应直接大规模重构。

## 4. 当前最重要的架构边界

- `SB.book` = **当前数据 Book / Book Context**，不得再用于魔法书视觉控制。
- `SB.magicBook` = **Magic Celestial 魔法书视觉与开书动画控制器**。
- `SB.store` = **业务数据兼容层**，当前内部读写 Supabase `book_data.payload`。
- `magic-celestial` 只是第一套 Theme，不等于 Starbook Core。
- `world-map` 只是第一套 Experience，不等于 Starbook Core。
- 当前是情侣书，但 Starbook Core 不得写死“情侣是唯一关系”。
- 当前 UI 只有一本 Book，但业务代码不得假设用户永远只有一本 Book。
- 当前 Memory 与 City 仍有 V1 耦合，这是技术债，不应进一步强化。

## 5. 当前数据与发布原则

### 代码生命周期

`release/*` 或 `feature/*` → PR → `validate-starbook` → merge `main` → GitHub Pages 自动部署。

### 数据生命周期

Supabase Database / Private Storage **独立于 Git 分支和 Pages 部署**。

正常前端版本升级：

- 不清空 Supabase；
- 不重新 seed Book；
- 不重新导入照片；
- 不重新导入回忆；
- 不执行破坏性 reset SQL。

数据库结构升级或 Production 数据元信息/成员变更必须使用**向前 migration**。

当前 v1.5.1 的标题与成员变更由 `supabase/migrations/002_v151_title_and_members.sql` 管理，禁止通过重跑 seed 清空或覆盖业务数据。

## 6. 每个版本强制维护的文件

每个正式版本必须同步更新：

- `VERSION`
- `CHANGELOG.md`
- `ROADMAP.md`
- `PROJECT_STATE.md`
- `docs/releases/vX.X.X.md`

如果项目管理链路、架构边界、数据策略或发布策略变化，还必须同步更新：

- `AGENTS.md`
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`
- `docs/DATA_LIFECYCLE.md`
- `docs/RELEASE_WORKFLOW.md`

`tools/check_project.py` 与 `validate-starbook` 会检查其中一部分要求。

## 7. 每个 Release Record 必须明确写出的链路变化

每个 `docs/releases/vX.X.X.md` 至少包含：

- 本版目标；
- 产品体验变化；
- Runtime / 架构链路变化；
- 数据链路变化；
- Auth / 权限 / RLS 变化；
- Storage 变化；
- Git / PR / CI / Pages 发布链路变化；
- Agent / 文档治理链路变化；
- 文件变化；
- Migration / 手动操作；
- 测试与验证；
- 已知问题；
- 回滚方式；
- 下一版本建议。

如果某一项没有变化，也必须明确写“无变化”，不能省略。

## 8. 发布前最低检查

至少执行：

```powershell
python build.py
python tools/check_project.py
```

然后通过 PR 的 `validate-starbook`。

正式 Pages 只允许 `main` 部署。

## 9. 禁止事项

除非用户明确批准并已有迁移/回滚方案，否则禁止：

- 重置 Supabase production 数据；
- 删除真实 `book_data` / Storage 文件；
- 重新运行会覆盖真实数据的 seed；
- 在前端或仓库加入 `sb_secret_`、`service_role`、数据库密码、GitHub PAT；
- 关闭 RLS 来“解决”权限错误；
- 绕过 `main` 直接让 release/feature 分支覆盖 Production；
- 无版本记录地修改 schema；
- 为了重构漂亮而破坏 2026-10-29 周年交付稳定性；
- 把 `SB.book` 与 `SB.magicBook` 再次合并；
- 将当前唯一 Theme / Experience / Relationship 写死为平台唯一能力。

## 10. Agent 交接输出格式

一个 Agent 完成工作后，应在回复或 release record 中说明：

1. 当前版本；
2. 完成了什么；
3. 修改/新增/删除了哪些文件；
4. 是否改数据库；
5. 是否需要用户手动操作；
6. 如何测试；
7. 是否影响 Production / Supabase 数据；
8. 已知问题；
9. 下一步建议；
10. 是否已经更新版本治理文档。

---

**核心原则：Starbook 的代码可以迭代，用户真实回忆数据必须持续存在；当前周年版本可以简单，但未来扩展接口不能被写死。**
