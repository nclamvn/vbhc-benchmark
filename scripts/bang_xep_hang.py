"""Dựng bảng xếp hạng VBHC-Bench pilot từ các tệp trả lời trong ket_qua/ (không cần GPU, không cần mạng).
Dùng: python3 scripts/bang_xep_hang.py   → BANG_XEP_HANG.md, ket_qua/bang_xep_hang.json
Mỗi con số trong bảng tính lại từ tệp trả lời bằng cham_diem.py (bộ chấm 1.1) và kiem_trung_thuc.py; điểm nội dung lấy từ các phiếu chấm mù đã lưu."""
import json, subprocess, sys
sys.path.insert(0, 'scripts'); import kiem_trung_thuc as k
P, M, B = 'ket_qua/pilot_2026-11-24/', 'ket_qua/m6/', 'ket_qua/m6b/'
Q13, M7, M7B = 'ket_qua/p13/', 'ket_qua/m7/', 'ket_qua/m7b/'
HE = [  # tên, nhóm, tệp đủ 285 câu (giao thức 1.1), tệp T1 có phạt lặp (giao thức 1.2) nếu có
    ('Qwen3-8B v6 tinh chỉnh (mô hình cơ sở, dùng với giao thức 2.1)', 'qwen3_8b_tinh_chinh_v6', M7B + 'qwen3_8b_tinh_chinh_v6.jsonl', None),
    ('Qwen3-8B v5 tinh chỉnh', 'qwen3_8b_tinh_chinh_v5', M7 + 'qwen3_8b_tinh_chinh_v5.jsonl', None),
    ('Qwen3-8B v4 tinh chỉnh', 'qwen3_8b_tinh_chinh_v4', B + 'qwen3_8b_tinh_chinh_v4.jsonl', B + 'p12_qwen3_8b_tinh_chinh_v4.jsonl'),
    ('Qwen3-8B v3 tinh chỉnh', 'qwen3_8b_tinh_chinh_v3', M + 'qwen3_8b_tinh_chinh_v3.jsonl', B + 'p12_qwen3_8b_tinh_chinh_v3.jsonl'),
    ('Llama-3.1-8B tinh chỉnh', 'llama31_8b_tinh_chinh', P + 'llama31_8b_tinh_chinh.jsonl', B + 'p12_llama31_8b_tinh_chinh.jsonl'),
    ('Qwen3-8B v2 tinh chỉnh', 'qwen3_8b_tinh_chinh_v2', M + 'qwen3_8b_tinh_chinh_v2.jsonl', None),
    ('Luật viết tay (không mô hình)', 'moc_luat', 'm3/moc_luat.jsonl', None),
    ('Qwen3-8B gốc', 'qwen3_8b_goc', P + 'qwen3_8b_goc.jsonl', B + 'p12_qwen3_8b_goc.jsonl'),
    ('Llama-3.1-8B gốc', 'llama31_8b_goc', P + 'llama31_8b_goc.jsonl', B + 'p12_llama31_8b_goc.jsonl'),
    ('Qwen2.5-0.5B tinh chỉnh', 'qwen25_05b_tinh_chinh', P + 'qwen25_05b_tinh_chinh.jsonl', None),
    ('Qwen2.5-0.5B gốc', 'qwen25_05b_goc', P + 'qwen25_05b_goc.jsonl', None)]
I = k.nap_chi_muc(); DA = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')}
def cham(f): return json.loads(subprocess.run([sys.executable, 'scripts/cham_diem.py', f], capture_output=True, text=True, check=True).stdout)
def tt(f):
    TL = {json.loads(l)['id']: json.loads(l).get('tra_loi', '') for l in open(f, encoding='utf-8')}
    return k.cham(I, DA, TL)[0]
f1 = lambda x: '—' if x is None else f'{x:.1f}'.replace('.', ',')
ND = {**{h: (v['tong_8'], 'M5, tham lam') for h, v in json.load(open(P + 'diem_T1_mo_phong_tong.json', encoding='utf-8')).items() if isinstance(v, dict)},
      **{h: (v['tong_8'], 'M6, tham lam') for h, v in json.load(open(M + 'diem_T1_mo_phong_tong.json', encoding='utf-8')).items() if isinstance(v, dict)}}
for h, v in json.load(open(B + 'diem_T1_mo_phong_tong.json', encoding='utf-8')).items():
    if isinstance(v, dict) and 'tong_8' in v: ND[h.replace('_p12', '') + '@p12'] = (v['tong_8'], 'M6b, phạt lặp')
