"""M8.1 · Tập huấn luyện v7, dựng lại từ kho v4 hiện có, không cào thêm (QĐ-18).
Sửa ba lỗi của tập cũ:
1. Bể soạn văn bản (T1) bỏ sót gần hết chỉ thị (2/262), quyết định, công điện vì bộ lọc đòi số và ngày trong toàn văn OCR phải đọc được.
   Số, ngày thường viết tay hoặc nằm dưới dấu đỏ nên OCR hỏng. v7 nhận cả văn bản "số gần khớp / không đọc được" nếu trích yếu khớp chỉ mục ≥ 80%,
   rồi viết lại dòng "Số:" và dòng "ngày … tháng … năm …" ở phần đầu theo chỉ mục (chỉ mục là nguồn sự thật cho siêu dữ liệu).
   Không tìm thấy dòng "Số" ở phần đầu thì bỏ văn bản, không dựng khung giả.
2. Che tên bằng scripts/m8_lam_sach.py (không còn che nhầm "Hà Nội", "Bộ Tài").
3. Cân bằng loại: công văn tối đa 35% bể T1; tư liệu tra cứu và bảng bộ máy đọc từ sổ SOT v1 (có Thủ tướng, Phó Thủ tướng 2026).
Phần tư liệu theo cách của v6: 70% bài có căn cứ thật trong tư liệu, 30% điều kiện tra cứu thật. T2 300, T3 300, T4 200 lấy từ m6b.
Dùng: python3 scripts/m8_du_lieu_v7.py  → m8/train.jsonl, m8/valid.jsonl, m8/thong_ke.json
"""
import json, re, os, sys, random, collections, copy
sys.path.insert(0, 'scripts')
src = open('scripts/m6_du_lieu_v2.py', encoding='utf-8').read()
G = {'__name__': 'v2_ham'}; exec(src[:src.index('def cu(p):')], G)   # dùng lại nguyên văn các hàm lọc, làm sạch, che của v2
C, SP, de_T1, msg, lam_sach_v2, che_v2, nhieu, v1, v2 = G['C'], G['SP'], G['de_T1'], G['msg'], G['lam_sach'], G['che'], G['nhieu'], G['v1'], G['v2']
if os.environ.get('VBHC_CHIA_TAP_THEM'):   # văn bản của các đợt cào M8 (chia tập riêng; nhãn 'de_moi' để ngoài huấn luyện)
    SP.update(json.load(open(os.environ['VBHC_CHIA_TAP_THEM'], encoding='utf-8')))
import tra_cuu as tcu, kiem_trung_thuc as k, m8_lam_sach as LS, sot_bo_may as SOT
tcu.SOT_BAN = 'v1'
import m7b_du_lieu_v6 as v6m   # hàm tu_lieu (đưa căn cứ thật vào tư liệu) và che_ngoai_danh_sach của v5
MAXTOK = int(os.environ.get('VBHC_MAX_TOKEN', '3000'))   # 3000 vừa max-seq 3072 như v4–v6; 6000 cần max-seq 6144 khi huấn luyện
rng = random.Random(20261127); O = os.environ.get('VBHC_RA', 'm8'); os.makedirs(O, exist_ok=True)
LOAI = ['Công văn', 'Thông báo', 'Quyết định (cá biệt)', 'Công điện', 'Chỉ thị']

def dt(c): d = c['doi_chieu']; return d if isinstance(d, dict) else eval(d)
RE_SO = re.compile(r'(?im)^(?P<dau>[^\n]{0,40}?)\bS[ốóôoồổỗộờ][\s.]*[:;]?\s*(?P<so>[^\s,]{0,8}\s*/\s*[^\s,]+)')
RE_NGAY = re.compile(r'ngày\s*\S{0,4}\s*th[áa]n?g?\s*\S{0,4}\s*n[ăa]m\s*\S{0,6}', re.I)
def sua_dau(c):
    """Viết lại số ký hiệu và ngày ở 15 dòng đầu theo chỉ mục. Trả (văn bản, đã sửa?) hoặc (None, lý do)."""
    t = c['text']; dau = '\n'.join(t.split('\n')[:15]); than = t[len(dau):]
    m = RE_SO.search(dau)
    if not m: return None, 'khong_co_dong_so'
    y, mo, d = c['ngay_ban_hanh'].split('-')
    dau2 = dau[:m.start('so')] + c['so_ky_hieu_chuan'] + dau[m.end('so'):]
    n = RE_NGAY.search(dau2, m.end())
    if n: dau2 = dau2[:n.start()] + f'ngày {int(d):02d} tháng {int(mo) if int(mo) >= 3 else f"{int(mo):02d}"} năm {y}' + dau2[n.end():]
    elif not dt(c).get('ngay_ban_hanh_toan_van'): return None, 'khong_co_dong_ngay'
    return dau2 + than, dau2 != dau

