"""M7b · Tập huấn luyện v6 (QĐ-16): sửa lỗi "không dám chép số" của v5.
v5 học để "…" vì khi dựng dữ liệu, văn bản cần dẫn thường không có trong tư liệu (285 chỗ che, 238 giữ).
v6: với 70% bài T1, mọi văn bản quy phạm trung ương mà bài thật dẫn (có trong chỉ mục, ban hành trước ngày soạn)
luôn được đưa vào tư liệu, trộn với văn bản nhiễu từ bộ tra cứu cho đủ 8 dòng, xếp ngẫu nhiên. 30% bài còn lại giữ
đúng điều kiện tra cứu thật như v5 (để mô hình vẫn biết để "…" khi danh sách không có văn bản cần dẫn).
Chỉ che viện dẫn không có trong tư liệu. T2 150, T3 150, T4 100 để ôn. Bộ kiểm tra không đổi: lúc chấm vẫn chỉ có tra cứu.
Dùng: python3 scripts/m7b_du_lieu_v6.py → m7b/train.jsonl, m7b/valid.jsonl, m7b/thong_ke.json
"""
import json, re, os, sys, random, collections, copy
sys.path.insert(0, 'scripts')
import m7_du_lieu_v5 as v5, tra_cuu as tcu, kiem_trung_thuc as k
rng = random.Random(20261127); TC = v5.TC
RE_DE = tcu.RE_DE

def tu_lieu(de, dich, kh_ban_than, co_dap_an):
    """Trả về lời yêu cầu đã làm giàu và tập ký hiệu trong tư liệu."""
    moi = tcu.lam_giau_de(de, TC, 8, bo_chinh_no=True); ds = list(tcu.lam_giau_de.ds)
    if not co_dap_an: return moi, {x[0] for x in ds}
    d, m, y = RE_DE.search(de).groups()[:3]; ngay = f'{y}-{int(m):02d}-{int(d):02d}'
    that = []
    for mm in v5.RE_QP.finditer(dich):
        kh = k.chuan(mm.group(0))
        if kh != k.chuan(kh_ban_than) and kh in TC.ngay and TC.ngay[kh][0] < ngay and kh not in [x[0] for x in that]:
            that.append((kh, *TC.ngay[kh]))
    if not that: return moi, {x[0] for x in ds}
    nhieu = [x for x in ds if x[0] not in {t[0] for t in that}][:max(0, 8 - len(that))]
    ds2 = that[:8] + nhieu; rng.shuffle(ds2)
    a, b = moi.index('\n\nTư liệu tra cứu'), moi.index('Bộ máy tại ngày ban hành:')
    dau = moi[a:].split('\n')[2]   # dòng tiêu đề khối tư liệu giữ nguyên
    khoi = '\n\n' + dau + '\n' + '\n'.join(tcu.dong_vb(*x) for x in ds2) + '\n'
    return moi[:a] + khoi + moi[b:], {x[0] for x in ds2}

def main():
    O = 'm7b'; os.makedirs(O, exist_ok=True); TK = {}
    for s, n2, n3, n4 in (('train', 150, 150, 100), ('valid', 30, 30, 20)):
        R = [json.loads(l) for l in open(f'm6b/{s}.jsonl', encoding='utf-8')]
        T1, dem = [], collections.Counter()
        for r in R:
            if v5.nv(r) != 'T1': continue
            r = copy.deepcopy(r); de = r['messages'][1]['content']; kh = re.search(r'Số, ký hiệu: (.*)', de).group(1)
            dap = rng.random() < 0.7; dem['co_dap_an_trong_tu_lieu' if dap else 'tra_cuu_that'] += 1
            r['messages'][1]['content'], cho = tu_lieu(de, r['messages'][2]['content'], kh, dap)
            giu = set(re.findall(r'Thủ tướng Chính phủ: ([^.]+)\.', r['messages'][1]['content']))
            t, a = v5.che_ngoai_danh_sach(r['messages'][2]['content'], cho, kh); t, b = v5.lam_sach(t, giu)
            r['messages'][2]['content'] = t; dem.update(a); dem.update(b); T1.append(r)
        from transformers import AutoTokenizer
        TOK = AutoTokenizer.from_pretrained(os.environ.get('VBHC_TOKENIZER', '/home/claude/m4/qwen25_05b'))
        vua = lambda r: len(TOK(TOK.apply_chat_template(r['messages'], tokenize=False))['input_ids']) <= 3000
        n0 = len(T1); T1 = [r for r in T1 if vua(r)]; dem['bo_qua_3000_token'] = n0 - len(T1)
        nhom = collections.defaultdict(list)
        for r in R: nhom[v5.nv(r)].append(r)
        for x in nhom.values(): rng.shuffle(x)
        rows = T1 + nhom['T2'][:n2] + nhom['T3'][:n3] + nhom['T4'][:n4]; rng.shuffle(rows)
        open(f'{O}/{s}.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
        TK[s] = {'tong': len(rows), 'T1': len(T1), 'T2': n2, 'T3': n3, 'T4': n4, 'T1_xu_ly': dict(dem)}
    json.dump(TK, open(f'{O}/thong_ke.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(TK, ensure_ascii=False))

if __name__ == '__main__': main()
