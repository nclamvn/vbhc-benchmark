"""Tạo phiếu chấm mù cho T1 từ bài làm của các mô hình.
Dùng: python3 scripts/tao_phieu_cham_T1.py ket_qua/m1.jsonl ket_qua/m2.jsonl ...  ->  cham_T1/phieu_cham.csv, cham_T1/khoa_giai_ma.json
Phiếu xáo thứ tự và không ghi tên mô hình. Tệp khóa giải mã không đưa cho người chấm."""
import json, sys, csv, random, os, hashlib
D = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_de.jsonl', encoding='utf-8')}
G = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')}
rows = []
for f in sys.argv[1:]:
    for l in open(f, encoding='utf-8'):
        x = json.loads(l)
        if x['id'].startswith('T1-'): rows.append((x['id'], os.path.basename(f).replace('.jsonl', ''), x.get('tra_loi', '')))
random.Random(2026).shuffle(rows); os.makedirs('cham_T1', exist_ok=True); khoa = {}
with open('cham_T1/phieu_cham.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['ma_phieu', 'yeu_cau', 'bai_lam', 'van_ban_tham_chieu', 'A_dung_viec', 'B_dung_vai', 'C_van_phong', 'D_khong_bia', 'ghi_chu'])
    for i, (iid, mo_hinh, tl) in enumerate(rows, 1):
        ma = f'P{i:04d}'; khoa[ma] = {'id': iid, 'mo_hinh': mo_hinh, 'sha256_bai': hashlib.sha256(tl.encode()).hexdigest()}
        w.writerow([ma, D[iid]['de'], tl, G[iid]['dap_an']['van_ban_tham_chieu'], '', '', '', '', ''])
json.dump(khoa, open('cham_T1/khoa_giai_ma.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(rows), 'phiếu từ', len(sys.argv) - 1, 'mô hình -> cham_T1/phieu_cham.csv')
