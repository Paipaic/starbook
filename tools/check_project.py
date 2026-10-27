#!/usr/bin/env python3
from pathlib import Path
import re, subprocess, tempfile, sys

root = Path(__file__).resolve().parents[1]
html = (root/'site'/'index.html').read_text(encoding='utf-8')
ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
dups = sorted({x for x in ids if ids.count(x)>1})
scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', html, flags=re.S|re.I)
errors=[]
for i, js in enumerate(scripts,1):
    if not js.strip():
        continue
    with tempfile.NamedTemporaryFile('w', suffix='.js', encoding='utf-8', delete=False) as f:
        f.write(js); name=f.name
    r=subprocess.run(['node','--check',name],capture_output=True,text=True)
    Path(name).unlink(missing_ok=True)
    if r.returncode:
        errors.append((i,r.stderr.strip()))

print(f'blocks: {len(list((root/"blocks").glob("*.html")))}')
print(f'dom ids: {len(ids)}; duplicates: {dups or "none"}')
print(f'inline scripts: {len(scripts)}; syntax errors: {len(errors)}')
if errors:
    for i,e in errors: print(f'-- script {i} --\n{e}')
    sys.exit(1)

# Runtime namespace ownership checks: prevent the data Book Context from being
# overwritten by the Magic Celestial visual controller again.
block_text = {f.name: f.read_text(encoding='utf-8') for f in (root/'blocks').glob('*.html')}
book_assigns = [(name, len(re.findall(r'\bSB\.book\s*=', txt))) for name, txt in block_text.items()]
magic_assigns = [(name, len(re.findall(r'\bSB\.magicBook\s*=', txt))) for name, txt in block_text.items()]
book_assigns = [(n,c) for n,c in book_assigns if c]
magic_assigns = [(n,c) for n,c in magic_assigns if c]
if book_assigns != [('00-runtime.html', 1)]:
    print(f'ERROR: SB.book must be owned only by 00-runtime.html; found {book_assigns}')
    sys.exit(1)
if magic_assigns != [('03-magic-book.html', 1)]:
    print(f'ERROR: SB.magicBook must be owned only by 03-magic-book.html; found {magic_assigns}')
    sys.exit(1)


# Anniversary reliability guards.
if '_pendingHistory' not in block_text.get('00-core.html',''):
    print('ERROR: history back queue guard missing from 00-core.html')
    sys.exit(1)
if block_text.get('07-globe.html','').count('three.min.js') < 3:
    print('ERROR: Three.js must keep at least three CDN fallbacks until vendored locally')
    sys.exit(1)

# v1.5.2 Typography guards: fonts with broken / missing glyphs and symbols that
# depend on system fallback fonts must not return (they rendered as "乱码").
for banned_font in ['ZCOOL XiaoWei', 'ZCOOL+XiaoWei', 'Cinzel Decorative', 'Cinzel+Decorative']:
    if banned_font in html:
        print(f'ERROR: banned font {banned_font} found in built site (broken glyphs / unreadable numerals)')
        sys.exit(1)
fallback_symbols = [c for c in '\u2726\u270e\u2715\u27f2' if c in html]
if fallback_symbols:
    print('ERROR: symbols without webfont glyphs found in built site: ' + ' '.join(fallback_symbols) + ' — use SB.icon()')
    sys.exit(1)
if 'SB.icon = ' not in block_text.get('00-core.html', ''):
    print('ERROR: SB.icon helper missing from 00-core.html')
    sys.exit(1)
player_text = block_text.get('11-memory-player.html', '')
for marker in ('duck(', 'SB.player = ', 'SB.cinema = '):
    if marker not in player_text:
        print(f'ERROR: cinematic player marker {marker!r} missing from 11-memory-player.html')
        sys.exit(1)

if 'api.github.com' in html or 'github token' in html.lower() or 'mp4-muxer' in html.lower():
    print('warning: legacy GitHub/mp4-muxer marker found in built site')

