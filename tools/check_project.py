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

# v1.7.3 performance / scene-transaction baseline guards.
core_text = block_text.get('00-core.html','')
store_text = block_text.get('05-store.html','')
city_text = block_text.get('10-city-album.html','')
editor_text = block_text.get('12-memory-editor.html','')
if 'SB.nextPaint' not in core_text:
    print('ERROR: scene paint synchronization missing from 00-core.html')
    sys.exit(1)
for marker in ('prepareTarget', 'scenes.prefetch', 'await prepareTarget', 'await Promise.resolve(nextHook.enter'):
    if marker not in core_text:
        print(f'ERROR: v1.7.3 scene transaction marker missing: {marker}')
        sys.exit(1)
if "prevEl?.classList.add('is-active')" in core_text:
    print('ERROR: portal transition reactivates previous scene and can cause visual residue')
    sys.exit(1)
if 'st.prefetchUrls' not in store_text:
    print('ERROR: Signed URL prefetch API missing from 05-store.html')
    sys.exit(1)
if re.search(r'async function applyRemote\(row\)\s*\{[^}]*await\s+warmUrls', store_text, re.S):
    print('ERROR: Store startup must not await full-library warmUrls; use scene-level prefetch')
    sys.exit(1)
for marker in ('async function prime(m)', 'SB.fx?.playback?.(true)', 'play:() => play(false), seek, jump, prime'):
    if marker not in player_text:
        print(f'ERROR: player performance marker {marker!r} missing from 11-memory-player.html')
        sys.exit(1)
if 'loading="lazy"' not in editor_text:
    print('ERROR: memory editor image lazy loading missing')
    sys.exit(1)
if 'content-visibility:auto' not in city_text:
    print('ERROR: city album offscreen rendering guard missing')
    sys.exit(1)

# v1.8.0 guards: magic gate transitions, search data, navigation simplification, unique DOM ids.
if dups:
    print(f'ERROR: duplicate DOM ids would break runtime lookups: {dups}')
    sys.exit(1)
gate_text = block_text.get('01b-gate.html', '')
for marker in ('SB.gate = ', 'portalFrame', 'abort()'):
    if marker not in gate_text:
        print(f'ERROR: magic gate marker {marker!r} missing from 01b-gate.html')
        sys.exit(1)
if 'gate.cover(gateKind' not in core_text or 'SB.gate?.abort?.()' not in core_text:
    print('ERROR: Scene Runtime must route flash/veil through SB.gate and abort it on failure')
    sys.exit(1)
if 'SB.WORLD_CITIES = ' not in block_text.get('06-world-cities.html', ''):
    print('ERROR: offline world city search data missing (06-world-cities.html)')
    sys.exit(1)
if "register('continent'" in ''.join(block_text.values()):
    print('ERROR: continent directory scene was removed in v1.8.0 and must not return')
    sys.exit(1)

# v1.8.1 guards: settings live in SB.dock, menu only holds scene navigation, timeline scene keeps id 'overview'.
if 'SB.dock = ' not in block_text.get('02y-dock.html', ''):
    print('ERROR: SB.dock utility icons missing (02y-dock.html)')
    sys.exit(1)
all_blocks = ''.join(block_text.values())
for legacy in ("menu.add({id:'music'", "menu.add({id:'motion'", "SB.menu.add({id:'account'", "menu.add({id:'book'", "SB.menu.add({id:'continents'"):
    if legacy in all_blocks:
        print(f'ERROR: settings / legacy item must not return to the menu: {legacy}')
        sys.exit(1)
if "register('overview'" not in block_text.get('13-overview.html', '') or '时光长卷' not in block_text.get('13-overview.html', ''):
    print('ERROR: timeline (时光长卷) must stay registered as scene id overview')
    sys.exit(1)

# v1.8.2 mobile guards: no WebGL warm-up during the visible book opening; rune ring stays out of the 3D context.
if "prefetch?.('globe'" in block_text.get('04-book-opening.html', '') or "prefetch('globe'" in block_text.get('04-book-opening.html', ''):
    print('ERROR: book opening must not prefetch the globe (WebGL init freezes the opening on phones)')
    sys.exit(1)
book_text = block_text.get('03-magic-book.html', '')
if 'bk-runes-front' not in book_text or 'bk-runes-back' not in book_text:
    print('ERROR: magic book rune ring must use the 2D front/back layers (3D ring causes WebKit plane splitting)')
    sys.exit(1)

# v1.9.0 guards: admin-division search data, editor batch-action registry, gate font decision.
if 'SB.ADMIN_DIVISIONS = ' not in block_text.get('06-admin-divisions.html', ''):
    print('ERROR: admin-division search data missing (06-admin-divisions.html, run tools/make_admin.py)')
    sys.exit(1)
if 'photoActions' not in block_text.get('12-memory-editor.html', ''):
    print('ERROR: editor batch photo action registry (SB.editor.photoActions) missing')
    sys.exit(1)
if 'gateType' not in block_text.get('00-runtime.html', ''):
    print('ERROR: login gate one-time font decision (data-gate-type) missing')
    sys.exit(1)

