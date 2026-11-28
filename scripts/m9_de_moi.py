"""M9 · Bộ đề nhỏ từ 20 văn bản mới nhất đã để ngoài huấn luyện (10 của đợt B, 10 của đợt C, nhãn 'de_moi').
Chỉ ghi số, không làm cổng (bộ đề chính thức mới là việc của M8.6). Lời yêu cầu T1 dựng đúng như m3/test_de.jsonl.
Dùng: python3 scripts/m9_de_moi.py → m9/de_moi.jsonl, m9/dap_an_moi.jsonl, m9/can_cu_moi.json
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiem_trung_thuc as k
HE = 'Bạn là trợ lý soạn thảo và rà soát văn bản hành chính Việt Nam theo Nghị định 30/2020/NĐ-CP.'
def co_quan(c): return c.get('co_quan_ten') or {'VPCP': 'Văn phòng Chính phủ', 'TTg': 'Thủ tướng Chính phủ'}.get(c['co_quan_ky_hieu'], c['co_quan_ky_hieu'])
def de_T1(c):
    y, m, d = c['ngay_ban_hanh'].split('-')
    return (f'Soạn hoàn chỉnh một văn bản loại "{c["loai_van_ban"]}" đúng thể thức Nghị định 30/2020/NĐ-CP với thông tin sau:\n- Cơ quan ban hành: {co_quan(c)}\n- Số, ký hiệu: {c["so_ky_hieu_chuan"]}\n'
            f'- Ngày ban hành: ngày {d} tháng {m if int(m) < 3 else int(m)} năm {y}\n- Trích yếu nội dung: {c["trich_yeu"]}\nViết đủ các thành phần thể thức và phần nội dung phù hợp với trích yếu. Chỉ trả về văn bản.')
CT = json.load(open('m8/chia_tap_dot_c.json', encoding='utf-8')); ma = sorted(d for d, v in CT.items() if v == 'de_moi')
BY = {}
for l in open('data/stage4_v7/corpus.jsonl', encoding='utf-8'):
    c = json.loads(l)
    if c['docid'] in ma: BY[c['docid']] = c
I = k.nap_chi_muc(); DE, DA, CC = [], [], {}
for j, d in enumerate(sorted(ma, key=lambda d: (BY[d]['ngay_ban_hanh'], d)), 1):
    c = BY[d]; i = f'M9M-{j:04d}'
    DE.append({'id': i, 'nhiem_vu': 'T1', 'he_thong': HE, 'de': de_T1(c)})
    DA.append({'id': i, 'nhiem_vu': 'T1', 'docid': d, 'dap_an': {'van_ban_tham_chieu': c['text'], 'so_ky_hieu_chuan': c['so_ky_hieu_chuan'], 'loai_van_ban': c['loai_van_ban'], 'ngay_ban_hanh': c['ngay_ban_hanh'], 'trich_yeu': c['trich_yeu']}})
    CC[i] = sorted({kh for kh, kq in k.kiem_trich_dan(c['text'], I, c['ngay_ban_hanh'], c['so_ky_hieu_chuan']) if kq == 'dung'})
w = lambda f, R: open(f, 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in R))
w('m9/de_moi.jsonl', DE); w('m9/dap_an_moi.jsonl', DA); json.dump(CC, open('m9/can_cu_moi.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
import collections; print(len(DE), collections.Counter(BY[d]['loai_van_ban'] for d in ma), sum(len(v) for v in CC.values()), 'căn cứ kiểm được')