for h, v in json.load(open(M7B + 'diem_T1_mo_phong_tong.json', encoding='utf-8')).items():
    if isinstance(v, dict) and 'tong_8' in v: ND[h.rsplit('_p2', 1)[0] + '@m7'] = (v['tong_8'], 'M7, giao thức ' + ('2.1' if h.endswith('p21') else '2.0'))
out = []
for ten, ma, f, f12 in HE:
    d = cham(f); r = {'he': ten, 'ma': ma, 'tong_hop': d['tong_hop'], 'T1': d['T1']['diem'], 'T1_the_thuc': d['T1']['the_thuc'], 'T2': d['T2']['dung'], 'T3': d['T3']['diem']}
    if ma != 'moc_luat':
        t = tt(f); r.update(sach_11=t['bai_sach_pct'], lap_11=t['bai_lap_pct'])
    if f12:
        d12 = cham(f12)['T1']; t12 = tt(f12); r.update(T1_12=d12['diem'], T1_the_thuc_12=d12['the_thuc'], sach_12=t12['bai_sach_pct'], lap_12=t12['bai_lap_pct'])
    r['noi_dung'] = [list(ND[x]) for x in (ma, ma + '@p12', ma + '@m7') if x in ND]
    out.append(r)
CC = json.load(open('m3/can_cu_tham_chieu_T1.json', encoding='utf-8'))
RQP = __import__('re').compile(r'(\d{1,4})/(\d{4})/(NĐ-CP|NQ-CP|QĐ-TTg|TT-[A-ZĐ]+|TTLT-[A-ZĐ-]+)')
def can_cu(f):
    tong = trung = 0; that = sum(len(v) for v in CC.values())
    for l in open(f, encoding='utf-8'):
        r = json.loads(l)
        if r['id'] not in CC: continue
        a = {k.chuan(m.group(0)) for m in RQP.finditer(r.get('tra_loi', ''))}; ref = set(CC[r['id']])
        tong += len(a); trung += len(a & ref)
    return (100 * trung / tong if tong else None), 100 * trung / that
T13 = [('Qwen3-8B v4 tinh chỉnh', Q13 + 'p13_qwen3_8b_tinh_chinh_v4.jsonl'), ('Qwen3-8B v3 tinh chỉnh', Q13 + 'p13_qwen3_8b_tinh_chinh_v3.jsonl'),
       ('Llama-3.1-8B tinh chỉnh', Q13 + 'p13_llama31_8b_tinh_chinh.jsonl'), ('Qwen3-8B gốc', Q13 + 'p13_qwen3_8b_goc.jsonl'), ('Llama-3.1-8B gốc', Q13 + 'p13_llama31_8b_goc.jsonl'),
       ('Qwen3-14B gốc', M7 + 'p13_qwen3_14b_goc.jsonl'), ('Qwen3-30B-A3B gốc', M7 + 'p13_qwen3_30b_a3b_goc.jsonl')]
T20 = [('Qwen3-8B v6 tinh chỉnh', '2.1', M7B + 'p21_qwen3_8b_tinh_chinh_v6.jsonl'), ('Qwen3-8B v6 tinh chỉnh', '2.0', M7B + 'p20_qwen3_8b_tinh_chinh_v6.jsonl'),
       ('Qwen3-8B v5 tinh chỉnh', '2.1', M7 + 'p21_qwen3_8b_tinh_chinh_v5.jsonl'), ('Qwen3-8B v5 tinh chỉnh', '2.0', M7 + 'p20_qwen3_8b_tinh_chinh_v5.jsonl'),
       ('Qwen3-8B v4 tinh chỉnh', '2.0', M7 + 'p20_qwen3_8b_tinh_chinh_v4.jsonl'), ('Qwen3-14B gốc', '2.0', M7 + 'p20_qwen3_14b_goc.jsonl'), ('Qwen3-8B gốc', '2.0', M7 + 'p20_qwen3_8b_goc.jsonl')]
bang13, bang20 = [], []
for ten, f in T13:
    d = cham(f)['T1']; t = tt(f); cx, ph = can_cu(f)
    bang13.append({'he': ten, 'T1': d['diem'], 'the_thuc': d['the_thuc'], 'sach': t['bai_sach_pct'], 'sai_moi_bai': t['trich_dan_sai_moi_bai'], 'thoi_diem': t['bai_sai_thoi_diem_pct'], 'lap': t['bai_lap_pct'], 'can_cu_chinh_xac': cx, 'can_cu_phu': ph})