# v1.9.1 guards: photo groups in editor + player; no data-source line in the globe search panel.
if 'normalizeGroups' not in block_text.get('12-memory-editor.html', '') or "id:'group'" not in block_text.get('12-memory-editor.html', ''):
    print('ERROR: editor photo groups (normalizeGroups / group action) missing')
    sys.exit(1)
if 'unitsOf' not in block_text.get('11-memory-player.html', '') or 'holdsOf' not in block_text.get('11-memory-player.html', ''):
    print('ERROR: player group units (unitsOf) / manual-playback holds (holdsOf) missing')
    sys.exit(1)
if '数据：国家统计局' in block_text.get('07-globe.html', ''):
    print('ERROR: globe search panel must not show the data-source line (Owner request v1.9.1; credit lives in README)')
    sys.exit(1)

# v1.9.2 guards: screening language library, movie-mode preload, editor drag into / out of groups.
pl = block_text.get('11-memory-player.html', '')
if 'pickShot' not in pl or 'animGen' not in pl or 'async function start()' not in pl:
    print('ERROR: player screening library (pickShot / animGen) or movie-mode preload (start) missing')
    sys.exit(1)
if 'wireGroupDrop' not in block_text.get('12-memory-editor.html', ''):
    print('ERROR: editor drag into / out of photo groups (wireGroupDrop) missing')
    sys.exit(1)

# v1.10.0 guards: ring timeline + year reel; music auto-loop; UTF-8 safety of docs and release scripts.
ov = block_text.get('13-overview.html', '')
if 'function proj(' not in ov or 'stations(' not in ov or 'yearReel' not in ov:
    print('ERROR: overview ring timeline (proj / stations / yearReel hook) missing')
    sys.exit(1)
if 'SB.yearReel = ' not in block_text.get('14-year-reel.html', ''):
    print('ERROR: year reel block (14-year-reel.html, SB.yearReel) missing')
    sys.exit(1)
if "el.addEventListener('ended'" not in block_text.get('11-memory-player.html', ''):
    print('ERROR: background music auto-loop recovery missing')
    sys.exit(1)
# v1.10.1 guards: windowed ring (cards + beads), no lazy images, no rebuild on unchanged data; day-precision dates; book page night world.
if 'function arcs(' not in ov or 'sigOf()' not in ov or 'loading="lazy"' in ov or 'settings?.anniversary' not in ov:
    print('ERROR: overview v1.10.1 (arcs fisheye window / sigOf rebuild guard / no lazy images / settings.anniversary) broken')
    sys.exit(1)
if 'SB.date = ' not in block_text.get('00-core.html', '') or 'SB.date.daysIn' not in block_text.get('12-memory-editor.html', ''):
    print('ERROR: day-precision dates (SB.date in core, day select in editor) missing')
    sys.exit(1)
if "world:'night', deepLink:true,\n    title:()=>'魔法书'" not in block_text.get('03-magic-book.html', ''):
    print("ERROR: magic book scene must use world 'night' (starry blue background, v1.10.1)")
    sys.exit(1)
# v1.10.2 guards: reel seek + progress bar and no flying tail line; return position via history; global drag guard; Android proxies.
yr = block_text.get('14-year-reel.html', '')
if 'function seekTo(' not in yr or 'yr-bar' not in yr or 'class="tail"' in yr:
    print('ERROR: year reel v1.10.2 (seekTo / progress bar, no flying tail line) broken')
    sys.exit(1)
if 'opts?.fromHistory' not in ov:
    print('ERROR: overview must restore position when returning via history (fromHistory)')
    sys.exit(1)
if "addEventListener('dragstart'" not in block_text.get('00-core.html', '') or 'st.displayUrl' not in block_text.get('05-store.html', ''):
    print('ERROR: global dragstart guard (00-core) or Android display proxies (05-store) missing')
    sys.exit(1)
# GBK-misread UTF-8 (mojibake) markers that appeared when Windows PowerShell read BOM-less UTF-8 as ANSI.
MOJIBAKE = ['銆', '锛', '鈥', '鈹', '鏄熷', '涔嬩功']
for rel in ['AGENTS.md', 'README.md', 'PROJECT_STATE.md', 'CHANGELOG.md', 'ROADMAP.md', 'blocks/00-config.html']:
    txt = (root/rel).read_text(encoding='utf-8-sig')
    bad = [m for m in MOJIBAKE if m in txt]
    if bad:
        print(f'ERROR: {rel} looks garbled (mojibake {bad}); restore it from git and read files with -Encoding UTF8')
        sys.exit(1)
for rel in ['release-current.ps1', 'publish.ps1']:
    for ln in (root/rel).read_text(encoding='utf-8-sig').splitlines():
        if 'Get-Content' in ln and not ln.lstrip().startswith('#') and '-Encoding' not in ln:
            print(f'ERROR: {rel} reads a file without -Encoding UTF8: {ln.strip()}')
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
    root/'docs'/'PERFORMANCE_GUIDE.md',
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
