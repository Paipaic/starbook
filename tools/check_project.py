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

if 'api.github.com' in html or 'github token' in html.lower() or 'mp4-muxer' in html.lower():
    print('warning: legacy GitHub/mp4-muxer marker found in built site')
print('OK')
