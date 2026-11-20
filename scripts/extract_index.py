"""Vòng 2: trích chỉ mục từ snapshot danh sách. Mỗi giá trị kèm đoạn verbatim lấy đúng vị trí
trong HTML thô. Phân loại văn bản suy từ số ký hiệu theo cấu trúc ký hiệu của Nghị định 30/2020
(văn bản hành chính) và Luật Ban hành VBQPPL (có năm trong ký hiệu)."""
import re, json, glob, os, csv, sys, html, datetime as dt
SNAP = sys.argv[1]; OUT = sys.argv[2]
ROW = re.compile(r"<tr>\s*<td>\s*<a href='/\?pageid=27160&docid=(\d+)'>\s*<span class=\"code\">([^<]*)</span>(.*?)</tr>", re.S)
def classify(code):
    c = code.strip().replace('\u00d0', '\u0110')  # Ð (Latin Eth) gõ nhầm cho Đ
    c = re.sub(r'\s*/\s*', '/', c); c = re.sub(r'\s*-\s*', '-', c); c = c.replace('_', '-')
    if re.search(r'/\d{4}/(QH|UBTVQH)\d+$', c): return 'Luật/Nghị quyết Quốc hội', 'VBQPPL', 'QH'
    if '/VBHN-' in c: return 'Văn bản hợp nhất', 'Hợp nhất', c.split('-')[-1]
    m = re.match(r'^\s*([\dA-Za-z./]+?)/(\d{4})/([A-ZĐa-z]+)-(.+)$', c)
    if m:  # có năm → VBQPPL hoặc VBHN
        kind = m.group(3); org = m.group(4)
        names = {'NĐ': 'Nghị định', 'QĐ': 'Quyết định (QPPL)', 'TT': 'Thông tư', 'NQ': 'Nghị quyết (QPPL)', 'VBHN': 'Văn bản hợp nhất', 'TTLT': 'Thông tư liên tịch', 'L': 'Luật', 'PL': 'Pháp lệnh', 'QH': 'Luật/NQ Quốc hội'}
        return names.get(kind, f'QPPL khác ({kind})'), 'VBQPPL' if kind != 'VBHN' else 'Hợp nhất', org
    m = re.match(r'^\s*[\dA-Za-z./]+/([A-ZĐ]{1,5})-(.+)$', c)
    if m:
        kind, org = m.group(1), m.group(2)
        names = {'QĐ': 'Quyết định (cá biệt)', 'CT': 'Chỉ thị', 'CĐ': 'Công điện', 'TB': 'Thông báo', 'BC': 'Báo cáo', 'TTr': 'Tờ trình', 'KH': 'Kế hoạch', 'NQ': 'Nghị quyết (cá biệt)', 'HD': 'Hướng dẫn', 'CTr': 'Chương trình', 'QC': 'Quy chế', 'QyĐ': 'Quy định', 'PA': 'Phương án', 'ĐA': 'Đề án', 'BB': 'Biên bản', 'GM': 'Giấy mời', 'TTr': 'Tờ trình'}
        if kind in names: return names[kind], 'Hành chính', org
    m = re.match(r'^\s*[\dA-Za-z./]+/([A-ZĐa-z]+)-([A-ZĐa-z0-9.&]+)$', c)
    if m:  # số/CƠQUAN-ĐƠNVỊ → công văn
        return 'Công văn', 'Hành chính', m.group(1)
    return 'Chưa phân loại', 'Chưa rõ', ''
rows, seen = [], {}
pages = sorted(glob.glob(os.path.join(SNAP, 'p*.html')))
for p in pages:
    raw = open(p, encoding='utf-8').read(); name = os.path.basename(p)
    for m in ROW.finditer(raw):
        docid, code, rest = m.group(1), html.unescape(m.group(2)).strip(), m.group(3)
        d = re.search(r'<span class="issued-date">(\d\d/\d\d/\d{4})</span>', rest)
        t = re.search(r'<span class="substract">(.*?)</span>', rest, re.S)
        files = re.findall(r'<a href="(https?://[^"]+)"[^>]*download', rest)
        if not d: continue
        dd, mm, yy = d.group(1).split('/')
        loai, hinh_thuc, coquan = classify(code)
        ky_tu_la = '\u00d0' in code
        sai_dinh_dang = bool(re.search(r'\s/|/\s|\s-|-\s|_|\s{2,}', code)) or ky_tu_la
        rec = {'docid': docid, 'so_ky_hieu': code, 'ngay_ban_hanh': f'{yy}-{mm}-{dd}', 'trich_yeu': html.unescape(re.sub(r'\s+', ' ', t.group(1)).strip()) if t else '',
               'tep': files, 'loai_van_ban': loai, 'hinh_thuc': hinh_thuc, 'co_quan_ky_hieu': coquan, 'ky_tu_la_trong_ky_hieu': ky_tu_la, 'ky_hieu_sai_trinh_bay': sai_dinh_dang, 'snapshot': name,
               'span_code': m.group(0)[:m.group(0).find('</span>') + 7][m.group(0).find('docid='):],
               'span_date': d.group(0), 'span_trich': t.group(0) if t else '', 'span_files': [re.search(r'<a href="' + re.escape(f) + r'"', rest).group(0) for f in files]}
        if docid in seen:
            seen[docid]['dup_pages'].append(name); continue
        rec['dup_pages'] = []; seen[docid] = rec; rows.append(rec)
cut = '2020-03-05'
inrange = [r for r in rows if r['ngay_ban_hanh'] >= cut]
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'index_all_rows.jsonl'), 'w', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
print('pages', len(pages), 'rows unique', len(rows), 'in range', len(inrange), 'dup docids', sum(1 for r in rows if r['dup_pages']))
from collections import Counter
print(Counter(r['loai_van_ban'] for r in inrange).most_common(30))
print(Counter(r['hinh_thuc'] for r in inrange))
print(Counter(r['ngay_ban_hanh'][:4] for r in inrange))
print('no file', sum(1 for r in inrange if not r['tep']))
unk = [r['so_ky_hieu'] for r in inrange if r['loai_van_ban'] == 'Chưa phân loại']
print('unclassified', len(unk), unk[:60]); print('sai trinh bay', sum(1 for r in inrange if r['ky_hieu_sai_trinh_bay'])); print('Ð instead of Đ', sum(1 for r in inrange if r['ky_tu_la_trong_ky_hieu']))
