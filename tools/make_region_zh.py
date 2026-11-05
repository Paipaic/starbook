#!/usr/bin/env python3
"""生成块 06-region-zh：国家面板省级地区的中文名与代表点（v1.12.2，复盘 #3 / #4）。

数据来源（均为公开数据，生成时从本地克隆读取，运行时不访问这些仓库）：
  地图分区：highcharts/map-collection-dist v2.3.3（与运行时加载的省级地图同一版本）countries/<k>/<k>-all.geo.json
           ——取每个分区的 hc-key、iso_3166_2 / iso3166-2、hasc、woe-id。
  中文名：  Unicode CLDR common/subdivisions/zh.xml（ISO 3166-2 分区中文名，Unicode License v3）。
  繁简：    OpenCC data/dictionary/TSPhrases.txt + TSCharacters.txt（Apache-2.0）——部分来源条目是繁体，统一转成简体。
  手工修正：法国 2016 年合并后的大区（来源里仍是合并前的旧名）见下方 FIX。
  补充：    Natural Earth ne_10m_admin_1_states_provinces（公有领域）——
           1) 地图分区没有 ISO 代码时，用 hasc / woe-id 找到 Natural Earth 条目再取 ISO 代码；
           2) CLDR 没有中文名时，用 Natural Earth 的 name_zh；
           3) 代表点：Natural Earth 的 label point（latitude / longitude，保证在分区内部）。
              地图分区由多个 Natural Earth 条目组成时（如法国的大区 = 多个省），取离这些条目平均位置最近的那个 label point。

为什么需要代表点：大多数省级地图是投影坐标（hc-transform），无法直接换算经纬度；
v1.12.1 及以前这些国家的「地区中心」退回到国家中心。v1.12.2 起作为「没有找到精确位置」时的后备，
以及给候选城市推断所在地区（离哪个代表点最近）。

输出：blocks/06-region-zh.html，定义 SB.REGION_ZH = { 国家key: "短key=中文名,经度,纬度;..." }（短 key = hc-key 去掉「国家key-」前缀）。
      中文名为空时只有坐标（中文名回退英文）。中国 / 美国 / 日本 的中文名仍以 06-world-geo 的手工表为准，这里只补坐标。

运行：python tools/make_region_zh.py <map-collection-dist 克隆目录> <cldr 克隆目录> <ne_10m_admin_1_states_provinces.geojson> <OpenCC 克隆目录>
"""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parent.parent

# 先覆盖常去的国家（复盘 #4：约 30 个起步，这里 50 个）；需要更多时在这里追加后重新生成
COUNTRIES = ('cn us jp kr th sg my vn id ph kh la np lk in ae tr eg ma tw '
             'fr it es pt gb ie de ch at nl be cz hu gr hr is no se fi dk pl ru '
             'au nz ca mx br ar cl pe za ke').split()
HAND = {'cn', 'us', 'jp'}           # 中文名有手工表的国家，只补坐标
# 来源里过时或不通行的译名（法国 2016 年大区合并后的正式中文译名）
FIX = {
    'fr-occ': '奥克西塔尼', 'fr-naq': '新阿基坦', 'fr-hdf': '上法兰西', 'fr-ara': '奥弗涅-罗讷-阿尔卑斯',
    'fr-ges': '大东部', 'fr-bfc': '勃艮第-弗朗什-孔泰', 'fr-cvl': '中央-卢瓦尔河谷', 'fr-cor': '科西嘉',
}


def simplifier(cc_dir):
    def load(name):
        d = {}
        for line in (Path(cc_dir) / 'data/dictionary' / name).read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'): continue
            a, b = line.split('\t', 1); d[a] = b.split(' ')[0]
        return d
    ph, ch = load('TSPhrases.txt'), load('TSCharacters.txt')
    phl = sorted(ph, key=len, reverse=True)
    def conv(t):
        for w in phl:
            if w in t: t = t.replace(w, ph[w])
        return ''.join(ch.get(c, c) for c in t)
    return conv


def clean(t):
    t = re.sub(r'[\u00b2\u00b3\u00b9\u2070-\u209f]', '', t or '').strip()
    return t.replace(',', '，').replace(';', '；').replace('=', '')


def norm(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', str(t or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z]', '', t)