def nhan(c):
    if c['loai_van_ban'] not in LOAI or SP.get(c['docid']) != 'train' and SP.get(c['docid']) != 'valid': return None, 'loai_hoac_tap'
    d = dt(c)
    if (d.get('trung_trich_yeu') or 0) < 0.8 or '[HỌ TÊN]' in c['trich_yeu']: return None, 'trich_yeu'
    if d.get('so_ky_hieu_toan_van') not in ('khop', 'gan_khop', 'khong_doc_duoc', 'nguoi_kiem_xac_nhan'): return None, 'so_khac'
    t, sua = sua_dau(c)
    if t is None: return None, sua
    c2 = dict(c, text=t)
    if not v1.du_trang(c2): return None, 'thieu_trang'
    if not (1200 <= len(t) <= MAXTOK * 3): return None, 'do_dai'
    if {x for x, v in v2.kiem(c2).items() if v} - {'L11', 'L12'}: return None, 'luat_the_thuc'
    s, _ = lam_sach_v2(t)
    if len(s) > MAXTOK * 2.7: return None, 'do_dai'
    if nhieu(s) > 0.02: return None, 'nhieu'
    return (c2, s, sua), 'dat'

from transformers import AutoTokenizer
TOK = AutoTokenizer.from_pretrained(os.environ.get('VBHC_TOKENIZER', '/home/claude/m4/qwen25_05b'))
vua = lambda r: len(TOK(TOK.apply_chat_template(r['messages'], tokenize=False))['input_ids']) <= MAXTOK
TK = {}; LY = collections.Counter()
BE = collections.defaultdict(list)
for c in sorted(C, key=lambda c: c['docid']):
    r, ly = nhan(c); LY[ly] += 1
    if r: BE[SP[c['docid']]].append(r)
for s, n2, n3, n4 in (('train', 300, 300, 200), ('valid', 30, 30, 20)):
    be = BE[s]; rng.shuffle(be)
    if s == 'valid': be = be[:40]
    T1, dem = [], collections.Counter()
    for c, sach, sua in be:
        dem['dau_sua'] += bool(sua)
        tra, n = che_v2(sach, c['so_ky_hieu_chuan'])
        de = de_T1(c); dap = rng.random() < 0.7
        de2, cho = v6m.tu_lieu(de, tra, c['so_ky_hieu_chuan'], dap)
        giu = set(SOT.pho_thu_tuong(c['ngay_ban_hanh'])) | ({SOT.thu_tuong(c['ngay_ban_hanh'])} - {None})
        tra, a = v6m.v5.che_ngoai_danh_sach(tra, cho, c['so_ky_hieu_chuan']); tra, b = LS.che(tra, giu)
        dem.update(a); dem.update(b); dem['co_dap_an' if dap else 'tra_cuu_that'] += 1
        r = msg(de2, tra); r['_loai'] = c['loai_van_ban']; T1.append(r)
    n0 = len(T1); T1 = [r for r in T1 if vua(r)]; dem['bo_qua_qua_dai'] = n0 - len(T1)
    # cân bằng: công văn tối đa 35% (M8.1); từ khi có đợt cào M8 (VBHC_CHIA_TAP_THEM), mọi loại tối đa 35%
    tran_loai = ['Công văn'] if not os.environ.get('VBHC_CHIA_TAP_THEM') else LOAI
    for _ in range(3 if os.environ.get('VBHC_CHIA_TAP_THEM') else 1):   # lặp vì bỏ bớt loại này làm tỷ lệ loại khác tăng (M8.1 giữ một lượt như cũ)
        dem_l = collections.Counter(r['_loai'] for r in T1)
        for L in tran_loai:
            khac = len(T1) - dem_l[L]; tran = int(0.35 / 0.65 * khac)
            if dem_l[L] > tran or not os.environ.get('VBHC_CHIA_TAP_THEM'):   # M8.1: luôn xếp lại như bản đầu (để tái lập)
                giu = [r for r in T1 if r['_loai'] == L][:tran]; dem['bo_bot:' + L] = dem.get('bo_bot:' + L, 0) + max(0, dem_l[L] - tran)
                T1 = [r for r in T1 if r['_loai'] != L] + giu; dem_l = collections.Counter(r['_loai'] for r in T1)
    loai = collections.Counter(r.pop('_loai') for r in T1)
    R = [json.loads(l) for l in open(f'm6b/{s}.jsonl', encoding='utf-8')]
    nhom = collections.defaultdict(list)
    for r in R: nhom[v6m.v5.nv(r)].append(r)
    for x in nhom.values(): rng.shuffle(x)
    rows = T1 + nhom['T2'][:n2] + nhom['T3'][:n3] + nhom['T4'][:n4]; rng.shuffle(rows)
    open(f'{O}/{s}.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    TK[s] = {'tong': len(rows), 'T1': len(T1), 'T1_theo_loai': dict(loai), 'T2': n2, 'T3': n3, 'T4': n4, 'xu_ly': dict(dem)}
TK['ly_do_loai_khoi_be'] = dict(LY)
json.dump(TK, open(f'{O}/thong_ke.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(TK, ensure_ascii=False, indent=1))
