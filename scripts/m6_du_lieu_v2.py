"""M6 · Tập huấn luyện v2 (QĐ-12). Bộ kiểm tra m3/test_* giữ nguyên, chỉ đổi dữ liệu huấn luyện và thẩm định.

1. T1 lọc theo độ nhiễu chữ thay vì độ tin OCR: tỷ lệ âm tiết không có trong từ vựng lấy từ văn bản có lớp chữ (xuất hiện ≥ 3 lần) phải ≤ 2%.
   Cho phép vi phạm L11 (quyền hạn người ký: người đứng đầu tự ký thì không ghi TM./KT.) và L12 (./., chưa có căn cứ), không cho phép luật khác.
2. T1 thay chi tiết không suy ra được từ lời yêu cầu bằng dấu "…": số và ngày của văn bản viện dẫn không phải văn bản quy phạm trung ương
   (tờ trình, công văn, quyết định cá biệt, văn bản địa phương), và họ tên người ký. Giữ nguyên viện dẫn luật, nghị định, thông tư, nghị quyết có năm.
   Mục đích: dạy mô hình để trống thay vì bịa (tiêu chí D của hướng dẫn chấm).
3. Cân lại: T3 600 (đã bão hòa), T2 giữ 600 như m3, T1 lấy hết bể đạt lọc.
Dùng: VBHC_TOAN_VAN=<toan_van_v4.jsonl> python3 scripts/m6_du_lieu_v2.py   → m6/train.jsonl, m6/valid.jsonl, m6/thong_ke.json
"""
import json, re, os, sys, random, collections, lzma, ast
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
rng = random.Random(2026); O = 'm6'; os.makedirs(O, exist_ok=True)
C = [json.loads(l) for l in open(os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'), encoding='utf-8')]
SP = json.load(open('m3/chia_tap.json', encoding='utf-8'))['chia_tap']
# lấy nguyên văn hàm dựng lời yêu cầu T1 từ m3_dung_bo.py để lời yêu cầu huấn luyện trùng khuôn với bộ kiểm tra
src = open('scripts/m3_dung_bo.py', encoding='utf-8').read(); g = {}
for node in ast.parse(src).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('co_quan', 'de_T1'):
        exec(ast.get_source_segment(src, node), g)
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('HE', 'NAM_LOAI'):
        exec(ast.get_source_segment(src, node), g)
de_T1, HE, NAM_LOAI = g['de_T1'], g['HE'], g['NAM_LOAI']

dem = collections.Counter()
for c in C:
    if c['boc_chu'] == 'text_layer': dem.update(w.lower() for w in re.findall(r'[^\W\d_]+', c['text']))
LEX = {w for w, n in dem.items() if n >= 3}
def nhieu(t):
    w = [x.lower() for x in re.findall(r'[^\W\d_]+', t)]
    return sum(x not in LEX for x in w) / max(1, len(w))
DAU = re.compile(r'C[ổô]ng\s*Th[ôo]ng\s*t[iíừứưu]+|thongtin|chinhphu\.?vn|Th[ờo]i gian k[ýy]|K[ýy] b[ởo]i|E-?mai|^\W{0,3}Ng[àa]y:\s*[“"\d]|TH[ÔO]NG\s*T[IÍ]N\s*Đ[IỊ]ỆN\s*T[ỬỪU]', re.I)
def lam_sach(t):
    """Bỏ dòng dấu chữ ký số của Cổng TTĐT và dòng rác do con dấu đè chữ; không sửa chữ trong dòng còn lại."""
    giu, bo = [], 0
    for ln in t.split('\n'):
        w = re.findall(r'[^\W\d_]+', ln)
        x = sum(v.lower() not in LEX for v in w) / len(w) if w else 0
        hoa = sum(ch.isupper() for ch in ln) >= 0.6 * max(1, sum(ch.isalpha() for ch in ln))
        if DAU.search(ln) or (hoa and len(ln.strip()) < 50 and re.search(r'ĐI[ỆỂE]N\s*T[ỬỪỰUỦ]|\bĐẾN\b', ln)) or len(ln.strip()) in (1, 2, 3) or (re.search(r'\.{4,}', ln) and len(ln.strip()) < 40) or (w and x > 0.4 and len(ln.strip()) < 80) or (not w and len(ln.strip()) > 0 and not re.search(r'\d|-{3,}|—{3,}|\./\.', ln)):
            bo += 1; continue
        giu.append(ln)
    # phần trước dòng quốc hiệu chỉ giữ dòng chữ in hoa (tên cơ quan); còn lại là rác của dấu chữ ký số
    for k, ln in enumerate(giu[:12]):
        if re.search(r'C[ỘO]NG\s*H[OÒ]', ln):
            dau = [x for x in giu[:k] if len(x.strip()) >= 6 and sum(ch.isupper() for ch in x) >= 0.7 * max(1, sum(ch.isalpha() for ch in x))]
            bo += k - len(dau); giu = dau + giu[k:]; break
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(giu)).strip(), bo
def t3_ok(c):
    d = c['doi_chieu']
    return c['loai_van_ban'] in NAM_LOAI and d['so_ky_hieu_toan_van'] == 'khop' and d['ngay_ban_hanh_toan_van'] and (d['trung_trich_yeu'] or 0) >= 0.8 and '[HỌ TÊN]' not in c['trich_yeu'] and 800 <= len(c['text'])
def t1_ok_v2(c):
    if not (t3_ok(c) and 1200 <= len(c['text']) <= 9000 and v1.du_trang(c)): return False
    if {k for k, v in v2.kiem(c).items() if v} - {'L11', 'L12'}: return False
    t = lam_sach(c['text'])[0]
    return len(t) <= 8000 and nhieu(t) <= 0.02   # 8000 ký tự ≈ 3000 token Qwen, vừa max-seq-length 3072

GIU = re.compile(r'^(NĐ-CP|NQ-CP|QĐ-TTg|QH1[3-5]|UBTVQH1[3-5]|TT-[A-ZĐa-z]+|TTLT-[A-ZĐa-z-]+)$')
KH = re.compile(r'(?<![\d/…])(\d{1,5})/(?:(\d{4})/)?([A-ZĐ]{1,8}\d{0,2}(?:-[A-ZĐa-zđ0-9]{1,12}){0,3})')
NGAY = re.compile(r'(\s*(?:,\s*)?ngày\s*)(\d{1,2})(\s*tháng\s*)(\d{1,2})(\s*năm\s*)(\d{4})|(\s*(?:,\s*)?ngày\s*)(\d{1,2}/\d{1,2}/\d{4})', re.I)
TEN = re.compile(r'(^|\s{3,})([A-ZĐ][a-zà-ỹđ]+(?:[ \t][A-ZĐ][a-zà-ỹđ]+){1,3})[ \t]*$', re.M)
def che(t, kh_ban_than):
    n = {'van_ban': 0, 'ten': 0}
    out, i = [], 0
    for m in KH.finditer(t):
        so, nam, ky = m.groups()
        if m.group(0) == kh_ban_than or (nam and GIU.match(ky)): continue
        out.append(t[i:m.start()]); out.append(f'…/{nam + "/" if nam else ""}{ky}'); i = m.end(); n['van_ban'] += 1
        d = NGAY.match(t, i)
        if d:
            out.append(f'{d.group(1)}… tháng … năm …' if d.group(1) is not None else f'{d.group(7)}…'); i = d.end()
    out.append(t[i:]); t = ''.join(out)
    cut = int(len(t) * 0.7)
    def thay(m):
        n['ten'] += 1; return m.group(1) + '[Họ và tên]'
    t = t[:cut] + TEN.sub(thay, t[cut:])
    return t, n

def msg(de, tra): return {'messages': [{'role': 'system', 'content': HE}, {'role': 'user', 'content': de}, {'role': 'assistant', 'content': tra}]}
def cu(p):
    f = lzma.open(p, 'rt', encoding='utf-8') if p.endswith('.xz') else open(p, encoding='utf-8')
    R = [json.loads(l) for l in f]
    t2 = [r for r in R if r['messages'][1]['content'].startswith('Văn bản dưới đây có thể có MỘT lỗi')]
    t3 = [r for r in R if r['messages'][1]['content'].startswith('Đọc văn bản và trả về JSON')]
    return t2, t3
TK = {}
for s, nguon, n3 in (('train', 'm3/train.jsonl.xz', 600), ('valid', 'm3/valid.jsonl', 80)):
    t2, t3 = cu(nguon); rng.shuffle(t3)
    p1 = sorted(c['docid'] for c in C if SP[c['docid']] == s and t1_ok_v2(c)); rng.shuffle(p1)
    BY = {c['docid']: c for c in C}
    T1 = []; tong = collections.Counter()
    for d in p1[:10**6 if s == 'train' else 40]:
        c = BY[d]; sach, bo = lam_sach(c['text']); tra, n = che(sach, c['so_ky_hieu_chuan']); n['dong_bo'] = bo; tong.update(n)
        T1.append(msg(de_T1(c), tra))
    rows = t2 + t3[:n3] + T1; rng.shuffle(rows)
    open(f'{O}/{s}.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    TK[s] = {'tong': len(rows), 'T1': len(T1), 'T2': len(t2), 'T3': min(n3, len(t3)), 'T1_theo_loai': dict(collections.Counter(BY[d]['loai_van_ban'] for d in p1[:len(T1)])),
             'da_che': dict(tong)}
    assert all(SP[d] == s for d in p1[:len(T1)])
json.dump(TK, open(f'{O}/thong_ke.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(TK, ensure_ascii=False))
