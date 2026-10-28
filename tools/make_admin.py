#!/usr/bin/env python3
"""生成块 06-admin-divisions：地球搜索栏的中国 / 美国行政区划库（v1.9.0）。

数据来源（均为公开数据，生成时从本地克隆读取，运行时不访问这些仓库）：
  中国：Vonng/adcode（https://github.com/Vonng/adcode）——国家统计局 2016 区划代码 + 民政部变更 + 高德地图地理中心；
        取 rank 1（省级）、rank 2（地级）、rank 3（县级：市辖区 / 县 / 县级市 / 旗等），跳过「市辖区」「省直辖县级行政区划」等虚拟单位。
  美国：btskinner/spatial data/county_centers.csv（美国人口普查局 2010 年县几何中心）
        + kjhealy/fips-codes county_fips_master.csv / state_fips_master.csv（FIPS → 县名 / 州名）。
        州的中心取该州所有县几何中心的平均值；州中文名为下方手工对照表。

输出：blocks/06-admin-divisions.html，定义 SB.ADMIN_DIVISIONS（紧凑字符串，搜索时才解析）：
  cn.p = "省名,经度,纬度;..."                       （省级，按出现顺序编号）
  cn.c = "市名,省号,经度,纬度;..."                   （地级）
  cn.d = "县级名,省号,市号(-1=直属省),经度,纬度;..."  （县级）
  us.s = "州缩写,英文名,中文名,经度,纬度,别名;..."
  us.c = "县名,州号,经度,纬度;..."

运行：python tools/make_admin.py <adcode 克隆目录> <btskinner/spatial 克隆目录> <kjhealy/fips-codes 克隆目录>
"""
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parent.parent

US_ZH = {
 'AL':'亚拉巴马州','AK':'阿拉斯加州','AZ':'亚利桑那州','AR':'阿肯色州','CA':'加利福尼亚州','CO':'科罗拉多州','CT':'康涅狄格州','DE':'特拉华州',
 'DC':'华盛顿哥伦比亚特区','FL':'佛罗里达州','GA':'佐治亚州','HI':'夏威夷州','ID':'爱达荷州','IL':'伊利诺伊州','IN':'印第安纳州','IA':'艾奥瓦州',
 'KS':'堪萨斯州','KY':'肯塔基州','LA':'路易斯安那州','ME':'缅因州','MD':'马里兰州','MA':'马萨诸塞州','MI':'密歇根州','MN':'明尼苏达州',
 'MS':'密西西比州','MO':'密苏里州','MT':'蒙大拿州','NE':'内布拉斯加州','NV':'内华达州','NH':'新罕布什尔州','NJ':'新泽西州','NM':'新墨西哥州',
 'NY':'纽约州','NC':'北卡罗来纳州','ND':'北达科他州','OH':'俄亥俄州','OK':'俄克拉何马州','OR':'俄勒冈州','PA':'宾夕法尼亚州','RI':'罗得岛州',
 'SC':'南卡罗来纳州','SD':'南达科他州','TN':'田纳西州','TX':'得克萨斯州','UT':'犹他州','VT':'佛蒙特州','VA':'弗吉尼亚州','WA':'华盛顿州',
 'WV':'西弗吉尼亚州','WI':'威斯康星州','WY':'怀俄明州'}

# 跨越 180° 经线或为群岛的州：县几何中心的平均值会偏离，使用州的地理中心
STATE_CENTER = {'AK':(-152.0, 64.2), 'HI':(-157.4, 20.6)}

# 常见的另一种中文写法 / 简称（只用于搜索）
US_ALT = {'TX':'德克萨斯 德州','CA':'加州','NY':'纽约','FL':'佛州 佛罗里达','WA':'华州','MA':'麻省 麻州','PA':'宾州','NJ':'新州','IL':'伊州','MI':'密州',
  'NC':'北卡','SC':'南卡','ND':'北达','SD':'南达','NM':'新墨','NV':'内州','AZ':'亚州','GA':'乔治亚','HI':'夏威夷','AK':'阿拉斯加','DC':'华盛顿特区 华府','VA':'维州','OR':'俄州','CO':'科州','UT':'犹州','MD':'马州'}

def f3(v): return f'{float(v):.3f}'.rstrip('0').rstrip('.')

