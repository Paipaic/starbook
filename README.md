# 星屿之书 Starbook

当前正式项目版本：**v1.12.2**。

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

## 一键发布

从 v1.6.0 起，完成新版本迭代后优先使用：

```powershell
.\release-current.ps1
```

脚本从 `VERSION` 自动识别版本，自动补齐缺失 Release Record、生成 `scripts/releases/release-vX.X.X.ps1`，再执行 build / validation / PR / Auto-merge。详细说明见 [`docs/RELEASE_AUTOMATION.md`](docs/RELEASE_AUTOMATION.md)。

## 数据来源

世界星图搜索使用的公开数据（页面上不再显示来源行，在此署名）：

- 中国行政区划：[Vonng/adcode](https://github.com/Vonng/adcode)（国家统计局 2016 区划代码 + 民政部变更 + 高德地图地理中心）。
- 美国州 / 县：美国人口普查局 2010 县几何中心（via [btskinner/spatial](https://github.com/btskinner/spatial)）+ [kjhealy/fips-codes](https://github.com/kjhealy/fips-codes)。
- 世界城市：[GeoNames](https://www.geonames.org/)（CC BY 4.0）与 Unicode CLDR 中文名（`tools/make_cities.py`）。
- 在线地名补充搜索：[Open-Meteo Geocoding API](https://open-meteo.com/)（CC BY 4.0，地点数据来自 GeoNames；只发送搜索词与国家代码）。
- 省级地区中文名（v1.12.2，`tools/make_region_zh.py`）：[Unicode CLDR](https://cldr.unicode.org/) subdivisions 中文名（Unicode License v3）、[Natural Earth](https://www.naturalearthdata.com/) admin-1（公有领域，中文名补充与代表点）、[OpenCC](https://github.com/BYVoid/OpenCC) 繁简词典（Apache-2.0）；分区与 Highcharts map-collection 2.3.3 对应。
