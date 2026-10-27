# Starbook 一键版本发布自动化

> 从 v1.6.0 起，版本迭代完成后优先运行根目录 `release-current.ps1`，不再手工重复执行一长串 Git / Build / PR 命令。

## 1. 唯一需要记住的命令

完成一个版本的代码与内容迭代后，先把根目录 `VERSION` 改成目标版本，例如：

```text
1.6.1
```

然后在仓库根目录运行：

```powershell
.\release-current.ps1
```

可选地给本版填写一句发布说明：

```powershell
.\release-current.ps1 -Message "秘境之门转场系统"
```

## 2. 脚本自动完成什么

`release-current.ps1` 会：

1. 从 `VERSION` 读取目标版本，不需要再次手写 `-Version`；
2. 将常见误命名 `release/1.6.1` 自动规范为 `release/v1.6.1`；
3. 在从 `main` 发布时检查本地 `main` 与 `origin/main` 是否一致，避免自动 stash/rebase 造成冲突；
4. 同步 `blocks/00-config.html`、`PROJECT_STATE.md`、`AGENTS.md`、`README.md` 中结构化的当前版本号；
5. 如果 `docs/releases/vX.X.X.md` 不存在，根据治理模板自动生成基础 Release Record；已有文件永不覆盖；
6. 如果 CHANGELOG 缺少当前版本标题，自动补一个最小版本区块；已有版本内容永不覆盖；
7. 自动生成版本专属脚本 `scripts/releases/release-vX.X.X.ps1`；
8. 调用该版本专属脚本，再进入 `publish.ps1`；
9. `publish.ps1` 执行 build、`check_project.py`、Secret 扫描、commit、push、PR、Auto-merge；
10. PR 的 `validate-starbook` 通过后进入 `main`，再由 GitHub Pages 自动部署。

## 3. 为什么还生成版本专属脚本

例如 `VERSION=1.6.1` 时会生成：

```text
scripts/releases/release-v1.6.1.ps1
```

它记录这一版实际使用的版本号和默认发布描述，属于版本审计记录。以后 Agent 或人工查看旧版本时，不需要猜当时用了什么发布命令。

版本专属脚本可以单独重新执行：

```powershell
.\scripts\releases\release-v1.6.1.ps1
```

但日常仍推荐统一使用：

```powershell
.\release-current.ps1
```

## 4. Release Record 自动生成规则

如果 `docs/releases/vX.X.X.md` 已存在，脚本完全保留它。

如果不存在，脚本自动创建包含以下治理主题的基础记录：

- 版本目标；
- Runtime；
- 架构；
- Auth / Membership / RLS；
- 数据 / Migration；
- Storage；
- Git / PR / Merge；
- CI；
- Pages；
- Agent / 文档治理；
- 手动操作；
- 测试；
- Production 数据影响；
- 回滚；
- 下一版本建议。

自动生成只是“防止漏档”，不代表 Agent 可以省略真实设计记录。**凡是本版确实改变了架构、数据、权限或部署链路，仍必须把实际变化补充到 Release Record。**

## 5. 数据安全边界

一键发布脚本：

- 不执行 Supabase SQL；
- 不 reset Database；
- 不重新 seed Book；
- 不删除 Private Storage；
- 不重新导入回忆；
- 不把 `site/data/db.json` 当持久化数据库。

如果检测到 `supabase/` 相关未提交修改，自动生成的 Release Record 会提示人工核对 migration。

Production 数据变化仍遵循：**forward migration + release record + 人工明确执行**。

## 6. 防旧架构回流

构建与项目检查会阻止：

- 非空 `site/data/db.json` 被部署；
- Active blocks / built site 再次使用 `data/db.json`；
- GitHub PAT / `ghApi()` 重新成为运行时存储；
- `SB.book.open / busy / reset / ...` 重新用于 3D 魔法书视觉对象。

职责保持：

```text
SB.book      = Supabase Book Runtime Context
SB.magicBook = 3D 魔法书视觉控制器
```

## 7. 如果脚本停止

脚本在以下情况会主动停止，而不是偷偷处理：

- 本地 `main` 落后/偏离 `origin/main`；
- 当前分支既不是 `main` 也不是目标 `release/vX.X.X`；
- build / check_project 失败；
- Secret 扫描失败；
- GitHub CLI 未登录；
- required checks / GitHub rules 阻止 merge。

这是为了避免自动 stash、强推或数据库操作造成不可逆问题。

## 8. 新 Agent 的版本发布规则

新 Agent 完成版本开发后必须：

1. 更新 `VERSION`；
2. 更新本版真实 `CHANGELOG / PROJECT_STATE / ROADMAP / Release Record`；
3. 不手写一套新的发布流程；
4. 直接运行 `release-current.ps1`；
5. 若修改了发布链路本身，同步更新本文件与 `PROJECT_MANAGEMENT_FULL_CHAIN.md`。
