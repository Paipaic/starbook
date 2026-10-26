# Starbook 项目管理全链路

> Canonical project-management document / 项目管理唯一主说明。
>
> 本文描述 Starbook 从“需求提出”到“代码修改、数据处理、验证、PR、合并、部署、数据保留、回滚、Agent 交接”的完整链路。
>
> 当其他文档与本文发生管理流程冲突时，应先核对 `PROJECT_STATE.md` 和最新 release record，再以当前仓库中更新日期较新的正式约定为准。

## 1. 项目目标与当前阶段

Starbook 长期目标不是一页情侣网页，而是一个可扩展的数字记忆书平台：

- 多用户；
- 一个用户可拥有/加入多本 Book；
- Book 可记录爱情、亲情、友情、旅行、个人等关系/主题；
- 多种 Theme；
- 多种 Experience；
- Memory 为长期核心实体；
- 数据与前端版本生命周期分离。

但 **2026-10-29 前** 的唯一交付目标仍然是：

> 基于 V1 做出一份稳定、私密、手机可用、可长期保存真实回忆的周年纪念版本。

因此当前采用 **Anniversary Bridge Architecture**：保留 V1 前端结构和 JSON 业务模型，以最小风险接入 Supabase。

## 2. 当前系统四条主链路

### 2.1 产品运行链路

```text
Supabase Auth
    ↓
SB.user
    ↓
SB.book.current
    ↓
SB.store.ready
    ↓
Magic Celestial Theme
    ↓
World Map Experience
    ↓
City / Memory / Media
```

### 2.2 代码发布链路

```text
需求/改动
    ↓
release/vX.X.X 或 feature/*
    ↓
本地 build + check
    ↓
Push
    ↓
Pull Request → main
    ↓
Validate Starbook
    ↓
Auto-merge / approved merge
    ↓
main
    ↓
Deploy Starbook to GitHub Pages
    ↓
Production URL 不变
```

### 2.3 数据链路

```text
Production Frontend
    ↓
Supabase Publishable Client
    ↓
Auth + RLS
    ↓
books / book_members / book_data
    ↓
Private Storage starbook-media
```

GitHub Pages 更新**不重建** Supabase 数据。

### 2.4 Agent 交接链路

```text
新 Agent
    ↓
AGENTS.md
    ↓
PROJECT_STATE.md
    ↓
本文件
    ↓
Architecture / Data policy
    ↓
CHANGELOG + ROADMAP + 当前 Release Record
    ↓
相关代码
    ↓
实施改动
    ↓
同步更新治理文件
```

## 3. Git 分支角色

### `main`

唯一 Production branch。

规则：

- GitHub Pages 只从 `main` 的成功构建 artifact 部署；
- 不应直接在 `main` 上进行日常功能开发；
- 应通过 PR 合并；
- 应要求 `validate-starbook` 通过；
- 不允许 force push；
- 不允许随意删除。

### `release/vX.X.X`

正式版本候选分支。

适用：

- 版本收尾；
- 多个相关改动组合；
- 版本文档与代码一起进入 PR。

### `feature/<name>`

未来较大独立功能使用，例如：

- `feature/theme-engine`
- `feature/timeline-experience`

当前周年交付阶段应避免产生过多长期分支。

### `archive/v1`

V1 历史安全备份，不参与当前部署。

## 4. 版本号策略

使用 Semantic Versioning 思路：

```text
MAJOR.MINOR.PATCH
```

例如：

- `1.5.1`：治理、修复、小改进；
- `1.6.0`：增加明显用户能力但不破坏兼容；
- `2.0.0`：长期平台架构进入正式多 Book / 正规化数据阶段，可能伴随迁移。

周年特殊 tag 可保留语义后缀，但 `VERSION` 从 v1.5.1 开始优先使用纯版本数字，便于自动检查。

## 5. 一次标准版本迭代的完整步骤

### Step 1 — 确定版本目标

先明确：

- 本版为什么存在；
- 用户能感知什么变化；
- 是否涉及数据库；
- 是否涉及部署链路；
- 是否涉及未来扩展约束。

### Step 2 — 更新版本治理文档草稿

在代码改动前或同步进行：

- 建立 `docs/releases/vX.X.X.md`；
- 更新 `VERSION`；
- 在 release record 中列出预计链路变化；
- 在 `ROADMAP.md` 标记本版目标。

### Step 3 — 创建/使用 release branch

推荐使用：

```powershell
.\publish.ps1 -Version X.X.X -Message "版本说明"
```

但注意：`publish.ps1` 是**发布收尾工具**，不是替代开发过程的万能脚本。

复杂版本可先手动创建 release branch 开发，再在完成时运行脚本。

### Step 4 — 修改代码

优先遵守：

- 小步修改；
- 不跨层级滥用全局对象；
- 不直接绕过 `SB.store` 在业务模块散落 Supabase 调用；
- 不把当前 Theme/Experience 写死进 Core；
- 不执行破坏性 production 数据操作。

### Step 5 — 本地构建与检查

必须执行：

```powershell
python build.py
python tools/check_project.py
```

如果失败，禁止发布。

### Step 6 — 更新版本记录

完成后同步：

- `CHANGELOG.md`：只记录已完成；
- `ROADMAP.md`：更新 TODO / DONE / 下一版本；
- `PROJECT_STATE.md`：更新当前真实状态；
- `docs/releases/vX.X.X.md`：写完整 release record；
- 如管理/架构/数据策略改变，更新对应 canonical docs。

### Step 7 — Push + PR

Release branch push 到 GitHub，并创建 PR：

```text
release/vX.X.X → main
```

### Step 8 — CI Validation

`Validate Starbook` 至少验证：

