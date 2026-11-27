"""Đo cổng nghiệm thu M8 trên một tập huấn luyện đã dựng (bài soạn văn bản T1 của train.jsonl).
Đo: tỷ lệ từng loại, tỷ lệ bài từ 03/2025, thông tin cá nhân máy kiểm (cùng biểu thức của scripts/pii_check.py, chạy trên toàn bộ bài, không lấy mẫu).
Dùng: python3 scripts/m8_kiem_cong.py m8b_6000 m8c_6000 ...  → in bảng, ghi ket_qua/dot_cao/cong_<thư mục>.json
"""
import json, re, sys, collections, os
src = open('scripts/pii_check.py', encoding='utf-8').read()
g = {}; exec(src[src.index('NAMEW'):src.index('tot = ')], {'re': re}, g); CHECKS = g['checks']
NGUONG = {'Kế hoạch': ('≥', 0.05), 'Chỉ thị': ('≥', 0.05), 'Báo cáo': ('≥', 0.02)}
RE_DE = re.compile(r'loại "([^"]+)"[\s\S]*?Ngày ban hành: ngày (\d+) tháng (\d+) năm (\d{4})')

def do(thu_muc):
    T1 = []
    for l in open(f'{thu_muc}/train.jsonl', encoding='utf-8'):
        r = json.loads(l); u = next(m['content'] for m in r['messages'] if m['role'] == 'user'); m = RE_DE.search(u)
        if m and u.startswith('Soạn hoàn chỉnh'): T1.append((m[1], f'{m[4]}-{int(m[3]):02d}-{int(m[2]):02d}', r['messages'][-1]['content']))
    n = len(T1); loai = collections.Counter(x[0] for x in T1)
    pii = {k: sum(len(p.findall(x[2])) for x in T1) for k, p in CHECKS.items()}
    kq = {'thu_muc': thu_muc, 'bai_soan': n, 'ty_le_loai': {k: round(v / n, 3) for k, v in loai.most_common()},
          'tu_03_2025': round(sum(x[1] >= '2025-03-01' for x in T1) / n, 3), 'pii_may_kiem': pii}
    kq['cong'] = {**{f'{L} {d} {int(t * 100)}%': (kq['ty_le_loai'].get(L, 0) >= t) for L, (d, t) in NGUONG.items()},
                  'mọi loại ≤ 35%': max(kq['ty_le_loai'].values()) <= 0.35, 'từ 03/2025 ≥ 40%': kq['tu_03_2025'] >= 0.40}
    os.makedirs('ket_qua/dot_cao', exist_ok=True)
    json.dump(kq, open(f'ket_qua/dot_cao/cong_{os.path.basename(thu_muc.rstrip("/"))}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return kq

if __name__ == '__main__':
    for t in sys.argv[1:]: print(json.dumps(do(t), ensure_ascii=False))
