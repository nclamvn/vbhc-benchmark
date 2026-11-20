"""Trích chỉ mục ba cổng tỉnh, mỗi giá trị kèm đoạn HTML gốc. Dùng chung bộ phân loại ký hiệu với Cổng Chính phủ."""
import re, json, glob, os, html, sys
sys.argv = ['x', 'data/snapshots/list', '/tmp/_unused']
src = open('scripts/extract_index.py', encoding='utf-8').read().split('rows, seen = [], {}')[0]
ns = {}; exec(src, ns); classify = ns['classify']
NAMEW = r'[A-ZĐÂĂÊÔƠƯÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ][a-zà-ỹđ]+'
PERSONAL = re.compile(r'\b(ông|bà|Ông|Bà|anh|chị|cụ|cháu|hộ ông|hộ bà)\s+' + NAMEW + r'(\s' + NAMEW + r'){1,4}')
def row(src, did, code, date, trich, files, snap, spans, coquan_ten=''):
    dd, mm, yy = date.split('/'); loai, ht, cq = classify(html.unescape(code).strip())
    return {'nguon': src, 'docid': did, 'so_ky_hieu': html.unescape(code).strip(), 'ngay_ban_hanh': f'{yy}-{mm}-{dd}', 'trich_yeu': html.unescape(re.sub(r'\s+', ' ', trich)).strip(),
            'tep': files, 'loai_van_ban': loai, 'hinh_thuc': ht, 'co_quan_ky_hieu': cq, 'co_quan_ten': coquan_ten, 'snapshot': snap, 'spans': spans,
            've_ca_nhan_cu_the': bool(PERSONAL.search(html.unescape(trich)))}
out = []
for p in sorted(glob.glob('data/prov/tn/p*.html')):
    s = open(p, encoding='utf-8').read(); n = os.path.basename(p)
    for i in sorted(set(re.findall(r'lbSoHieuVB_(\d+)"', s)), key=int):
        code = re.search(rf'lbSoHieuVB_{i}">([^<]*)<', s); date = re.search(rf'lbNgayBanHanh_{i}">([^<]*)<', s)
        seg = s[date.end(): s.find(f'lbSoHieuVB_{int(i) + 1}"', date.end()) if f'lbSoHieuVB_{int(i) + 1}"' in s else date.end() + 4000]
        det = re.search(r'href="(/\?pageid=27218&(?:amp;)?p_steering=(\d+))"', seg); tr = re.search(r'<span class="summary">(.*?)</span>', seg, re.S)
        fl = re.findall(r"href='(https://storage-vnportal\.vnpt\.vn/[^']+)' class=\"download\"", seg)
        if not (code and date and det): continue
        out.append(row('thainguyen.gov.vn', 'tn-' + det.group(2), code.group(1), date.group(1), tr.group(1) if tr else '', fl, n, {'code': code.group(0), 'date': date.group(0)}))
for p in sorted(glob.glob('data/prov/hy/p*.html')):
    s = open(p, encoding='utf-8').read(); n = os.path.basename(p)
    for m in re.finditer(r'<tr><td>(\d+)</td><td><strong>([^<]*)</strong></td><td>(.*?)</td>.*?Ngày ban hành:</strong>\s*(\d\d/\d\d/\d{4})</p>(.*?)</tr>', s, re.S):
        fl = ['https://hungyen.gov.vn' + f for f in re.findall(r'href="(/upload/[^"]+)"', m.group(5))]
        cq = re.search(r'Cơ quan ban hành:</strong>\s*([^<]*)<', m.group(0))
        did = 'hy-' + re.sub(r'\W+', '_', m.group(2)) + '-' + m.group(4).replace('/', '')
        out.append(row('hungyen.gov.vn', did, m.group(2), m.group(4), m.group(3), fl, n, {'code': f'<strong>{m.group(2)}</strong>', 'date': m.group(4)}, cq.group(1).strip() if cq else ''))
for p in sorted(glob.glob('data/prov/qt/p*.html')):
    s = open(p, encoding='utf-8').read(); n = os.path.basename(p)
    blocks = re.split(r'(?=href="/van-ban/[0-9a-f-]{36}")', s)[1:]
    for bl in blocks:
        bl = bl[:4000]; idm = re.match(r'href="/van-ban/([0-9a-f-]{36})"', bl)
        p1 = re.search(r'(<p class="min-w-0 truncate[^>]*>)(.*?)</p>', bl, re.S); tm = re.search(r'dateTime="(\d{4})-(\d\d)-(\d\d)"', bl)
        p2 = re.search(r'</time></div><p[^>]*>(.*?)</p>', bl, re.S)
        if not (idm and p1 and tm): continue
        label = html.unescape(re.sub(r'<[^>]+>', '', p1.group(2))).strip(); code = label.split(' số ', 1)[1].strip() if ' số ' in label else label
        out.append(row('tracuuvanban.quangtri.gov.vn', 'qt-' + idm.group(1), code, f'{tm.group(3)}/{tm.group(2)}/{tm.group(1)}', p2.group(1) if p2 else '', [], n, {'code': p1.group(2), 'date': tm.group(0)}, 'UBND tỉnh Quảng Trị'))
seen = set(); uniq = []
for r in out:
    if r['docid'] in seen: continue
    seen.add(r['docid']); uniq.append(r)
open('data/prov/index_prov.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in uniq))
from collections import Counter
print(Counter(r['nguon'] for r in uniq)); print(Counter((r['nguon'][:6], r['hinh_thuc']) for r in uniq))
print('ve ca nhan', Counter(r['nguon'][:6] for r in uniq if r['ve_ca_nhan_cu_the'])); print('co tep', Counter(r['nguon'][:6] for r in uniq if r['tep']))
print('date range', min(r['ngay_ban_hanh'] for r in uniq), max(r['ngay_ban_hanh'] for r in uniq))
print(Counter(r['loai_van_ban'] for r in uniq).most_common(12))
