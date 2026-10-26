# Starbook v1.5.1 · Operator Steps

> 本文件只描述 v1.5.1 这一次发布需要项目 Owner 手动完成的步骤。长期项目规则见 `AGENTS.md` 与 `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`。

## 0. 本版本目标

- 建立完整 Agent 交接 / 项目治理文档体系；
- 将当前 Book 标题统一为《星屿之书》；
- 添加两名 active `editor`；
- 不重置、不重新导入现有回忆数据；
- 验证 release → PR → validate → main → Pages 全链路。

## 1. 将 v1.5.1 文件放入 release 分支

从最新 `main` 创建或切换到：

```powershell
git checkout main
git pull --rebase origin main
git checkout -b release/v1.5.1
```

将 v1.5.1 项目文件覆盖到仓库根目录，保留 `.git/`。

## 2. 本地验证

```powershell
python build.py
python tools/check_project.py
```

必须全部通过。

## 3. 发布 PR

如果已经安装并登录 GitHub CLI：

```powershell
.\publish.ps1 -Version 1.5.1 -Message "项目治理、Agent 全链路、星屿之书标题与成员更新"
```

脚本将 push `release/v1.5.1`、创建 PR，并尝试开启 Auto-merge。

GitHub 侧确认：

```text
release/v1.5.1
→ Validate Starbook
→ main
→ Deploy Starbook to GitHub Pages
```

## 4. 运行 v1.5.1 Supabase migration

确认以下两个 UID 已存在于：

`Supabase → Authentication → Users`

- `11aa32fe-3875-4880-81fb-02a543dca853`
- `62adee54-c59a-4844-abb5-1b5629da3bf9`

然后进入：

`Supabase → SQL Editor → New query`

整段运行：

`supabase/migrations/002_v151_title_and_members.sql`

该脚本会：

- 把当前固定 Book 名称更新为《星屿之书》；
- 将上述两个 UID upsert 为 `editor / active`；
- 不修改 `book_data.payload`；
- 不删除 Storage；
- 不重新 seed Book 数据。

脚本会检查两个 UID 是否都成功成为 editor；如果任一 UID 不存在，会报错并回滚整个 migration。

## 5. 验证 Supabase 结果

在 SQL Editor 运行：

```sql
select
  b.name,
  bm.user_id,
  bm.role,
  bm.status
from public.books b
join public.book_members bm on bm.book_id = b.id
where b.id = '8a3cc6fe-b667-4ce7-b47b-79cebc0e1353'
order by bm.role, bm.user_id;
```

预期：

- Book name = `星屿之书`；
- 原 Owner 仍为 `owner / active`；
- 两个新增 UID 均为 `editor / active`。

## 6. Production smoke test

打开固定 Production URL，确认：

- 页面标题 / 登录页显示《星屿之书》；
- Owner 登录正常；
- 新 editor 账号可登录并读取同一本 Book；
- editor 可以写入回忆；
- 原有城市、回忆、照片、音乐仍存在；
- 魔法书、地球、大洲、国家、返回链路正常。

## 7. 数据保留结论

v1.5.1 不要求重新导入任何旧数据。

```text
Git / Pages：更新前端代码
Supabase：继续持有原 Book / book_data / Private Storage
```

如果已有回忆消失，视为异常，不要重新 seed；优先停止操作并检查 Book ID / RLS / migration。
