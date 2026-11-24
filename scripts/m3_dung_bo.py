"""M3 · Dựng bộ đánh giá VBHC-Bench bản pilot từ bộ toàn văn v4.
Ba nhiệm vụ: T1 soạn văn bản từ yêu cầu; T2 tìm lỗi thể thức; T3 trích thông tin.
Chia tập theo CỤM MẪU: văn bản gần trùng mẫu (gan_trung_mau_voi) luôn nằm cùng một phía.
Đáp án T2 sinh từ lỗi cài; đáp án T3 chỉ lấy ô mà chỉ mục và toàn văn cùng xác nhận."""
import json, re, random, sys, copy, collections, hashlib, os
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
SEED = 2026; rng = random.Random(SEED); O = 'm3'
C = [json.loads(l) for l in open(os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'), encoding='utf-8')]  # người ngoài: đặt VBHC_TOAN_VAN=<đường dẫn toan_van_v4.jsonl tải từ Drive>
BY = {c['docid']: c for c in C}
NAM_LOAI = ['Công văn', 'Thông báo', 'Quyết định (cá biệt)', 'Công điện', 'Chỉ thị']
# ---------- cụm mẫu (union-find)
par = {c['docid']: c['docid'] for c in C}
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for c in C:
    for o in c.get('gan_trung_mau_voi') or []:
        if o in par: par[find(c['docid'])] = find(o)
# cụm theo chuỗi văn bản định kỳ: cùng cơ quan và cùng trích yếu sau khi bỏ số, ngày tháng (bắt các mẫu mà Jaccard < 0,9 bỏ sót)
def khoa_mau(c):
    t = re.sub(r'\d+', '#', c['trich_yeu'].lower()); t = re.sub(r'\(?ngày # tháng # năm #\)?|#/#/#|#/#|tuần #|tháng #|quý \w+|năm #', '~', t)
    return c['nguon'] + '|' + c['co_quan_ky_hieu'] + '|' + re.sub(r'[\s~#.,;:()\-–]+', ' ', t).strip()
_dau = {}
for c in C:
    k = khoa_mau(c)
    if len(k.split('|')[-1]) >= 25:
        if k in _dau: par[find(c['docid'])] = find(_dau[k])
        else: _dau[k] = c['docid']
cum = collections.defaultdict(list)
for c in C: cum[find(c['docid'])].append(c['docid'])
# ---------- ứng viên từng nhiệm vụ
D2 = re.compile(r'ngày \d\d tháng \d\d năm \d{4}')
def sach(c):  # văn bản đạt mọi luật và có đủ mẫu chữ để cài lỗi
    t = c['text']
    return (c['loai_van_ban'] in NAM_LOAI and len(t) <= 9000 and v1.du_trang(c) and not any(v2.kiem(c).values()) and D2.search(v1.vung_dau(t))
            and 'Độc lập - Tự do - Hạnh phúc' in t[:1500] and re.search(r'Số: \d', t[:2000]) and 'Nơi nhận' in t and 'Lưu: VT' in t and './.' in t
            and re.search(r'CỘNG HO[ÀÒ]A? XÃ HỘI CHỦ NGHĨA VIỆT NAM', t[:1500]))
def t3_ok(c):
    d = c['doi_chieu']
    return c['loai_van_ban'] in NAM_LOAI and d['so_ky_hieu_toan_van'] == 'khop' and d['ngay_ban_hanh_toan_van'] and (d['trung_trich_yeu'] or 0) >= 0.8 and '[HỌ TÊN]' not in c['trich_yeu'] and 800 <= len(c['text'])
def t1_ok(c):
    return t3_ok(c) and 1200 <= len(c['text']) <= 7000 and v1.du_trang(c) and (c['boc_chu'] == 'text_layer' or (c['do_tin_ocr'] or 0) >= 93) and sum(bool(x) for x in v2.kiem(c).values()) == 0
S2 = [c['docid'] for c in C if sach(c)]; S3 = [c['docid'] for c in C if t3_ok(c)]; S1 = [c['docid'] for c in C if t1_ok(c)]
# ---------- chọn tập kiểm tra theo cụm
test_cum = set(); test = {'T1': [], 'T2': [], 'T3': []}
def lay(pool, n_moi_loai, key, da_dung):
    p = pool[:]; rng.shuffle(p); dem = collections.Counter()
    for d in p:
        l = BY[d]['loai_van_ban']
        if dem[l] >= n_moi_loai.get(l, 0) or d in da_dung: continue
        test[key].append(d); dem[l] += 1; da_dung.add(d); test_cum.add(find(d))
    return dem
dd = set()
print('T2', lay(S2, {'Công văn': 45, 'Thông báo': 45, 'Quyết định (cá biệt)': 8, 'Công điện': 8, 'Chỉ thị': 4}, 'T2', dd))
print('T1', lay(S1, {l: 10 for l in NAM_LOAI}, 'T1', dd))
print('T3', lay(S3, {l: 30 for l in NAM_LOAI}, 'T3', dd))
split = {}
for r, ds in cum.items():
    s = 'test' if r in test_cum else ('valid' if int(hashlib.md5(r.encode()).hexdigest(), 16) % 20 == 0 else 'train')
    for d in ds: split[d] = s
in_test = {d for ds in test.values() for d in ds}
for d, s in split.items():
    if s == 'test' and d not in in_test: split[d] = 'giu_ngoai'   # cùng cụm với văn bản kiểm tra: không dùng để huấn luyện
print('chia tập:', collections.Counter(split.values()), '| số cụm:', len(cum), '| cụm >1 văn bản:', sum(len(v) > 1 for v in cum.values()))
# ---------- lời yêu cầu
HE = 'Bạn là trợ lý soạn thảo và rà soát văn bản hành chính Việt Nam theo Nghị định 30/2020/NĐ-CP.'
LOI = {'quoc_hieu_viet_tat': 'Quốc hiệu viết tắt hoặc thiếu', 'tieu_ngu_hoa_sai': 'Tiêu ngữ viết hoa sai', 'so_thieu_hai_cham': 'Dòng số, ký hiệu thiếu dấu hai chấm sau chữ Số',
       'ky_hieu_dao': 'Ký hiệu đảo thứ tự tên loại và cơ quan', 'ngay_dang_so': 'Ngày ban hành viết dạng số thay vì "ngày ... tháng ... năm ..."', 'ngay_thieu_so_0': 'Ngày dưới 10 hoặc tháng 1, 2 thiếu số 0 ở trước',
       'ten_loai_viet_thuong': 'Tên loại văn bản không viết hoa', 'cong_van_thieu_trich_yeu': 'Công văn thiếu trích yếu V/v', 'thieu_noi_nhan': 'Thiếu mục Nơi nhận',
       'luu_sai': 'Mục lưu không ghi "Lưu: VT"', 'thieu_ket_thuc': 'Nội dung không kết thúc bằng "./."'}
def de_T2(t): return ('Văn bản dưới đây có thể có MỘT lỗi thể thức hoặc không có lỗi. Chọn đúng một mã trong danh sách và trả về JSON dạng {"loi": "<mã>"}.\n'
                      'Danh sách mã:\n- KHONG_LOI: không có lỗi nào trong danh sách\n' + ''.join(f'- {k}: {v}\n' for k, v in LOI.items()) + '\nVĂN BẢN:\n' + t)
def de_T3(t): return ('Đọc văn bản và trả về JSON với đúng bốn khóa: "so_ky_hieu", "ngay_ban_hanh" (dạng YYYY-MM-DD), "loai_van_ban" (một trong: ' + ', '.join(NAM_LOAI) + '), "trich_yeu".\n\nVĂN BẢN:\n' + t[:5000] + ('\n[...]\n' + t[-1200:] if len(t) > 6200 else t[5000:]))
def co_quan(c): return c.get('co_quan_ten') or {'VPCP': 'Văn phòng Chính phủ', 'TTg': 'Thủ tướng Chính phủ'}.get(c['co_quan_ky_hieu'], c['co_quan_ky_hieu'])
def de_T1(c):
    y, m, d = c['ngay_ban_hanh'].split('-')
    return (f'Soạn hoàn chỉnh một văn bản loại "{c["loai_van_ban"]}" đúng thể thức Nghị định 30/2020/NĐ-CP với thông tin sau:\n- Cơ quan ban hành: {co_quan(c)}\n- Số, ký hiệu: {c["so_ky_hieu_chuan"]}\n'
            f'- Ngày ban hành: ngày {d} tháng {m if int(m) < 3 else int(m)} năm {y}\n- Trích yếu nội dung: {c["trich_yeu"]}\nViết đủ các thành phần thể thức và phần nội dung phù hợp với trích yếu. Chỉ trả về văn bản.')
# ---------- cài lỗi (như M1)
def mut(c, kind):
    d = copy.deepcopy(c); t = d['text']; vd = v1.vung_dau(t); H = t[:len(vd)]; R = t[len(vd):]
    def sub(p, r, x):
        y = re.sub(p, r, x, count=1); assert y != x; return y
    if kind == 'quoc_hieu_viet_tat': H = sub(r'CỘNG HO[ÀÒ]A? XÃ HỘI CHỦ NGHĨA VIỆT NAM', 'CHXHCN VIỆT NAM', H)
    elif kind == 'tieu_ngu_hoa_sai': H = sub('Độc lập - Tự do - Hạnh phúc', 'Độc Lập - Tự Do - Hạnh Phúc', H)
    elif kind == 'so_thieu_hai_cham': H = sub(r'Số: (\d)', r'Số \1', H)
    elif kind == 'ky_hieu_dao':
        assert d['loai_van_ban'] != 'Công văn'; a, b = d['so_ky_hieu_chuan'].split('/', 1); p = b.split('-', 1); assert b in H; H = H.replace(b, f'{p[1]}-{p[0]}')
    elif kind == 'ngay_dang_so': H = sub(r'ngày (\d\d) tháng (\d\d) năm (\d{4})', r'\1/\2/\3', H)
    elif kind == 'ngay_thieu_so_0': H = sub(r'ngày \d\d tháng \d\d năm (\d{4})', r'ngày 5 tháng 2 năm \1', H)
    elif kind == 'ten_loai_viet_thuong':
        assert d['loai_van_ban'] != 'Công văn'; ten = d['loai_van_ban'].split(' (')[0].upper(); H = sub(r'(?m)^(\s*)' + ten + r'\s*$', lambda m: m.group(1) + ten.capitalize(), H)
    elif kind == 'cong_van_thieu_trich_yeu':
        assert d['loai_van_ban'] == 'Công văn'; t2 = re.sub(r'V\s*/\s*v|Về việc', '', t[:2500]); assert t2 != t[:2500]; H, R = t2, t[2500:]
    elif kind == 'thieu_noi_nhan': H, R = t.replace('Nơi nhận:', '').replace('Nơi nhận', ''), ''
    elif kind == 'luu_sai': H, R = t.replace('Lưu: VT', 'Lưu: VP'), ''
    elif kind == 'thieu_ket_thuc': H, R = re.sub(r'\.\s*[/⁄]\s*\.', '.', t), ''
    return H + R
KINDS = list(LOI)
def muc_T2(c, kind, i):
    t = c['text'] if kind == 'KHONG_LOI' else mut(c, kind)
    return {'id': f'T2-{i:04d}', 'nhiem_vu': 'T2', 'docid': c['docid'], 'de': de_T2(t), 'dap_an': {'loi': kind}}
def w(name, rows): open(f'{O}/{name}', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
# ---------- bộ kiểm tra
T = []; i = 0; ds = test['T2'][:]; rng.shuffle(ds); dem_k = collections.Counter()
for d in ds:
    c = BY[d]; i += 1
    if i % 5 == 0: T.append(muc_T2(c, 'KHONG_LOI', i)); continue
    for k in sorted(KINDS, key=lambda k: (dem_k[k], rng.random())):
        try: T.append(muc_T2(c, k, i)); dem_k[k] += 1; break
        except AssertionError: continue
for j, d in enumerate(test['T3'], 1):
    c = BY[d]; T.append({'id': f'T3-{j:04d}', 'nhiem_vu': 'T3', 'docid': d, 'de': de_T3(c['text']), 'dap_an': {'so_ky_hieu': c['so_ky_hieu_chuan'], 'ngay_ban_hanh': c['ngay_ban_hanh'], 'loai_van_ban': c['loai_van_ban'], 'trich_yeu': c['trich_yeu']}})
for j, d in enumerate(test['T1'], 1):
    c = BY[d]; T.append({'id': f'T1-{j:04d}', 'nhiem_vu': 'T1', 'docid': d, 'de': de_T1(c), 'dap_an': {'van_ban_tham_chieu': c['text'], 'so_ky_hieu_chuan': c['so_ky_hieu_chuan'], 'loai_van_ban': c['loai_van_ban'], 'ngay_ban_hanh': c['ngay_ban_hanh'], 'trich_yeu': c['trich_yeu']}})
w('test_de.jsonl', [{'id': x['id'], 'nhiem_vu': x['nhiem_vu'], 'he_thong': HE, 'de': x['de']} for x in T])
w('test_dap_an.jsonl', [{'id': x['id'], 'nhiem_vu': x['nhiem_vu'], 'docid': x['docid'], 'dap_an': x['dap_an']} for x in T])
print('bộ kiểm tra:', collections.Counter(x['nhiem_vu'] for x in T), '| T2 đáp án:', collections.Counter(x['dap_an']['loi'] for x in T if x['nhiem_vu'] == 'T2'))
# ---------- tập huấn luyện và thẩm định (dạng hội thoại cho mlx_lm)
def msg(de, tra): return {'messages': [{'role': 'system', 'content': HE}, {'role': 'user', 'content': de}, {'role': 'assistant', 'content': tra}]}
TR = {'train': [], 'valid': []}
for s in TR:
    p2 = [d for d in S2 if split[d] == s]; p3 = [d for d in S3 if split[d] == s]; p1 = [d for d in S1 if split[d] == s]
    rng.shuffle(p3); rng.shuffle(p1)
    for d in p2:
        c = BY[d]; TR[s].append(msg(de_T2(c['text']), json.dumps({'loi': 'KHONG_LOI'}, ensure_ascii=False)))
        ks = KINDS[:]; rng.shuffle(ks); n = 0
        for k in ks:
            if n >= 4: break
            try: TR[s].append(msg(de_T2(mut(c, k)), json.dumps({'loi': k}, ensure_ascii=False))); n += 1
            except AssertionError: pass
    for d in p3[:1200 if s == 'train' else 80]:
        c = BY[d]; TR[s].append(msg(de_T3(c['text']), json.dumps({'so_ky_hieu': c['so_ky_hieu_chuan'], 'ngay_ban_hanh': c['ngay_ban_hanh'], 'loai_van_ban': c['loai_van_ban'], 'trich_yeu': c['trich_yeu']}, ensure_ascii=False)))
    for d in p1[:600 if s == 'train' else 40]:
        c = BY[d]; TR[s].append(msg(de_T1(c), c['text']))
    rng.shuffle(TR[s]); w(f'{s}.jsonl', TR[s]); print(s, len(TR[s]), 'ví dụ | T2 gốc', len(p2), 'T3', min(len(p3), 1200 if s == 'train' else 80), 'T1', min(len(p1), 600 if s == 'train' else 40))
json.dump({'seed': SEED, 'chia_tap': split, 'cum': {d: find(d) for d in split}}, open(f'{O}/chia_tap.json', 'w', encoding='utf-8'), ensure_ascii=False)
# kiểm rò rỉ: không văn bản kiểm tra hay cùng cụm nào nằm trong huấn luyện
tr_ids = {d for d, s in split.items() if s in ('train', 'valid')}
assert not (in_test & tr_ids) and not ({find(d) for d in in_test} & {find(d) for d in tr_ids}); print('kiểm rò rỉ theo cụm: đạt')
