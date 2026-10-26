# Starbook Project State

## Current Release

- Version: `1.5.0-anniversary` (in progress · Phase 3 stability)
- Deadline: `2026-10-29`
- Delivery goal: 私密、稳定、手机可用的周年纪念礼物。
- Base: V1 `blocks + build.py + site/index.html`。

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

Current Book preset:
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

## Known Technical Debt

- `book_data.payload` 是整体 JSONB，后续需要正规化。
- Memory 当前仍与 City 强耦合。
- Theme / Experience 目前只有 Context，没有插件加载器。
- Signed URL 仅做内存缓存；刷新后重新签名。
- 核心 Third-party CDN 尚未全部本地化。
- 完整深层 URL Router 尚未实现。
- 暂未使用 Realtime。
- 图片仍是单一压缩尺寸。

## Live Supabase Status

Confirmed by owner on 2026-10-26:
- `001_anniversary_bridge.sql`: executed successfully.
- `002_anniversary_owner.sql`: executed successfully.
- Book seed query returned one row.
- `starbook-media`: confirmed `public = false`.

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

1. 实机验证 Phase 3：Android / 手机端、连续返回、后台恢复、地图拖动误触。
2. 完成 Private Storage 正式照片与 BGM 的实际内容填充前测试。
3. Phase 3 稳定后实现周年扉页 / 献词 / 结尾（ANN-008）。
4. 2026-10-28 晚 Feature Freeze。
