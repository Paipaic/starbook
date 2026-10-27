#!/usr/bin/env python3
"""Starbook 构建脚本。

把 blocks/ 按文件名顺序拼接：
  index.html       —— 片段版
  site/index.html  —— GitHub Pages 完整版

v1.5 Anniversary 起，运行时数据由 Supabase 承载；构建脚本不再创建公开的 site/data/db.json。
如旧项目仍有真实 V1 数据，请先完成备份/迁移，不要直接删除原仓库数据。
"""
from pathlib import Path
import shutil

root = Path(__file__).parent
parts = []
for f in sorted((root / "blocks").glob("*.html")):
    parts.append(f"<!-- ████ BLOCK {f.stem} START ████ -->\n{f.read_text(encoding='utf-8').strip()}\n<!-- ████ BLOCK {f.stem} END ████ -->")
body = "\n\n".join(parts) + "\n"
(root / "index.html").write_text(body, encoding="utf-8")

HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>星屿之书</title>
<meta name="theme-color" content="#0d0805">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="星屿之书">
<link rel="icon" href="icon.png">
<link rel="apple-touch-icon" href="icon.png">
<style>html,body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
site = root / "site"
site.mkdir(exist_ok=True)
(site / "index.html").write_text(HEAD + body + "</body>\n</html>\n", encoding="utf-8")
(site / ".nojekyll").write_text("", encoding="utf-8")
if (root / "icon.png").exists():
    shutil.copy(root / "icon.png", site / "icon.png")

legacy_db = site / "data" / "db.json"
if legacy_db.exists():
    try:
        txt = legacy_db.read_text(encoding="utf-8").strip()
    except Exception as exc:
        raise RuntimeError("无法检查旧 site/data/db.json；为避免公开部署旧数据，构建已中止。") from exc
    if txt in ('', '{"cities":{},"memories":{},"settings":{}}'):
        legacy_db.unlink()
        try:
            legacy_db.parent.rmdir()
        except OSError:
            pass
    else:
        raise RuntimeError(
            "检测到非空 site/data/db.json。v1.5+ 禁止把旧 V1 数据部署到 GitHub Pages；"
            "请先备份/迁移到 Supabase，再删除该文件。"
        )

print("index.html 与 site/index.html 已生成，共", len(parts), "块")