for ten, gt, f in T20:
    d = cham(f)['T1']; t = tt(f); cx, ph = can_cu(f)
    bang20.append({'he': ten, 'giao_thuc': gt, 'T1': d['diem'], 'the_thuc': d['the_thuc'], 'sach': t['bai_sach_pct'], 'sai_moi_bai': t['trich_dan_sai_moi_bai'], 'thoi_diem': t['bai_sai_thoi_diem_pct'], 'lap': t['bai_lap_pct'], 'can_cu_chinh_xac': cx, 'can_cu_phu': ph})
out = {'bang_chinh': out, 'giao_thuc_1_3': bang13, 'giao_thuc_2': bang20}
json.dump(out, open('ket_qua/bang_xep_hang.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
f2 = lambda x: '—' if x is None else f'{x:.2f}'.replace('.', ',')
bang13, bang20, out = out['giao_thuc_1_3'], out['giao_thuc_2'], out['bang_chinh']
L = ['# Bảng xếp hạng VBHC-Bench · pilot (cập nhật 27/11/2026)', '',
     'Tính lại bằng `python3 scripts/bang_xep_hang.py` từ các tệp trả lời trong `ket_qua/`. Bộ kiểm tra có 285 câu: T1 soạn văn bản 41 câu, T2 tìm lỗi thể thức 94 câu, T3 trích thông tin 150 câu. Tổng hợp là trung bình đều của ba nhiệm vụ, bộ chấm 1.1, giải mã tham lam.', '',
     '## Bảng chính (giao thức 1.1)', '', '| # | Hệ | Tổng hợp | T1 | T1 thể thức | T2 | T3 | T1 bài sạch | T1 bài lặp |', '|---|---|---|---|---|---|---|---|---|']
for i, r in enumerate(sorted(out, key=lambda r: -r['tong_hop']), 1):
    L.append(f"| {i} | {r['he']} | **{f1(r['tong_hop'])}** | {f1(r['T1'])} | {f1(r['T1_the_thuc'])} | {f1(r['T2'])} | {f1(r['T3'])} | {f1(r.get('sach_11'))}% | {f1(r.get('lap_11'))}% |".replace('—%', '—'))
L += ['', '## Phần soạn văn bản với phạt lặp (giao thức 1.2)', '', 'Cấu hình: `repetition_penalty` 1,1, cửa sổ 64 token, chỉ áp cho T1. Bảng này công bố riêng, không trộn vào bảng chính.', '',
      '| Hệ | T1 | T1 thể thức | Bài sạch | Bài lặp |', '|---|---|---|---|---|']
for r in sorted([r for r in out if 'T1_12' in r], key=lambda r: -r['sach_12']):
    L.append(f"| {r['he']} | {f1(r['T1_12'])} | {f1(r['T1_the_thuc_12'])} | {f1(r['sach_12'])}% | {f1(r['lap_12'])}% |")
L += ['', '## Phần soạn văn bản, giao thức 1.3 (phạt lặp + dừng khi lặp nguyên đoạn)', '',
      '**Căn cứ đúng chỗ:** tỷ lệ viện dẫn văn bản quy phạm trung ương trong bài trùng với văn bản bài thật đã dẫn (`m3/can_cu_tham_chieu_T1.json`). **Phủ:** tỷ lệ căn cứ của bài thật được bài viết dẫn lại.', '',
      '| Hệ | T1 | Thể thức | Bài sạch | Viện dẫn sai mỗi bài | Sai thời điểm | Lặp | Căn cứ đúng chỗ | Phủ căn cứ |', '|---|---|---|---|---|---|---|---|---|']
for r in sorted(bang13, key=lambda r: -r['sach']):
    L.append(f"| {r['he']} | {f1(r['T1'])} | {f1(r['the_thuc'])} | {f1(r['sach'])}% | {f2(r['sai_moi_bai'])} | {f1(r['thoi_diem'])}% | {f1(r['lap'])}% | {f1(r['can_cu_chinh_xac'])}% | {f1(r['can_cu_phu'])}% |".replace('—%', '—'))
L += ['', '## Phần soạn văn bản có tra cứu (giao thức 2.0 và 2.1)', '',
      'Giao thức 2.0: lời yêu cầu T1 kèm 8 văn bản quy phạm tra được (`scripts/tra_cuu.py`, chỉ dùng chỉ mục công khai và tập huấn luyện; phủ 65,9% căn cứ thật) và bảng bộ máy theo ngày ban hành; giải mã như 1.3. Giao thức 2.1: 2.0 cộng bước điền số và ngày tất định, không dùng mô hình (`scripts/dien_can_cu.py`). Đề bài khác bảng chính nên không so trực tiếp với bảng 1.x.', '',
      '| Hệ | Giao thức | T1 | Thể thức | Bài sạch | Viện dẫn sai mỗi bài | Sai thời điểm | Lặp | Căn cứ đúng chỗ | Phủ căn cứ |', '|---|---|---|---|---|---|---|---|---|---|']
for r in bang20:
    L.append(f"| {r['he']} | {r['giao_thuc']} | {f1(r['T1'])} | {f1(r['the_thuc'])} | {f1(r['sach'])}% | {f2(r['sai_moi_bai'])} | {f1(r['thoi_diem'])}% | {f1(r['lap'])}% | {f1(r['can_cu_chinh_xac'])}% | {f1(r['can_cu_phu'])}% |".replace('—%', '—'))
L += ['', '## Chấm mù nội dung T1 (chuyên gia mô phỏng · AI)', '',
      'Thang 8 điểm, gồm bốn tiêu chí 0–2: đúng việc, đúng vai và thẩm quyền, văn phong, không bịa (`docs/huong_dan_cham_T1.md`). Mỗi hệ có 13 đề. Chỉ so điểm trong cùng một phiên chấm.', '',
      '| Hệ | Điểm /8 (phiên, giao thức) |', '|---|---|']
for r in out:
    if r['noi_dung']: L.append(f"| {r['he']} | " + ' · '.join(f"{a:.2f} ({b})".replace('.', ',', 1) for a, b in r['noi_dung']) + ' |')
L += ['', '## Cách đọc và giới hạn', '',
      '- **Bài sạch:** bộ kiểm trung thực bằng máy (`scripts/kiem_trung_thuc.py`) không bắt được lỗi nào. Bộ kiểm đối chiếu viện dẫn với chỉ mục 24.874 văn bản, và bắt người ký sai vai, tên cơ quan sai thời điểm, bài lặp. Chạy trên 41 văn bản thật, bộ kiểm cho 97,6% bài sạch.',
      '- **Chấm nội dung do AI đóng vai**, chưa phải chấm độc lập. Phiên M6b: v4 thắng Qwen3 gốc 8, hòa 1, thua 4 trên 13 đề, p ≈ 0,39. Phiên M7 (có tra cứu): v6 + 2.1 thắng v4 + 2.0 6–2–5, thắng Qwen3 gốc + 2.0 5–5–3; chưa có ý nghĩa thống kê.',
      '- **Mô hình cơ sở v6 phải dùng kèm giao thức 2.1.** Không tra cứu và giải mã tham lam, v6 lặp ở 48,8% số bài. Theo 2.1, v6 trượt điều kiện phủ căn cứ (17,5% so với mốc 49%): v6 thường để "…" cho số căn cứ thay vì chép từ tư liệu. v4 + 2.0 phủ cao hơn nhưng 79% căn cứ là thừa.',
      '- **Lỗi dữ liệu đã biết ở v5, v6:** bước che họ tên che nhầm "Hà Nội" sau ký hiệu "TTg" (290 bài huấn luyện) và chữ "Bộ Tài" trong "Bộ trưởng Bộ Tài nguyên…", nên bài có thể ra "[Họ và tên], ngày…". Sẽ sửa ở M8.',
      '- **T3 cùng phân bố với dữ liệu huấn luyện** (đáp án và dữ liệu huấn luyện đều lấy từ chỉ mục cổng). Điểm gần 100 không chứng minh mô hình tổng quát hoá.',
      '- **T2 nên dùng luật viết tay.** Mọi mô hình đều thiên về một đáp án.',
      '- **Qwen2.5-0.5B chạy trên CPU**, nên không có bảng giao thức 1.2.', '',
      '## Gửi kết quả', '', 'Chạy hệ của bạn trên `m3/test_de.jsonl`, mỗi dòng ghi `{"id": ..., "tra_loi": ...}`, rồi chấm bằng `python3 scripts/cham_diem.py <tệp>` và `python3 scripts/kiem_trung_thuc.py m3/chi_muc_kiem_trung_thuc.csv.xz m3/test_dap_an.jsonl <tệp>`. Mở pull request thêm tệp trả lời vào `ket_qua/` và một dòng vào `HE` trong `scripts/bang_xep_hang.py`. Ghi rõ giao thức giải mã bạn dùng.', '']
open('BANG_XEP_HANG.md', 'w', encoding='utf-8').write('\n'.join(L))
print('\n'.join(L[:20]))
