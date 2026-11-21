"""M1: dựng bộ cài lỗi (mỗi văn bản một lỗi đã biết) từ văn bản thật đạt mọi luật, rồi đo luật bắt được bao nhiêu.
Dùng: python3 scripts/m1_danh_gia.py <seed> <tệp ra>"""
import json, sys, random, re, copy
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
C = [json.loads(l) for l in open('data/stage4_v3/corpus.jsonl', encoding='utf-8')]
D = re.compile(r'ngày \d\d tháng \d\d năm \d{4}')
ok = [c for c in C if v1.du_trang(c) and not any(v2.kiem(c).values()) and D.search(v1.vung_dau(c['text'])) and 'Độc lập - Tự do - Hạnh phúc' in c['text'][:1500] and re.search(r'Số: \d', c['text'][:2000]) and 'Nơi nhận' in c['text'] and 'Lưu: VT' in c['text'] and './.' in c['text'] and re.search(r'CỘNG HO[ÀÒ]A? XÃ HỘI CHỦ NGHĨA VIỆT NAM', c['text'][:1500])]
named = [c for c in ok if c['loai_van_ban'] != 'Công văn']; cv = [c for c in ok if c['loai_van_ban'] == 'Công văn']
def mut(c, kind):
    d = copy.deepcopy(c); t = d['text']; vd = v1.vung_dau(t); H = t[:len(vd)]; R = t[len(vd):]
    def sub(p, r, x):
        y = re.sub(p, r, x, count=1); assert y != x; return y
    if kind == 'quoc_hieu_viet_tat': H = sub(r'CỘNG HO[ÀÒ]A? XÃ HỘI CHỦ NGHĨA VIỆT NAM', 'CHXHCN VIỆT NAM', H); exp = 'L01'
    elif kind == 'tieu_ngu_hoa_sai': H = sub('Độc lập - Tự do - Hạnh phúc', 'Độc Lập - Tự Do - Hạnh Phúc', H); exp = 'L13'
    elif kind == 'so_thieu_hai_cham': H = sub(r'Số: (\d)', r'Số \1', H); exp = 'L03'
    elif kind == 'ky_hieu_dao':
        a, b = d['so_ky_hieu_chuan'].split('/', 1); p = b.split('-', 1); d['so_ky_hieu_chuan'] = f'{a}/{p[1]}-{p[0]}'; H = H.replace(b, f'{p[1]}-{p[0]}'); exp = 'L14'
    elif kind == 'ngay_dang_so': H = sub(r'ngày (\d\d) tháng (\d\d) năm (\d{4})', r'\1/\2/\3', H); exp = 'L05'
    elif kind == 'ngay_thieu_so_0': H = sub(r'ngày \d\d tháng \d\d năm (\d{4})', r'ngày 5 tháng 2 năm \1', H); exp = 'L15'
    elif kind == 'ten_loai_viet_thuong':
        ten = d['loai_van_ban'].split(' (')[0].upper(); H = sub(r'(?m)^(\s*)' + ten + r'\s*$', lambda m: m.group(1) + ten.capitalize(), H); exp = 'L06'
    elif kind == 'cong_van_thieu_trich_yeu':
        t2 = re.sub(r'V\s*/\s*v|Về việc', '', t[:2500]); assert t2 != t[:2500]; H, R = t2, t[2500:]; exp = 'L07'
    elif kind == 'thieu_noi_nhan': H, R = t.replace('Nơi nhận:', '').replace('Nơi nhận', ''), ''; exp = 'L09'
    elif kind == 'luu_sai': H, R = t.replace('Lưu: VT', 'Lưu: VP'), ''; exp = 'L10'
    elif kind == 'thieu_ket_thuc': H, R = re.sub(r'\.\s*[/⁄]\s*\.', '.', t), ''; exp = 'L12'
    d['text'] = H + R; return d, exp
kn = ['quoc_hieu_viet_tat', 'tieu_ngu_hoa_sai', 'so_thieu_hai_cham', 'ky_hieu_dao', 'ngay_dang_so', 'ngay_thieu_so_0', 'ten_loai_viet_thuong', 'thieu_noi_nhan', 'luu_sai', 'thieu_ket_thuc']
plan = [(k, 'n') for k in kn] + [('cong_van_thieu_trich_yeu', 'c')] * 2 + [(k, 'c') for k in ['quoc_hieu_viet_tat', 'tieu_ngu_hoa_sai', 'so_thieu_hai_cham', 'ngay_dang_so', 'ngay_thieu_so_0', 'thieu_noi_nhan', 'luu_sai', 'thieu_ket_thuc']]
rng = random.Random(int(sys.argv[1])); rng.shuffle(named); rng.shuffle(cv); out = []
for k, pool in plan:
    src = named if pool == 'n' else cv
    while True:
        c = src.pop()
        try: d, exp = mut(c, k); break
        except AssertionError: continue
    r2 = sorted(x for x, y in v2.kiem(d).items() if y and y != v1.KXD)
    out.append({'goc': c['docid'], 'loai_van_ban': d['loai_van_ban'], 'loi_cai': k, 'luat_mong_doi': exp, 'so_ky_hieu_chuan': d['so_ky_hieu_chuan'], 'bao': r2, 'text': d['text']})
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False)
print('seed', sys.argv[1], '| bắt đúng luật:', sum(o['luat_mong_doi'] in o['bao'] for o in out), '/', len(out), '| cờ thừa:', sum(len(set(o['bao']) - {o['luat_mong_doi']}) for o in out), '| sót:', [(o['loi_cai'], o['goc']) for o in out if o['luat_mong_doi'] not in o['bao']])