- 必需治理文件存在；
- VERSION 与 release record / PROJECT_STATE 一致；
- build 成功；
- JS 静态语法检查通过；
- Runtime namespace ownership 不被破坏；
- 高风险 Secret marker 不出现在部署产物；
- Pages entry point 存在。

### Step 9 — Merge main

Required checks 通过后：

- GitHub Auto-merge 可自动 squash merge；或
- 人工确认后 merge。

原则：**不采用无条件自动 push/merge main。**

### Step 10 — Production Deploy

`main` 更新自动触发：

```text
Deploy Starbook to GitHub Pages
```

流程：

```text
checkout main
→ Python
→ build.py
→ site/
→ upload Pages artifact
→ deploy-pages
```

Production URL 保持不变。

### Step 11 — Production smoke test

每个正式版本至少确认：

- 线上 URL 可打开；
- Auth 正常；
- 魔法书主链路正常；
- 本版核心能力正常；
- 已有 Supabase 数据仍存在；
- 图片/音乐仍可访问；
- 无明显 Console fatal error。

### Step 12 — Tag / Release

重要正式版本建议创建 Git tag：

```text
vX.X.X
```

周年最终版必须 tag。

## 6. 文档治理链路

### `AGENTS.md`

Agent 的唯一入口，简洁地告诉新窗口“先读什么、不能做什么”。

### `PROJECT_STATE.md`

描述**此刻真实状态**，不是历史记录。

必须及时更新：

- Current Release；
- 当前后端；
- Runtime Context；
- 已验证状态；
- Known Technical Debt；
- Highest Priority Next。

### `CHANGELOG.md`

记录**已经完成**的版本变化。

不放尚未完成的设想。

### `ROADMAP.md`

记录**尚未完成**和计划中的事项。

### `docs/releases/vX.X.X.md`

每版完整审计记录，必须包含所有链路变化，即使某链路“无变化”。

### Canonical supporting docs

- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`
- `docs/DATA_LIFECYCLE.md`
- `docs/RELEASE_WORKFLOW.md`

这些文件只有当对应规则发生变化时才修改，不需要每版机械重写。

## 7. 每版本必须记录的变化维度

为了让未来 Agent 能重建项目演进历史，每个 Release Record 必须逐项写：

1. Product / UX chain
2. Runtime chain
3. Architecture / extension contract
4. Auth / membership / RLS
5. Data model / schema / migration
6. Storage / media
7. Build / validation / CI
8. Git / branch / PR / merge
9. Pages deployment
10. Agent handoff / governance docs
11. Manual operator actions
12. Rollback path

如果没有变化，写：

```text
无变化：沿用 vX.X.X 的既有链路。
```

## 8. Supabase 与 Git 的关系

### Git 管代码

Git 保存：

- 前端源码；
- build script；
- SQL migration；
- 文档；
- CI/CD 配置。

### Supabase 管 Production 数据

Supabase 保存：

- Auth user；
- Book membership；
- Book runtime data；
- Private photos/music。

### 关键结论

```text
Git 版本更新 != Supabase 数据重置
```

任何 Agent 如果提出“每次发布重新导入数据”，默认视为错误方案，除非用户明确执行灾难恢复。

## 9. 数据库变更流程

普通前端版本：

- 不需要 SQL；
- 不运行 seed；
- 不动真实数据。

需要 schema 变化：

1. 新建新的 migration 编号；
2. 设计向前兼容；
3. 备份/验证；
4. SQL 必须尽量可重跑或明确一次性；
5. Release Record 写明 migration；
6. 用户手动执行 production SQL 时要有清晰步骤；
7. 不删除旧数据再重新录入。

## 10. 当前 Anniversary Bridge 的生命周期

当前：

```text
book_data.payload JSONB
```

仍保存 V1：

```json
{
  "cities": {},
  "memories": {},
  "settings": {}
}
```

长期 V2 才会正规化为：

- memories；
- locations；
- assets；
- settings；
- tags 等。

这次正规化必须是 migration，而不是 reset。

## 11. Production 回滚链路

### 前端回滚

优先：

- revert main 的有问题 commit / merge；
- 或从已知稳定 tag 创建修复 PR；
- Pages 自动重新部署稳定 main。

### 数据回滚

与前端分开处理。

禁止因为前端 Bug 就重置 Supabase。

如果 migration 导致数据问题，应依据该 migration 的回滚/恢复方案处理。

### V1 历史回退

`archive/v1` 和 `v1.0` 用于历史参考/灾难恢复，不是日常 production workflow。

## 12. 安全边界

浏览器允许：

- Supabase Project URL；
- Publishable Key。

禁止提交：

- `sb_secret_...`
- `service_role`
- Supabase DB password
- GitHub PAT
- 用户密码

Production 数据访问由 Auth + RLS + Private Storage policy 控制。

## 13. 周年交付阶段的变更预算

在 2026-10-29 前：

- 稳定性 > 架构纯洁度；
- 已验证功能 > 新功能数量；
- 不做无必要大重构；
- 不做 PWA / Realtime / 多 Theme 真实现；
- 10/28 晚 Feature Freeze。

## 14. Agent 结束工作时的交接要求

Agent 应说明：

- 当前 version / branch；
- 实际完成项；
- 代码链路变化；
- 数据链路变化；
- 发布链路变化；
- 手动操作；
- 测试结果；
- 未完成项；
- 文档是否同步。

如果 Agent 未更新应更新的 release record，则该工作不算完整完成。


## v1.5.1 数据元信息 / Membership 变更示例

当前《星屿之书》的标题变更和成员新增采用 `supabase/migrations/002_v151_title_and_members.sql` 向前迁移，而不是重新 seed。此模式是后续 Production 数据元信息和权限变更的标准做法：保留 `book_data.payload` 与 Storage，只修改明确需要变化的记录。
