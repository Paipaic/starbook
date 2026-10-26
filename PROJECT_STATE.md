# Starbook Project State

## Current Release

- Version: `1.5.2` (Typography System「星文」)
- Deadline: `2026-10-29`
- Delivery goal: 私密、稳定、手机可用的周年纪念礼物。
- Base: V1 `blocks + build.py + site/index.html`。
- Runtime config version: `1.5.2`。

## Current Architecture

Frontend: GitHub Pages 静态页面。

Backend: Supabase Lite / Anniversary Bridge：
- Auth: Email + Password
- Database: `books`, `book_members`, `book_data`
- Storage: private bucket `starbook-media`
- Realtime: **not enabled for anniversary release**
- PWA: **not enabled for anniversary release**

## Runtime Context

- `SB.user`: 当前登录用户 / Session。
- `SB.book`: 当前数据 Book 与用户角色（Supabase Runtime Context）。
- `SB.magicBook`: Magic Celestial 封面与开书动画控制器；不得与 `SB.book` 合并。
- `SB.theme.current`: 当前 `magic-celestial`。
- `SB.experience.current`: 当前 `world-map`。
- `SB.store`: V1 兼容数据接口，内部读取 `book_data.payload`。

Current Book:
- id: `8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`
- name: `星屿之书`
- relationship: `romantic`
- theme: `magic-celestial`
- experience: `world-map`

## Anniversary Bridge Data

`book_data.payload` 当前继续保存 V1：

```json
{
  "cities": {},
  "memories": {},
  "settings": {}
}
```

这是临时兼容层，不是最终 V2 数据模型。

`revision` 用于轻量并发冲突检测。

## Storage Convention

Private bucket: `starbook-media`

```text
{book_id}/images/{generated-id}.jpg
{book_id}/audio/{generated-id}.mp3|m4a|...
```

媒体属于 Book，不属于单个 User。

## Architecture Invariants

1. Starbook 必须保留多用户扩展能力。
2. 一个用户未来可以拥有或加入多本 Book。
3. 一本 Book 可以有多个成员。
4. 不允许业务代码假设系统永远只有一本 Book。
5. 不允许 Starbook Core 假设所有 Book 都是情侣关系。
6. Relationship Type 与 Theme 独立。
7. Theme 与 Experience 独立。
8. `magic-celestial` 只是第一套 Theme。
9. `world-map` 只是第一套 Experience。
10. Memory 未来不得强制要求 Location / City。
11. Book 内业务数据必须有明确 Book 所属关系。
12. 当前未开放的未来能力优先通过配置关闭，而不是破坏扩展接口。
13. 2026-10-29 前，周年版稳定性高于架构纯洁度和功能数量。
14. 不为周年版引入 React / Vue / Vite 大迁移。
15. 不在浏览器或仓库中放 Supabase Secret / service_role / 数据库密码。

## Project Governance / Agent Handoff

从 v1.5.1 起，项目上下文与管理链路正式固化在仓库内：

- `AGENTS.md`: 新 Agent 必读入口。
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`: 开发 → 校验 → PR → main → Pages → 数据保留 → 回滚全链路。
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`: 多用户 / 多 Book / Relationship / Theme / Experience 长期扩展契约。
- `docs/DATA_LIFECYCLE.md`: Supabase 数据生命周期与 migration 规则。
- `docs/RELEASE_WORKFLOW.md`: 版本发布操作说明。
- `docs/releases/vX.X.X.md`: 每版本必须记录 Runtime、数据、CI、部署和治理链路变化。

Production governance:

```text
release/vX.X.X or feature/*
→ Pull Request
→ validate-starbook
→ merge main
→ Deploy Starbook to GitHub Pages
```

`main` 是唯一 Production branch。普通代码发布不重置 Supabase 数据。

## Visual / Typography (v1.5.2)

