"""M9 · Chấm v7 so với v6 khi kết quả từ Mac về (ket_qua/m9/).
Mỗi tệp giao thức 2.0 được điền căn cứ tất định thành 2.1 (scripts/dien_can_cu.py, cùng khối bộ máy và bảng đồng viện dẫn như lúc chạy).
Đo trên 41 bài T1: điểm T1, thể thức, bài sạch, viện dẫn sai mỗi bài, căn cứ đúng chỗ, phủ căn cứ, bài lặp.
Đo trên 20 văn bản mới (m9/de_moi.jsonl): bài sạch, viện dẫn sai mỗi bài, căn cứ đúng chỗ, phủ (so với m9/can_cu_moi.json). Chỉ ghi số.
Cổng M9 (so cùng điều kiện, giao thức 2.1): bài sạch không thấp hơn, viện dẫn sai mỗi bài không cao hơn, căn cứ đúng chỗ tăng.
Dùng: python3 scripts/m9_cham.py [thư mục, mặc định ket_qua/m9] → <thư mục>/bang_m9.json, <thư mục>/bang_m9.md
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import kiem_trung_thuc as k
D = sys.argv[1] if len(sys.argv) > 1 else 'ket_qua/m9'
I = k.nap_chi_muc()
RQP = re.compile(r'(\d{1,4})/(\d{4})/(NĐ-CP|NQ-CP|QĐ-TTg|TT-[A-ZĐ]+|TTLT-[A-ZĐ-]+)')
def nap(f): return {json.loads(l)['id']: json.loads(l) for l in open(f, encoding='utf-8')}
DA41, CC41 = nap('m3/test_dap_an.jsonl'), json.load(open('m3/can_cu_tham_chieu_T1.json', encoding='utf-8'))
DAM, CCM = nap('m9/dap_an_moi.jsonl'), json.load(open('m9/can_cu_moi.json', encoding='utf-8'))
def dien(vao, ra, env):
    if not os.path.exists(ra): subprocess.run([sys.executable, 'scripts/dien_can_cu.py', vao, ra], env={**os.environ, **env}, check=True)
    return ra
def can_cu(TL, CC):
    tong = trung = 0; that = sum(len(v) for v in CC.values())
    for i, a in TL.items():
        if i not in CC: continue
        s = {k.chuan(m.group(0)) for m in RQP.finditer(a)}; tong += len(s); trung += len(s & set(CC[i]))
    return (round(100 * trung / tong, 1) if tong else None), round(100 * trung / max(1, that), 1)
def do(f, DA, CC, co_diem=True):
    TL = {i: r.get('tra_loi', '') for i, r in nap(f).items()}; t = k.cham(I, DA, TL)[0]; cx, ph = can_cu(TL, CC)
    r = {'tep': f, 'n': len(TL), 'sach': t['bai_sach_pct'], 'sai_moi_bai': t['trich_dan_sai_moi_bai'], 'lap': t['bai_lap_pct'], 'can_cu_dung_cho': cx, 'phu': ph}
    if co_diem:
        d = json.loads(subprocess.run([sys.executable, 'scripts/cham_diem.py', f], capture_output=True, text=True, check=True).stdout)['T1']
        r.update(T1=d['diem'], the_thuc=d['the_thuc'])
    return r
V0 = {}; V11 = {'VBHC_SOT_BAN': 'v1.1', 'VBHC_DVD': 'm8/dong_vien_dan_c.json'}; VM = {**V11, 'VBHC_DE': 'm9/de_moi.jsonl'}
HANG = [('v6 (đã công bố, M7b)', 'khối bộ máy cũ', 'ket_qua/m7b/p20_qwen3_8b_tinh_chinh_v6.jsonl', 'ket_qua/m7b/p21_qwen3_8b_tinh_chinh_v6.jsonl'),
        ('v7', 'khối bộ máy cũ', f'{D}/p20_v7_sot0.jsonl', None, V0),
        ('v6', 'khối bộ máy v1.1', f'{D}/p20_v6_sot11.jsonl', None, V11),
        ('v7', 'khối bộ máy v1.1', f'{D}/p20_v7.jsonl', None, V11)]
B = []
for h in HANG:
    ten, dk, f20 = h[:3]
    if not os.path.exists(f20): print('chưa có', f20); continue
    f21 = h[3] or dien(f20, f20.replace('p20_', 'p21_'), h[4])
    B.append({'he': ten, 'dieu_kien': dk, '2.0': do(f20, DA41, CC41), '2.1': do(f21, DA41, CC41)})
M = []
for ten in ['v6', 'v7']:
    f = f'{D}/moi_{ten}.jsonl'
    if os.path.exists(f): M.append({'he': ten, '2.0': do(f, DAM, CCM, False), '2.1': do(dien(f, f.replace('moi_', 'moi21_'), VM), DAM, CCM, False)})
def cong(a, b):   # b thắng a?
    x, y = a['2.1'], b['2.1']
    return {'bài sạch không thấp hơn': y['sach'] >= x['sach'], 'viện dẫn sai mỗi bài không cao hơn': y['sai_moi_bai'] <= x['sai_moi_bai'],
            'căn cứ đúng chỗ tăng': (y['can_cu_dung_cho'] or 0) > (x['can_cu_dung_cho'] or 0)}
G = {}
by = {(r['he'], r['dieu_kien']): r for r in B}
if ('v7', 'khối bộ máy cũ') in by: G['v7 so với v6 đã công bố (khối cũ)'] = cong(by[('v6 (đã công bố, M7b)', 'khối bộ máy cũ')], by[('v7', 'khối bộ máy cũ')])
if ('v7', 'khối bộ máy v1.1') in by and ('v6', 'khối bộ máy v1.1') in by: G['v7 so với v6 (khối v1.1)'] = cong(by[('v6', 'khối bộ máy v1.1')], by[('v7', 'khối bộ máy v1.1')])
json.dump({'bo_de_41': B, 'van_ban_moi_20': M, 'cong': G}, open(f'{D}/bang_m9.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
f1 = lambda x: '—' if x is None else (f'{x:.2f}' if isinstance(x, float) and x < 5 else f'{x:.1f}').replace('.', ',')
L = ['# M9 · v7 so với v6', '', '## 41 bài T1 của bộ đề', '', '| Hệ | Khối bộ máy | Giao thức | T1 | Thể thức | Bài sạch | Viện dẫn sai/bài | Căn cứ đúng chỗ | Phủ | Bài lặp |', '|---|---|---|---|---|---|---|---|---|---|']
for r in B:
    for gt in ('2.0', '2.1'):
        x = r[gt]; L.append(f"| {r['he']} | {r['dieu_kien']} | {gt} | {f1(x['T1'])} | {f1(x['the_thuc'])} | {f1(x['sach'])}% | {f1(x['sai_moi_bai'])} | {f1(x['can_cu_dung_cho'])}% | {f1(x['phu'])}% | {f1(x['lap'])}% |")
L += ['', '## 20 văn bản mới nhất, chưa từng huấn luyện (chỉ ghi số)', '', '| Hệ | Giao thức | Bài sạch | Viện dẫn sai/bài | Căn cứ đúng chỗ | Phủ | Bài lặp |', '|---|---|---|---|---|---|---|']
for r in M:
    for gt in ('2.0', '2.1'):
        x = r[gt]; L.append(f"| {r['he']} | {gt} | {f1(x['sach'])}% | {f1(x['sai_moi_bai'])} | {f1(x['can_cu_dung_cho'])}% | {f1(x['phu'])}% | {f1(x['lap'])}% |")
L += ['', '## Cổng M9 (giao thức 2.1)', ''] + [f"- {ten}: " + ', '.join(f"{c} {'✓' if v else '✗'}" for c, v in g.items()) for ten, g in G.items()]
open(f'{D}/bang_m9.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