def main(hc_dir, cldr_dir, ne_path, cc_dir):
    hc_dir, cldr_dir = Path(hc_dir), Path(cldr_dir)
    s2 = simplifier(cc_dir)
    zh = {m.group(1): m.group(2).strip() for m in re.finditer(
        r'<subdivision type="([a-z0-9]+)"[^>]*>([^<]+)</subdivision>',
        (cldr_dir / 'common/subdivisions/zh.xml').read_text(encoding='utf-8'))}
    ne = [f['properties'] for f in json.loads(Path(ne_path).read_text(encoding='utf-8'))['features']]
    by_iso, by_hasc, by_woe, by_reg = {}, {}, {}, {}
    for p in ne:
        if p.get('iso_3166_2'): by_iso.setdefault(p['iso_3166_2'], []).append(p)
        if p.get('code_hasc'): by_hasc.setdefault(p['code_hasc'], []).append(p)
        if p.get('woe_id') not in (None, -99, -90, 0): by_woe.setdefault(str(p['woe_id']), []).append(p)
        if p.get('region_cod'): by_reg.setdefault(p['region_cod'].strip(), []).append(p)

    def label(rows):
        pts = [(p['longitude'], p['latitude']) for p in rows if p.get('longitude') is not None]
        if not pts: return None
        if len(pts) == 1: return pts[0]
        mx, my = sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
        return min(pts, key=lambda q: (q[0] - mx) ** 2 + (q[1] - my) ** 2)

    out, stat = {}, []
    for k in COUNTRIES:
        f = hc_dir / f'countries/{k}/{k}-all.geo.json'
        if not f.exists(): stat.append(f'{k}: 没有地图'); continue
        rows, n, named, placed = [], 0, 0, 0
        for feat in json.loads(f.read_text(encoding='utf-8'))['features']:
            p = feat.get('properties') or {}
            key = p.get('hc-key')
            if not key or p.get('hc-group') != 'admin1': continue
            n += 1
            iso = p.get('iso_3166_2') or p.get('iso3166-2') or ''
            if iso.endswith('-'): iso = ''
            cand = []
            if iso: cand = by_iso.get(iso) or by_reg.get(iso) or []
            # 没有 ISO 代码：先按 woe-id（最具体），再按「hc-key 当作 ISO 代码且英文名相同」，最后按 hasc（只接受唯一匹配）
            if not cand and p.get('woe-id') not in (None, '-99'): cand = by_woe.get(str(p['woe-id']), [])
            if not cand:
                guess = by_iso.get(key.upper(), [])
                if len(guess) == 1 and norm(guess[0].get('name')) and norm(guess[0].get('name')) == norm(p.get('name')): cand = guess
            if not cand and p.get('hasc') not in (None, '-99'):
                h = by_hasc.get(p['hasc'], [])
                if len(h) == 1: cand = h
            if not iso and len(cand) == 1: iso = cand[0].get('iso_3166_2') or ''
            name = ''
            if k not in HAND:
                if iso: name = zh.get(iso.lower().replace('-', ''), '')
                if not name and len(cand) == 1: name = (cand[0].get('name_zh') or '').strip()
            ll = label(cand)
            if ll is None and p.get('longitude') not in (None, ''):
                try: ll = (float(p['longitude']), float(p['latitude']))
                except ValueError: ll = None
            if not name and ll is None: continue
            if key in FIX: name = FIX[key]
            short = key[len(k) + 1:] if key.startswith(k + '-') else key
            name = s2(clean(name))
            rows.append(f'{short}={name},{ll[0]:.2f},{ll[1]:.2f}' if ll else f'{short}={name},,')
            named += bool(name); placed += ll is not None
        out[k] = ';'.join(rows)
        stat.append(f'{k}: {n} 个分区，中文名 {named}，代表点 {placed}')

    js = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    html = ('<script>\n/* ── 块 06r · 省级地区中文名与代表点（由 tools/make_region_zh.py 生成，请勿手改）──\n'
            '   SB.REGION_ZH[国家key] = "短key=中文名,经度,纬度;..."；06-world-geo 的 regionZh() / 地区中心使用。\n'
            '   来源：Unicode CLDR subdivisions 中文名、Natural Earth admin-1（公有领域）、Highcharts map-collection 2.3.3 分区。 */\n'
            'window.SB = window.SB || {};\nSB.REGION_ZH = ' + js + ';\n</script>\n')
    dst = ROOT / 'blocks/06-region-zh.html'
    dst.write_text(html, encoding='utf-8')
    print('\n'.join(stat)); print(f'写入 {dst}（{len(html.encode())} 字节）')


if __name__ == '__main__':
    if len(sys.argv) != 5: sys.exit(__doc__)
    main(*sys.argv[1:])
