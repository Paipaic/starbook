# 星屿之书 Starbook

当前正式项目版本：**v1.6.0**。

这是一个以沉浸式“记忆书”为核心的私人数字记忆项目。当前生产形态是 `romantic + magic-celestial + world-map`，但底层架构已经为多用户、多 Book、多关系类型、多 Theme、多 Experience 的后续扩展保留边界。

## 新 Agent / 新开发窗口

**不要直接从代码开始。**

第一步请阅读：[`AGENTS.md`](AGENTS.md)

随后严格按照其中定义的顺序读取 `PROJECT_STATE.md`、全链路管理文档、扩展契约、数据生命周期、CHANGELOG、ROADMAP 和当前 Release Record。

## Production

```text
release/* or feature/*
→ Pull Request
→ validate-starbook
→ main
→ GitHub Actions
→ GitHub Pages
```

`main` 是唯一 Production branch。Supabase Database / Private Storage 与 Git 分支生命周期独立，普通代码版本发布不会重置真实回忆数据。

## 当前 Book

- 名称：**星屿之书**
- Relationship：`romantic`
- Theme：`magic-celestial`
- Experience：`world-map`

## 发布前

```powershell
python build.py
python tools/check_project.py
```

正式版本必须同步维护 `VERSION`、`CHANGELOG.md`、`ROADMAP.md`、`PROJECT_STATE.md` 与 `docs/releases/vX.X.X.md`。
