"""Kiểm một kho văn bản theo bộ tiêu chuẩn cào lọc M8 (QĐ-18), lớp 3 (từng văn bản) và lớp 4 (cân bằng tập).
Chạy trên kho hiện có để lấy mốc, và sau mỗi đợt cào để biết đợt đó có làm chỉ số nhích không.
Dùng: python3 scripts/kiem_dot_cao.py [corpus.jsonl] [--ten <tên đợt>]   → ket_qua/dot_cao/<tên>.json và in bảng
"""
import json, re, os, sys, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import m8_lam_sach as LS
a = [x for x in sys.argv[1:] if not x.startswith('--')]
P = a[0] if a else os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl')
TEN = sys.argv[sys.argv.index('--ten') + 1] if '--ten' in sys.argv else 'moc_kho_v4'
C = [json.loads(l) for l in open(P, encoding='utf-8')]
nfc = lambda s: unicodedata.normalize('NFC', s)
def am(s): return [w for w in re.findall(r'[0-9a-zà-ỹđ]+', nfc(s).lower()) if not w.isdigit()]
TD = collections.Counter(w for c in C for w in am(c['text'][:3000])); TD = {w for w, n in TD.items() if n >= 20}
LOAI_SOAN = ['Công văn', 'Quyết định (cá biệt)', 'Thông báo', 'Công điện', 'Chỉ thị', 'Tờ trình', 'Báo cáo', 'Kế hoạch']
# nhiễu tối đa hiệu chỉnh trên kho v4: ngưỡng 2% loại 24% kho, 3% là phân vị 90 (QĐ-18)
NGUONG = {'nhieu_toi_da': 0.03, 'khop_trich_yeu_toi_thieu': 0.9, 'loai_toi_thieu': 0.08, 'loai_toi_da': 0.35, 'sau_sap_nhap_toi_thieu': 0.40,
          'co_quan_toi_thieu': 6, 'nguoi_ky_toi_da': 0.03}

def lop3(c):
    w = am(c['text']); nhieu = 1 - sum(x in TD for x in w) / max(1, len(w))
    try: khop = json.loads(c['doi_chieu'].replace("'", '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')).get('trung_trich_yeu')
    except Exception: khop = None
    if khop is None:
        ws = set(w); ty = am(c.get('trich_yeu', '')); khop = sum(x in ws for x in ty) / max(1, len(ty))
    return {'nhieu': nhieu, 'khop_trich_yeu': khop, 'trung': bool(c.get('gan_trung_mau_voi')), 'cho_xac_minh': bool(c.get('cho_xac_minh'))}

L3 = [lop3(c) for c in C]
dat3 = [c for c, r in zip(C, L3) if r['nhieu'] <= NGUONG['nhieu_toi_da'] and (r['khop_trich_yeu'] or 0) >= NGUONG['khop_trich_yeu_toi_thieu'] and not r['trung']]
# lớp 4, tính trên các văn bản đạt lớp 3 và thuộc nhóm loại dùng để soạn
S = [c for c in dat3 if c.get('loai_van_ban') in LOAI_SOAN]
loai = collections.Counter(c['loai_van_ban'] for c in S); n = max(1, len(S))
ty_le_loai = {k: round(loai.get(k, 0) / n, 3) for k in LOAI_SOAN}
sau = sum(c['ngay_ban_hanh'] >= '2025-03-01' for c in S if c.get('ngay_ban_hanh')) / n
co_quan = collections.Counter(c.get('co_quan_ky_hieu') or c.get('nguon') for c in S)
ky = collections.Counter()
for c in S:
    duoi = c['text'][-1500:]
    for m in re.finditer(rf'(?<![\w\[])(?:{LS.HO})(?:[ \t]+{LS.AM}){{1,3}}(?![a-zà-ỹđ])', duoi):
        t = re.sub(r'\s+', ' ', m.group(0))
        if not LS.la_dia_danh(t) and len(t.split()) >= 3: ky[t] += 1; break
dau_ky, so_ky = ky.most_common(1)[0] if ky else ('', 0)
KQ = {'ten_dot': TEN, 'tep': P, 'so_van_ban': len(C),
      'lop3': {'dat': len(dat3), 'ty_le_dat': round(len(dat3) / len(C), 3),
               'loai_vi_nhieu': sum(r['nhieu'] > NGUONG['nhieu_toi_da'] for r in L3),
               'loai_vi_khong_khop_chi_muc': sum((r['khop_trich_yeu'] or 0) < NGUONG['khop_trich_yeu_toi_thieu'] for r in L3),
               'loai_vi_trung': sum(r['trung'] for r in L3), 'cho_nguoi_xac_minh': sum(r['cho_xac_minh'] for r in L3)},
      'lop4': {'so_van_ban_soan': len(S), 'ty_le_loai': ty_le_loai, 'sau_sap_nhap': round(sau, 3), 'so_co_quan': len(co_quan),
               'co_quan_lon_nhat': co_quan.most_common(3), 'nguoi_ky_nhieu_nhat': [dau_ky, round(so_ky / n, 3)]},
      'nguong': NGUONG}
KQ['danh_gia'] = {
    'loai_thieu': [k for k, v in ty_le_loai.items() if v < NGUONG['loai_toi_thieu']],
    'loai_qua_tai': [k for k, v in ty_le_loai.items() if v > NGUONG['loai_toi_da']],
    'sau_sap_nhap_dat': sau >= NGUONG['sau_sap_nhap_toi_thieu'],
    'co_quan_dat': len(co_quan) >= NGUONG['co_quan_toi_thieu'],
    'nguoi_ky_dat': so_ky / n <= NGUONG['nguoi_ky_toi_da']}
os.makedirs('ket_qua/dot_cao', exist_ok=True)
json.dump(KQ, open(f'ket_qua/dot_cao/{TEN}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(KQ, ensure_ascii=False, indent=1))
