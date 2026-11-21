"""Ba mốc không dùng mô hình ngôn ngữ, để biết sàn và trần của bộ đánh giá:
(1) dap_an: trả đúng đáp án (kiểm bộ chấm, phải ra 100 ở T2, T3); (2) rong: trả lời rỗng; (3) luat: biểu thức chính quy và bộ luật M1."""
import json, re, sys
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
D = [json.loads(l) for l in open('m3/test_de.jsonl', encoding='utf-8')]; G = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')}
TL = {v: k for k, v in v2.TL.items()}; M = {'L01': 'quoc_hieu_viet_tat', 'L13': 'tieu_ngu_hoa_sai', 'L03': 'so_thieu_hai_cham', 'L14': 'ky_hieu_dao', 'L05': 'ngay_dang_so', 'L15': 'ngay_thieu_so_0', 'L06': 'ten_loai_viet_thuong', 'L07': 'cong_van_thieu_trich_yeu', 'L09': 'thieu_noi_nhan', 'L10': 'luu_sai', 'L12': 'thieu_ket_thuc'}
def ma(t):
    m = re.search(r'S[ốô]\s*:?\s*(\d+[a-z]?\s*/\s*[A-Za-zĐđ0-9&.\-]+)', v1.vung_dau(t)); return re.sub(r'\s+', '', m.group(1)) if m else ''
def loai(code):
    p = code.split('/', 1)[-1].split('-')
    if p and p[0] in TL: return TL[p[0]], False
    if len(p) > 1 and p[-1] in TL: return TL[p[-1]], True
    return 'Công văn', False
def t2(t):
    code = ma(t); lo, dao = loai(code)
    if dao: return 'ky_hieu_dao'
    k = v2.kiem({'text': t, 'so_ky_hieu_chuan': code or '0/X', 'loai_van_ban': lo})
    for L in ['L01', 'L13', 'L03', 'L05', 'L15', 'L06', 'L07', 'L09', 'L10', 'L12', 'L14']:
        if k.get(L) and k[L] != v1.KXD: return M[L]
    return 'KHONG_LOI'
def t3(t):
    code = ma(t); lo, _ = loai(code); vd = v1.vung_dau(t)
    m = re.search(r'ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})', vd); ng = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}' if m else ''
    if lo == 'Công văn': m2 = re.search(r'(V\s*/\s*v[^\n]*(?:\n[^\n]{3,60}){0,4}?)\n\s*\n', t[:2500]); ty = m2.group(1) if m2 else ''
    else:
        ten = lo.split(' (')[0].upper(); m2 = re.search(r'(?m)^\s*' + ten + r'\s*\n((?:[^\n]+\n){1,4}?)\s*\n', t[:3000]); ty = m2.group(1) if m2 else ''
    return {'so_ky_hieu': code, 'ngay_ban_hanh': ng, 'loai_van_ban': lo, 'trich_yeu': re.sub(r'\s+', ' ', ty).strip()}
for ten in ['dap_an', 'rong', 'luat']:
    with open(f'm3/moc_{ten}.jsonl', 'w', encoding='utf-8') as f:
        for d in D:
            g = G[d['id']]['dap_an']; t = d['de'].split('VĂN BẢN:\n', 1)[-1]
            if ten == 'rong': a = ''
            elif ten == 'dap_an': a = g['van_ban_tham_chieu'] if d['nhiem_vu'] == 'T1' else json.dumps(g, ensure_ascii=False)
            else: a = '' if d['nhiem_vu'] == 'T1' else json.dumps({'loi': t2(t)} if d['nhiem_vu'] == 'T2' else t3(t), ensure_ascii=False)
            f.write(json.dumps({'id': d['id'], 'tra_loi': a}, ensure_ascii=False) + '\n')
