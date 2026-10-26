"""把 Highcharts 世界地图（topojson，经纬度）转成网页内嵌的精简数据块 blocks/06-world-data.html。
数据来源：@highcharts/map-collection（基于 Natural Earth / OpenStreetMap），仅作个人非商业使用。"""
import json, math, sys
src = sys.argv[1]; out = sys.argv[2]; maps_list = sys.argv[3].split(',')
d = json.load(open(src))
tf = d['transform']; sx, sy = tf['scale']; tx, ty = tf['translate']
arcs = []
for a in d['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x*sx+tx, y*sy+ty))
    arcs.append(pts)
def ring(idx):
    pts = []
    for i in idx:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(a if not pts else a[1:])
    return pts
def dp(pts, tol):
    if len(pts) < 4: return pts
    keep = [False]*len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts)-1)]
    while stack:
        a, b = stack.pop(); (x1,y1),(x2,y2) = pts[a], pts[b]; dmax = -1; im = a
        L = math.hypot(x2-x1, y2-y1) or 1e-9
        for i in range(a+1, b):
            x0,y0 = pts[i]; dd = abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/L
            if dd > dmax: dmax, im = dd, i
        if dmax > tol: keep[im] = True; stack += [(a,im),(im,b)]
    return [p for p,k in zip(pts,keep) if k]
def area(r):
    return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
TOL = .03; Q = 50
CONT = {'Asia':'as','Europe':'eu','Africa':'af','North America':'na','South America':'sa','Oceania':'oc'}
SEVEN = {'sc':'af','mu':'af','mv':'as'}
geoms = list(d['objects'].values())[0]['geometries']
res = []
for g in geoms:
    p = g['properties']; k = p['hc-key']
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    rings = []
    for poly in polys:
        for ri, r in enumerate(poly[:1]):  # 只要外环
            rr = ring(r); h = len(rr)//2
            pts = dp(rr[:h+1], TOL)[:-1] + dp(rr[h:], TOL)
            if len(pts) < 4 or area(pts) < .004: continue
            q = [(round(x*Q), round(y*Q)) for x,y in pts]
            enc = [q[0][0], q[0][1]]
            for i in range(1,len(q)): enc += [q[i][0]-q[i-1][0], q[i][1]-q[i-1][1]]
            rings.append(enc)
    c = CONT.get(p.get('continent'), SEVEN.get(k, 'oc'))
    a2 = (p.get('iso-a2') or '').upper() if p.get('iso-a2') and len(p.get('iso-a2'))==2 else ''
    res.append({'k':k,'a2':a2,'n':p.get('name'),'c':c,'m':[p.get('hc-middle-lon'),p.get('hc-middle-lat')],'p':rings})
js = json.dumps({'q':Q,'countries':res,'maps':maps_list}, ensure_ascii=False, separators=(',',':'))
open(out,'w',encoding='utf-8').write(
"<script>\n/* ── 块 06 · 世界地理数据（由 tools/make_world.py 生成，请勿手改）──\n"
"   国家轮廓：经纬度 ×q 后差分编码；c = 大洲代码 as/eu/af/na/sa/oc；maps = 有省级地图的国家。\n"
"   数据来源：Highcharts Map Collection（Natural Earth / OpenStreetMap），个人非商业使用。 */\n"
"window.SB = window.SB || {};\nSB.WORLD_RAW = " + js + ";\n</script>\n")
print(len(res), 'countries', len(js)//1024, 'KB')