- 中文全站统一 Noto Serif SC（思源宋体）；拉丁铭文 Cinzel；数字 Cormorant Garamond；均来自 Google Fonts。
- ZCOOL XiaoWei 与 Cinzel Decorative 已移除（字形损坏 / 数字难辨），`tools/check_project.py` 防回归。
- 图标统一用 `SB.icon(name)` 内联 SVG，不依赖系统符号字体。
- 视觉升级后续版本计划：`docs/design/VISUAL_UPGRADE_PLAN.md`（v1.6.0 电影式放映、v1.6.1 转场、v1.6.2 魔法书/地球特效）。

## Known Technical Debt

- `book_data.payload` 是整体 JSONB，后续需要正规化。
- Memory 当前仍与 City 强耦合。
- Theme / Experience 目前只有 Context，没有插件加载器。
- Signed URL 仅做内存缓存；刷新后重新签名。
- 核心 Third-party CDN 尚未全部本地化（Google Fonts 仍为外部依赖；加载失败时回退系统宋体，版式不变）。
- 完整深层 URL Router 尚未实现。
- 暂未使用 Realtime。
- 图片仍是单一压缩尺寸。

## Live Supabase Status

Confirmed by owner on 2026-10-26:
- `001_anniversary_bridge.sql`: executed successfully.
- `002_anniversary_owner.sql`: executed successfully.
- Book seed query returned one row.
- `starbook-media`: confirmed `public = false`.

v1.5.1 planned forward migration:
- `002_v151_title_and_members.sql`: run after the v1.5.1 code release (or before final verification).
- Updates Book display name to `星屿之书`.
- Adds active editor `11aa32fe-3875-4880-81fb-02a543dca853`.
- Adds active editor `62adee54-c59a-4844-abb5-1b5629da3bf9`.
- Does **not** modify `book_data.payload` or Storage.

## Core live interaction verification

Confirmed by owner on 2026-10-26:
- Production URL can open successfully.
- Auth login / auth recovery paths work.
- Magic Book scene opens correctly.
- Globe drag and continent/country interactions work.
- Current mobile / back-navigation stability test has no observed blocker.

## Phase 2 interaction hotfix

- 已修复 `SB.book` 命名冲突：V1 魔法书动画控制器已重命名为 `SB.magicBook`。
- 原因：Runtime 多 Book Context 与 V1 视觉控制器曾覆盖同一全局命名空间，可能导致 Store 取不到当前 Book 并造成登录后交互异常。
- 修复后必须重新验证：登录 → 魔法书 → 地球拖拽 → 大洲 → 国家。

## Auth / Access Recovery Hotfix

- 密码或凭据错误：保留在登录表单，允许立即修改后重试。
- 已认证但没有当前 Book Membership：提供“重新检查权限”和“返回登录”。
- RLS / 权限 / Database 异常：提供“重新尝试”和“返回登录”，避免错误页锁死用户。
- “返回登录”会 sign out 当前 Supabase Session，并清空 `SB.book` Runtime Context。

## Phase 3 Stability Hardening

- 全局视口优先使用 `100dvh`，保留 `100vh` fallback。
- coarse pointer 下通用按钮、导航和菜单扩大触控目标。
- `SB.loadScript()` 增加单源超时与自动 fallback。
- Three.js 当前保留三 CDN fallback；本地 vendor 化仍是后续可选优化，不阻塞周年交付。
- 场景历史加入 `_pendingHistory`，连续 Android / 浏览器返回时以最后一次 history state 为准。
- bfcache 恢复会清理可能残留的 busy / veil / flash。
- Globe / Country Map 在触控设备上使用更宽松的拖动阈值，减少误触。

## Highest Priority Next

1. 发布 v1.5.2（release/v1.5.2 → PR → validate → main → Pages），在手机上确认「回忆总览」等文字显示正常。
1a. 继续视觉升级：v1.6.0 电影式放映 → v1.6.1 转场 → v1.6.2 魔法书/地球特效（10/28 Feature Freeze 前；后两版可顺延）。
2. 完成 Private Storage 正式照片与 BGM 的实际内容填充。
3. 核心稳定后实现周年扉页 / 献词 / 结尾（ANN-008）。
4. 进行最终手机端 Production URL 验收。
5. 2026-10-28 晚 Feature Freeze。
