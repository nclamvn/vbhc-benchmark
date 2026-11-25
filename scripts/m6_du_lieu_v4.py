"""M6b · Tập huấn luyện v4 (QĐ-13), dựng từ m6/ (v2). Bộ kiểm tra m3/test_* giữ nguyên.

Ba thay đổi, mỗi thay đổi nhắm một lỗi đã thấy ở bản v3:
1. T1 bỏ dòng "Cơ quan: …" ở đầu văn bản (vết của dấu chữ ký số, có ở 295/804 mục tiêu). Bản v3 chép dòng này vào bài.
2. T2 đổi sang dạng đối chứng: mỗi văn bản sạch sinh đủ 12 phiên bản (KHONG_LOI và 11 lỗi cài), để mô hình phải so
   cùng một văn bản với các lỗi khác nhau thay vì đoán theo tần suất. Bản v3 trả "thieu_ket_thuc" cho 71/94 câu.
3. Thêm nhiệm vụ phụ T4 "mốc thời gian bộ máy". Câu hỏi lấy ngày ban hành của văn bản thật trong tập huấn luyện.
   Đáp án suy tất định từ các mốc đã ban hành:
   - Nghị quyết 176/2025/QH15: cơ cấu Chính phủ mới từ 01/3/2025.
   - Bỏ cấp huyện từ 01/7/2025.
   - Thủ tướng Nguyễn Xuân Phúc đến 05/4/2021, Thủ tướng Phạm Minh Chính từ 05/4/2021. Chỉ dùng ngày trước 2026.
   Bản v3 áp tên bộ mới cho văn bản 2020–2024. T4 không thuộc bộ kiểm tra.
Cân lại: T3 300 (đã bão hòa).
Dùng: VBHC_TOAN_VAN=<toan_van_v4.jsonl> python3 scripts/m6_du_lieu_v4.py   → m6b/train.jsonl, m6b/valid.jsonl, m6b/thong_ke.json
"""
import json, re, os, sys, random, collections, copy, ast
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
rng = random.Random(20261125); O = 'm6b'; os.makedirs(O, exist_ok=True)
C = [json.loads(l) for l in open(os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'), encoding='utf-8')]
SP = json.load(open('m3/chia_tap.json', encoding='utf-8'))['chia_tap']
src = open('scripts/m3_dung_bo.py', encoding='utf-8').read(); g = {'re': re, 'copy': copy, 'v1': v1, 'v2': v2}
for node in ast.parse(src).body:   # lấy nguyên văn định nghĩa từ bộ dựng M3 để lời yêu cầu và lỗi cài trùng khuôn với bộ kiểm tra
    if isinstance(node, ast.FunctionDef) and node.name in ('sach', 'mut', 'de_T2'):
        exec(ast.get_source_segment(src, node), g)
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('NAM_LOAI', 'D2', 'HE', 'LOI'):
        exec(ast.get_source_segment(src, node), g)
sach, mut, de_T2, HE, LOI = g['sach'], g['mut'], g['de_T2'], g['HE'], g['LOI']; KINDS = list(LOI)
def msg(de, tra): return {'messages': [{'role': 'system', 'content': HE}, {'role': 'user', 'content': de}, {'role': 'assistant', 'content': tra}]}
def nv(r):
    u = r['messages'][1]['content']
    return 'T1' if u.startswith('Soạn') else 'T2' if u.startswith('Văn bản dưới') else 'T3' if u.startswith('Đọc văn bản') else '?'

# 1. T1: bỏ dòng "Cơ quan: …" trong 4 dòng đầu
def bo_co_quan(t):
    d = t.split('\n'); k = [i for i, x in enumerate(d[:4]) if re.match(r'\s*C[ơo] quan\s*:', x)]
    return '\n'.join(x for i, x in enumerate(d) if i not in k)

# 3. T4: mốc thời gian bộ máy
MOC = '2025-03-01'
LV = [('nông nghiệp', 'Bộ Nông nghiệp và Phát triển nông thôn', 'Bộ Nông nghiệp và Môi trường'),
      ('tài nguyên và môi trường', 'Bộ Tài nguyên và Môi trường', 'Bộ Nông nghiệp và Môi trường'),
      ('giao thông vận tải', 'Bộ Giao thông vận tải', 'Bộ Xây dựng'),
      ('kế hoạch và đầu tư', 'Bộ Kế hoạch và Đầu tư', 'Bộ Tài chính'),
      ('lao động, việc làm', 'Bộ Lao động - Thương binh và Xã hội', 'Bộ Nội vụ'),
      ('thông tin và truyền thông', 'Bộ Thông tin và Truyền thông', 'Bộ Khoa học và Công nghệ')]
def ngay_chu(d): y, m, dd = d.split('-'); return f'ngày {dd} tháng {m} năm {y}'
def t4(d):
    out = []
    for lv, cu, moi in LV:
        out.append((f'Văn bản hành chính ban hành {ngay_chu(d)}. Tại thời điểm đó, bộ quản lý nhà nước về {lv} có tên chính thức là gì? Chỉ trả lời tên bộ.',
                     cu if d < MOC else moi))
    out.append((f'Văn bản hành chính ban hành {ngay_chu(d)}. Tại thời điểm đó, chính quyền địa phương được tổ chức mấy cấp? Trả lời ngắn.',
                 'Ba cấp: tỉnh, huyện, xã.' if d < '2025-07-01' else 'Hai cấp: tỉnh và xã (không còn cấp huyện).'))
    if d < '2026-01-01':
        out.append((f'Văn bản của Thủ tướng Chính phủ ban hành {ngay_chu(d)}. Ai là Thủ tướng Chính phủ tại thời điểm đó? Chỉ trả lời họ tên.',
                     'Nguyễn Xuân Phúc' if d < '2021-04-05' else 'Phạm Minh Chính'))
    return out

def vua_fn():
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(os.environ.get('VBHC_TOKENIZER', '/home/claude/m4/qwen25_05b'))
    return lambda r: len(tok(tok.apply_chat_template(r['messages'], tokenize=False))['input_ids']) <= 3000
vua = vua_fn()
TK = {}
for s, n2, n3, n4 in (('train', 60, 300, 420), ('valid', 6, 30, 30)):
    cu = [json.loads(l) for l in open(f'm6/{s}.jsonl', encoding='utf-8')]
    T1 = []
    for r in cu:
        if nv(r) == 'T1':
            r = copy.deepcopy(r); r['messages'][2]['content'] = bo_co_quan(r['messages'][2]['content']); T1.append(r)
    T3 = [r for r in cu if nv(r) == 'T3']; rng.shuffle(T3); T3 = T3[:n3]
    p2 = sorted(c['docid'] for c in C if SP[c['docid']] == s and sach(c)); rng.shuffle(p2)
    BY = {c['docid']: c for c in C}; T2 = []; dem2 = collections.Counter()
    for d in p2[:n2]:
        c = BY[d]; T2.append(msg(de_T2(c['text']), json.dumps({'loi': 'KHONG_LOI'}, ensure_ascii=False))); dem2['KHONG_LOI'] += 1
        for k in KINDS:
            try: T2.append(msg(de_T2(mut(c, k)), json.dumps({'loi': k}, ensure_ascii=False))); dem2[k] += 1
            except AssertionError: pass
    ngay = sorted({c['ngay_ban_hanh'] for c in C if SP[c['docid']] == s and c.get('ngay_ban_hanh')})
    truoc = [d for d in ngay if d < MOC]; sau = [d for d in ngay if d >= MOC]
    pool = [(q, a, d) for d in rng.sample(truoc, min(len(truoc), 60)) + rng.sample(sau, min(len(sau), 60)) for q, a in t4(d)]
    rng.shuffle(pool); T4 = [msg(q, a) for q, a, _ in pool[:n4]]
    rows = [r for r in T1 + T2 + T3 + T4 if vua(r)]; rng.shuffle(rows)
    open(f'{O}/{s}.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    TK[s] = {'tong': len(rows), 'T1': len(T1), 'T1_bo_dong_co_quan': sum(bool(re.match(r'\s*C[ơo] quan', r['messages'][2]['content'])) for r in cu if nv(r) == 'T1'),
             'T2': len(T2), 'T2_theo_ma': dict(dem2), 'T3': len(T3), 'T4': len(T4), 'T4_truoc_moc_03_2025': sum(d < MOC for _, _, d in pool[:n4]), 'T4_tu_moc': sum(d >= MOC for _, _, d in pool[:n4])}
    assert all(SP[d] == s for d in p2[:n2])
json.dump(TK, open(f'{O}/thong_ke.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(TK, ensure_ascii=False))
