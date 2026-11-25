"""Dựng bảng xếp hạng VBHC-Bench pilot từ các tệp trả lời trong ket_qua/ (không cần GPU, không cần mạng).
Dùng: python3 scripts/bang_xep_hang.py   → BANG_XEP_HANG.md, ket_qua/bang_xep_hang.json
Mỗi con số trong bảng tính lại từ tệp trả lời bằng cham_diem.py (bộ chấm 1.1) và kiem_trung_thuc.py; điểm nội dung lấy từ các phiếu chấm mù đã lưu."""
import json, subprocess, sys
sys.path.insert(0, 'scripts'); import kiem_trung_thuc as k
P, M, B = 'ket_qua/pilot_2026-11-24/', 'ket_qua/m6/', 'ket_qua/m6b/'
HE = [  # tên, nhóm, tệp đủ 285 câu (giao thức 1.1), tệp T1 có phạt lặp (giao thức 1.2) nếu có
    ('Qwen3-8B v4 tinh chỉnh (mô hình cơ sở)', 'qwen3_8b_tinh_chinh_v4', B + 'qwen3_8b_tinh_chinh_v4.jsonl', B + 'p12_qwen3_8b_tinh_chinh_v4.jsonl'),
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
out = []
for ten, ma, f, f12 in HE:
    d = cham(f); r = {'he': ten, 'ma': ma, 'tong_hop': d['tong_hop'], 'T1': d['T1']['diem'], 'T1_the_thuc': d['T1']['the_thuc'], 'T2': d['T2']['dung'], 'T3': d['T3']['diem']}
    if ma != 'moc_luat':
        t = tt(f); r.update(sach_11=t['bai_sach_pct'], lap_11=t['bai_lap_pct'])
    if f12:
        d12 = cham(f12)['T1']; t12 = tt(f12); r.update(T1_12=d12['diem'], T1_the_thuc_12=d12['the_thuc'], sach_12=t12['bai_sach_pct'], lap_12=t12['bai_lap_pct'])
    r['noi_dung'] = [list(ND[x]) for x in (ma, ma + '@p12') if x in ND]
    out.append(r)
json.dump(out, open('ket_qua/bang_xep_hang.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# Bảng xếp hạng VBHC-Bench · pilot 25/11/2026', '',
     'Tính lại bằng `python3 scripts/bang_xep_hang.py` từ các tệp trả lời trong `ket_qua/`. Bộ kiểm tra có 285 câu: T1 soạn văn bản 41 câu, T2 tìm lỗi thể thức 94 câu, T3 trích thông tin 150 câu. Tổng hợp là trung bình đều của ba nhiệm vụ, bộ chấm 1.1, giải mã tham lam.', '',
     '## Bảng chính (giao thức 1.1)', '', '| # | Hệ | Tổng hợp | T1 | T1 thể thức | T2 | T3 | T1 bài sạch | T1 bài lặp |', '|---|---|---|---|---|---|---|---|---|']
for i, r in enumerate(sorted(out, key=lambda r: -r['tong_hop']), 1):
    L.append(f"| {i} | {r['he']} | **{f1(r['tong_hop'])}** | {f1(r['T1'])} | {f1(r['T1_the_thuc'])} | {f1(r['T2'])} | {f1(r['T3'])} | {f1(r.get('sach_11'))}% | {f1(r.get('lap_11'))}% |".replace('—%', '—'))
L += ['', '## Phần soạn văn bản với phạt lặp (giao thức 1.2)', '', 'Cấu hình: `repetition_penalty` 1,1, cửa sổ 64 token, chỉ áp cho T1. Bảng này công bố riêng, không trộn vào bảng chính.', '',
      '| Hệ | T1 | T1 thể thức | Bài sạch | Bài lặp |', '|---|---|---|---|---|']
for r in sorted([r for r in out if 'T1_12' in r], key=lambda r: -r['sach_12']):
    L.append(f"| {r['he']} | {f1(r['T1_12'])} | {f1(r['T1_the_thuc_12'])} | {f1(r['sach_12'])}% | {f1(r['lap_12'])}% |")
L += ['', '## Chấm mù nội dung T1 (chuyên gia mô phỏng · AI)', '',
      'Thang 8 điểm, gồm bốn tiêu chí 0–2: đúng việc, đúng vai và thẩm quyền, văn phong, không bịa (`docs/huong_dan_cham_T1.md`). Mỗi hệ có 13 đề. Chỉ so điểm trong cùng một phiên chấm.', '',
      '| Hệ | Điểm /8 (phiên, giao thức) |', '|---|---|']
for r in out:
    if r['noi_dung']: L.append(f"| {r['he']} | " + ' · '.join(f"{a:.2f} ({b})".replace('.', ',', 1) for a, b in r['noi_dung']) + ' |')
L += ['', '## Cách đọc và giới hạn', '',
      '- **Bài sạch:** bộ kiểm trung thực bằng máy (`scripts/kiem_trung_thuc.py`) không bắt được lỗi nào. Bộ kiểm đối chiếu viện dẫn với chỉ mục 24.874 văn bản, và bắt người ký sai vai, tên cơ quan sai thời điểm, bài lặp. Chạy trên 41 văn bản thật, bộ kiểm cho 97,6% bài sạch.',
      '- **Chấm nội dung do AI đóng vai**, chưa phải chấm độc lập. Phiên M6b là phiên duy nhất so v4 với Qwen3 gốc trong cùng điều kiện: v4 thắng 8, hòa 1, thua 4 trên 13 đề, p ≈ 0,39.',
      '- **T3 cùng phân bố với dữ liệu huấn luyện** (đáp án và dữ liệu huấn luyện đều lấy từ chỉ mục cổng). Điểm gần 100 không chứng minh mô hình tổng quát hoá.',
      '- **T2 nên dùng luật viết tay.** Mọi mô hình đều thiên về một đáp án.',
      '- **Qwen2.5-0.5B chạy trên CPU**, nên không có bảng giao thức 1.2.', '',
      '## Gửi kết quả', '', 'Chạy hệ của bạn trên `m3/test_de.jsonl`, mỗi dòng ghi `{"id": ..., "tra_loi": ...}`, rồi chấm bằng `python3 scripts/cham_diem.py <tệp>` và `python3 scripts/kiem_trung_thuc.py m3/chi_muc_kiem_trung_thuc.csv.xz m3/test_dap_an.jsonl <tệp>`. Mở pull request thêm tệp trả lời vào `ket_qua/` và một dòng vào `HE` trong `scripts/bang_xep_hang.py`. Ghi rõ giao thức giải mã bạn dùng.', '']
open('BANG_XEP_HANG.md', 'w', encoding='utf-8').write('\n'.join(L))
print('\n'.join(L[:20]))
