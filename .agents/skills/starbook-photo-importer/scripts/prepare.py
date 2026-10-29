#!/usr/bin/env python3
"""Inventory Starbook input and validate agent-authored intermediate manifests."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

IMAGES = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic', '.heif', '.bmp'}
VIDEOS = {'.mp4', '.mov', '.m4v', '.avi'}


def natural(s):
    return [int(x) if x.isdigit() else x.casefold() for x in re.split(r'(\d+)', str(s))]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def ui_length(value):
    return len(value.encode('utf-16-le')) // 2


def scan(root):
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('素材目录必须是目录')
    stories = sorted(root.rglob('故事.md'), key=lambda p: natural(p.as_posix()))
    events = []
    for story in stories:
        folder = story.parent
        images, videos = [], []
        for f in sorted(folder.rglob('*'), key=lambda p: natural(p.relative_to(folder).as_posix())):
            if not f.is_file():
                continue
            # A nested event belongs to its own story, not its parent.
            if any((p / '故事.md').exists() for p in (f.parent, *f.parent.parents) if p != folder and folder in p.parents):
                continue
            rel = f.relative_to(folder).as_posix()
            if f.suffix.lower() in IMAGES:
                images.append({'file': rel, 'sha256': digest(f), 'caption': '', 'group': None})
            elif f.suffix.lower() in VIDEOS:
                videos.append(rel)
        match = re.search(r'(?<!\d)(20\d{2})[-年.](\d{1,2})(?:[-月.](\d{1,2}))?', folder.name)
        source_date = match.group(0) if match else ''
        month = ''
        if match and 1 <= int(match.group(2)) <= 12:
            month = f'{match.group(1)}-{int(match.group(2)):02d}'
        events.append({'event_dir': folder.relative_to(root).as_posix(),
                       'story_file': '故事.md', 'reference_copy': '放映文案.md' if (folder / '放映文案.md').is_file() else None,
                       'city': folder.parent.name if folder != root else '', 'country': '', 'region': '',
                       'source_date': source_date, 'date': month, 'title': '', 'note': '',
                       'cover_file': '', 'style': '', 'season': '', 'bgmMode': '',
                       'bgm_file': None, 'selection_reasons': {},
                       'slides': images, 'groups': [], 'videos': videos,
                       'status': 'draft', 'issues': []})
    return {'schema_version': 1, 'root': str(root), 'events': events,
            'warnings': [] if stories else ['未找到故事.md；请人工检查目录或文件命名']}


def validate(data):
    errors = []
    root = Path(data['root'])
    for e in data['events']:
        label = e['event_dir']
        def err(msg): errors.append(f'{label}: {msg}')
        if e.get('status') != 'ready': err('尚未完成看图、文案和地点核实')
        for k in ('city', 'country', 'region', 'title', 'note', 'date', 'cover_file'):
            if not str(e.get(k, '')).strip(): err(f'缺少 {k}')
        if e.get('city') == '待确认城市': err('城市待确认')
        if e.get('style') not in ('cinema', 'constellation', 'journal'): err('放映风格无效或未选择')
        if e.get('season') not in ('auto', 'none', 'spring', 'summer', 'autumn', 'winter'): err('季节主题无效或未选择')
        if e.get('bgmMode') not in ('global', 'own', 'none'): err('音乐模式无效或未选择')
        if e.get('bgmMode') == 'own':
            music = (root / label / str(e.get('bgm_file') or '')).resolve()
            event_root = (root / label).resolve()
            if not music.is_relative_to(event_root) or not music.is_file(): err('专属音乐文件不存在或越界')
        reasons = e.get('selection_reasons', {})
        for k in ('cover', 'style', 'season', 'music'):
            if not str(reasons.get(k, '')).strip(): err(f'缺少选择理由: {k}')
        if ui_length(e.get('title', '')) > 40 or ui_length(e.get('note', '')) > 300: err('标题或导入语超长')
        m = re.fullmatch(r'(\d{4})-(\d{2})', e.get('date', ''))
        if not m or not 2000 <= int(m.group(1)) <= date.today().year + 1 or not 1 <= int(m.group(2)) <= 12: err('网页年月无效或不在编辑器范围')
        slides = e.get('slides', [])
        if not slides: err('没有照片')
        names = [s.get('file') for s in slides]
        if len(names) != len(set(names)): err('照片文件重复')
        if e.get('cover_file') not in names: err('封面不在照片中')
        gs = e.get('groups', [])
        ids = [g.get('id') for g in gs]
        if len(ids) != len(set(ids)) or any(not x for x in ids): err('组 ID 为空或重复')
        runs, prev = [], None
        for s in slides:
            name = s.get('file', '')
            f = (root / label / name).resolve()
            event_root = (root / label).resolve()
            if not f.is_relative_to(event_root) or not f.is_file(): err(f'照片不存在或越界: {name}')
            elif digest(f) != s.get('sha256'): err(f'照片哈希已变化: {name}')
            if not s.get('caption', '').strip() or ui_length(s.get('caption', '')) > 120: err(f'照片描述为空或超长: {name}')
            g = s.get('group')
            if g and g not in ids: err(f'照片引用不存在的组: {name}')
            if g and g != prev: runs.append(g)
            prev = g
        if len(runs) != len(set(runs)): err('组内照片不连续')
        for g in gs:
            if sum(s.get('group') == g.get('id') for s in slides) < 2: err(f'分组少于两张: {g.get("id")}')
            if not str(g.get('text', '')).strip(): err(f'分组描述为空: {g.get("id")}')
            if ui_length(g.get('text', '')) > 300: err(f'分组描述超长: {g.get("id")}')
        if e.get('issues'): err('仍有未解决问题')
    if not data['events']: errors.append('没有找到事件')
    return errors


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd', required=True)
    s = subs.add_parser('scan'); s.add_argument('root'); s.add_argument('--output', required=True)
    v = subs.add_parser('validate'); v.add_argument('manifest')
    args = parser.parse_args()
    if args.cmd == 'scan':
        data = scan(Path(args.root))
        output = Path(args.output)
        if output.exists(): raise SystemExit('输出已存在，请选择新路径以避免覆盖')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'事件 {len(data["events"])}，照片 {sum(len(e["slides"]) for e in data["events"])}，视频 {sum(len(e["videos"]) for e in data["events"])}；草稿: {output}')
    else:
        data = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
        errors = validate(data)
        print('\n'.join(errors) if errors else '结构校验通过；仍需人工核实文案、地点和照片内容')
        if errors: raise SystemExit(1)


if __name__ == '__main__': main()