def china(adcode_dir):
    rows = []
    for fn in sorted((Path(adcode_dir)/'data'/'adcode').glob('*.csv')):
        with open(fn, encoding='utf-8') as fh:
            for r in csv.reader(fh):
                if len(r) < 14: continue
                try: rank = int(r[4])
                except ValueError: continue
                if rank in (1, 2, 3): rows.append(r)
    rows.sort(key=lambda r: int(r[0]))
    virtual = lambda r: r[10] == 't' or r[2] in ('市辖区', '县', '省直辖县级行政区划', '自治区直辖县级行政区划')
    P, C, D, pi, ci = [], [], [], {}, {}
    for r in rows:
        code, parent, name, rank, lon, lat = r[0], r[1], r[2], int(r[4]), r[12], r[13]
        if rank == 1:
            if not lon: continue
            pi[code] = len(P); P.append(f'{name},{f3(lon)},{f3(lat)}')
    for r in rows:
        code, parent, name, rank, lon, lat = r[0], r[1], r[2], int(r[4]), r[12], r[13]
        if rank == 2 and parent in pi:
            if virtual(r) or not lon: ci[code] = (pi[parent], -1); continue
            ci[code] = (pi[parent], len(C)); C.append(f'{name},{pi[parent]},{f3(lon)},{f3(lat)}')
    for r in rows:
        code, parent, name, rank, lon, lat = r[0], r[1], r[2], int(r[4]), r[12], r[13]
        if rank == 3 and parent in ci and lon and not virtual(r):
            p, c = ci[parent]
            D.append(f'{name},{p},{c},{f3(lon)},{f3(lat)}')
    return {'p':';'.join(P), 'c':';'.join(C), 'd':';'.join(D)}, (len(P), len(C), len(D))

def usa(spatial_dir, fips_dir):
    centers = {}
    with open(Path(spatial_dir)/'data'/'county_centers.csv', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            lon, lat = r.get('clon10') or r.get('clon00'), r.get('clat10') or r.get('clat00')
            if lon and lat and lon != 'NA': centers[int(r['fips'])] = (float(lon), float(lat))
    states = {}
    with open(Path(fips_dir)/'state_fips_master.csv', encoding='utf-8') as fh:
        for r in csv.DictReader(fh): states[r['state_abbr']] = r['state_name']
    S, si, C, acc = [], {}, [], {}
    with open(Path(fips_dir)/'county_fips_master.csv', encoding='latin-1') as fh:
        cs = list(csv.DictReader(fh))
    for r in cs:
        ab = r['state_abbr']
        if ab not in US_ZH: continue
        fips = int(r['fips'])
        if fips not in centers: continue
        acc.setdefault(ab, []).append(centers[fips])
    for ab in sorted(acc, key=lambda a: states.get(a, a)):
        pts = acc[ab]; lon = sum(p[0] for p in pts)/len(pts); lat = sum(p[1] for p in pts)/len(pts)
        if ab in STATE_CENTER: lon, lat = STATE_CENTER[ab]
        si[ab] = len(S); S.append(f'{ab},{states.get(ab, ab)},{US_ZH[ab]},{f3(lon)},{f3(lat)},{US_ALT.get(ab, "")}')
    for r in cs:
        ab = r['state_abbr']; fips = int(r['fips'])
        if ab not in si or fips not in centers: continue
        name = r['county_name'].replace(',', ' ').strip()
        C.append(f'{name},{si[ab]},{f3(centers[fips][0])},{f3(centers[fips][1])}')
    return {'s':';'.join(S), 'c':';'.join(C)}, (len(S), len(C))

def main():
    if len(sys.argv) < 4: print(__doc__); sys.exit(1)
    cn, ncn = china(sys.argv[1]); us, nus = usa(sys.argv[2], sys.argv[3])
    data = json.dumps({'v':'cn-2016+us-2010', 'cn':cn, 'us':us}, ensure_ascii=False, separators=(',', ':'))
    out = ROOT/'blocks'/'06-admin-divisions.html'
    out.write_text('<script>\n/* ── 块 06 · 中国 / 美国行政区划搜索库（由 tools/make_admin.py 生成，不要手改）──\n'
                   f'   中国：省级 {ncn[0]} · 地级 {ncn[1]} · 县级 {ncn[2]}（Vonng/adcode：国家统计局 2016 区划 + 高德地理中心）\n'
                   f'   美国：州 {nus[0]} · 县 {nus[1]}（美国人口普查局 2010 县几何中心 via btskinner/spatial + kjhealy/fips-codes）*/\n'
                   f'window.SB = window.SB || {{}};\nSB.ADMIN_DIVISIONS = {data};\n</script>\n', encoding='utf-8')
    print('cn', ncn, 'us', nus, 'bytes', out.stat().st_size)

if __name__ == '__main__':
    main()
