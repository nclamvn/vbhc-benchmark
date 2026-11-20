"""Xuất tệp bàn giao vòng 2. Trích yếu trong tệp công bố được che họ tên người dân như toàn văn; bản gốc giữ trong gói kiểm lại."""
import json, csv, os, re, sys
sys.argv = ['x']; ns = {}
src = open('scripts/reconcile_clean_v2.py', encoding='utf-8').read()
exec(src[:src.index('corpus, rejects, dc = []')].replace("idx = {", "_unused = {", 1).split("plan = set()")[0].replace("_unused = {json.loads(l)['docid']: dict(json.loads(l), nguon='vanban.chinhphu.vn') for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8')}", ""), ns) if False else None
NAMEW = r'[A-ZĐÂĂÊÔƠƯÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ][a-zà-ỹđ]+'
HON = re.compile(r'\b(ông|bà|Ông|Bà|anh|chị|cụ|cháu)(\s+)(' + NAMEW + r'(?:\s' + NAMEW + r'){1,4})')
ADDR = re.compile(r'((?:địa chỉ|thường trú|trú tại)\s*(?:tại)?\s*:?\s*)([^;\n()]{4,140})')
def red(t): return ADDR.sub(lambda m: m.group(1) + '[ĐỊA CHỈ]', HON.sub(lambda m: m.group(1) + m.group(2) + '[HỌ TÊN]', t))
O = 'out_v2'; os.makedirs(O, exist_ok=True)
rows = [dict(json.loads(l), nguon='vanban.chinhphu.vn') for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8')]
rows = [r for r in rows if r['ngay_ban_hanh'] >= '2020-03-05'] + [json.loads(l) for l in open('data/prov/index_prov.jsonl', encoding='utf-8') if json.loads(l)['ngay_ban_hanh'] >= '2020-03-05']
with open(f'{O}/chi_muc_van_ban_v2.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['nguon', 'cap', 'docid', 'so_ky_hieu', 'ngay_ban_hanh', 'trich_yeu', 'loai_van_ban', 'hinh_thuc', 'co_quan_ky_hieu', 'co_quan_ten', 'ky_hieu_sai_trinh_bay', 'tep_dinh_kem_dau', 'trang_danh_sach'])
    for r in rows:
        w.writerow([r['nguon'], 'Trung ương' if r['nguon'] == 'vanban.chinhphu.vn' else 'Tỉnh', r['docid'], r['so_ky_hieu'], r['ngay_ban_hanh'], red(r['trich_yeu']), r['loai_van_ban'], r['hinh_thuc'], r['co_quan_ky_hieu'], r.get('co_quan_ten', ''), int(r.get('ky_hieu_sai_trinh_bay', False)), r['tep'][0] if r['tep'] else '', r['snapshot']])
C = [json.loads(l) for l in open('data/stage4_v2/corpus.jsonl', encoding='utf-8')]
with open(f'{O}/toan_van_v2.jsonl', 'w', encoding='utf-8') as f:
    for c in C:
        c = dict(c); c.pop('snapshot', None); c['trich_yeu'] = red(c['trich_yeu']); f.write(json.dumps(c, ensure_ascii=False) + '\n')
dc = [json.loads(l) for l in open('data/stage4_v2/doi_chieu.jsonl', encoding='utf-8')]
with open(f'{O}/doi_chieu_toan_van_v2.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['docid', 'so_ky_hieu_chi_muc', 'trang_thai_so_ky_hieu', 'so_doc_tu_toan_van', 'so_trong_ten_tep_khop', 'ten_tep', 'ngay_chi_muc', 'ngay_khop', 'trung_trich_yeu', 'boc_chu', 'do_tin_ocr'])
    for x in dc: w.writerow([x['docid'], x['so_ky_hieu_chi_muc'], x['trang_thai_so_ky_hieu'], ' | '.join(x['so_trong_van_ban']), int(x['so_trong_ten_tep_khop']), x['ten_tep'], x['ngay_chi_muc'], int(x['ngay_khop']), x.get('trung_trich_yeu'), x['method'], x['conf']])
R = [json.loads(l) for l in open('data/stage4_v2/rejects.jsonl', encoding='utf-8')]
with open(f'{O}/loai_bo_v2.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['docid', 'so_ky_hieu', 'buoc', 'ly_do', 'chi_tiet'])
    for r in R: w.writerow([r['docid'], r['so_ky_hieu'], r['stage'], r['reason'], json.dumps({k: v for k, v in r.items() if k not in ('docid', 'so_ky_hieu', 'stage', 'reason')}, ensure_ascii=False)])
rev = []
for x in dc:
    if not x['so_trong_ten_tep_khop']: rev.append([x['docid'], x['so_ky_hieu_chi_muc'], 'Số trong tên tệp khác chỉ mục (hoặc tên tệp không có số)', x['ten_tep'] + ' / toàn văn: ' + ' | '.join(x['so_trong_van_ban'])])
    elif x['trang_thai_so_ky_hieu'] == 'khac': rev.append([x['docid'], x['so_ky_hieu_chi_muc'], 'Số đọc từ toàn văn khác chỉ mục (thường do số viết tay)', ' | '.join(x['so_trong_van_ban'])])
for r in rows:
    if r.get('ky_hieu_sai_trinh_bay'): rev.append([r['docid'], r['so_ky_hieu'], 'Ký hiệu trình bày sai trong chỉ mục', r['nguon']])
    if r['loai_van_ban'] == 'Chưa phân loại': rev.append([r['docid'], r['so_ky_hieu'], 'Ký hiệu không theo mẫu đã biết, chưa phân loại', r['nguon']])
with open(f'{O}/can_nguoi_xem_v2.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['docid', 'so_ky_hieu', 'ly_do', 'chi_tiet']); w.writerows(rev)
print('index rows', len(rows), 'corpus', len(C), 'rejects', len(R), 'review', len(rev))