# Hard guards against V1 persistence / Magic Book namespace regressions.
legacy_db = root/'site'/'data'/'db.json'
if legacy_db.exists():
    print('ERROR: legacy site/data/db.json exists; v1.5+ persistence must use Supabase')
    sys.exit(1)
active_source = '\n'.join(block_text.values()) + '\n' + html
for marker in ('data/db.json', 'github_pat_', 'ghApi('):
    if marker in active_source:
        print(f'ERROR: legacy runtime persistence marker found in active source: {marker}')
        sys.exit(1)
for prop in ('busy','open','reset','state','scene','cover','tilt','gemBtn','page','stage','shocks','leaves'):
    if re.search(rf'\bSB\.book\.{prop}\b', active_source):
        print(f'ERROR: visual Magic Book property leaked back to SB.book: {prop}; use SB.magicBook')
        sys.exit(1)

# Governance / release-document consistency checks.
version = (root/'VERSION').read_text(encoding='utf-8-sig').strip()
required_files = [
    root/'README.md',
    root/'AGENTS.md',
    root/'CHANGELOG.md',
    root/'ROADMAP.md',
    root/'PROJECT_STATE.md',
    root/'docs'/'PROJECT_MANAGEMENT_FULL_CHAIN.md',
    root/'docs'/'ARCHITECTURE_EXTENSION_CONTRACT.md',
    root/'docs'/'DATA_LIFECYCLE.md',
    root/'docs'/'RELEASE_WORKFLOW.md',
    root/'docs'/'PROJECT_DOCS_INDEX.md',
    root/'docs'/'RELEASE_AUTOMATION.md',
    root/'release-current.ps1',
    root/'scripts'/'releases'/f'release-v{version}.ps1',
    root/'docs'/'releases'/f'v{version}.md',
]
missing = [str(x.relative_to(root)) for x in required_files if not x.exists()]
if missing:
    print('ERROR: required governance/release files missing: ' + ', '.join(missing))
    sys.exit(1)

changelog = (root/'CHANGELOG.md').read_text(encoding='utf-8')
project_state = (root/'PROJECT_STATE.md').read_text(encoding='utf-8')
release_record = (root/'docs'/'releases'/f'v{version}.md').read_text(encoding='utf-8')
if f'[{version}]' not in changelog:
    print(f'ERROR: CHANGELOG.md does not contain current version [{version}]')
    sys.exit(1)
if f'`{version}`' not in project_state and f'Version: {version}' not in project_state:
    print(f'ERROR: PROJECT_STATE.md does not declare current version {version}')
    sys.exit(1)
for heading in [
    '版本目标', 'Runtime', 'Auth', '数据', 'Storage', 'Git', 'CI',
    'Agent', '用户需要手动操作', '测试', 'Production 数据影响', '回滚'
]:
    if heading not in release_record:
        print(f'ERROR: release record v{version}.md missing required topic: {heading}')
        sys.exit(1)

# Current product identity guards.
current_book_title = '星屿之书'
for filename in ['00-runtime.html', '03-magic-book.html', '02-menu.html']:
    if current_book_title not in block_text.get(filename, ''):
        print(f'ERROR: current product title {current_book_title} missing from {filename}')
        sys.exit(1)
if '我们的星屿' in ''.join(block_text.values()):
    print('ERROR: legacy current Book title remains in runtime blocks')
    sys.exit(1)

v151_migration = root/'supabase'/'migrations'/'002_v151_title_and_members.sql'
if version == '1.5.1' and not v151_migration.exists():
    print('ERROR: v1.5.1 title/member migration is missing')
    sys.exit(1)



runtime_cfg = block_text.get('00-config.html','')
if f"version: '{version}'" not in runtime_cfg:
    print(f'ERROR: blocks/00-config.html runtime version does not match VERSION ({version})')
    sys.exit(1)

print('OK')
