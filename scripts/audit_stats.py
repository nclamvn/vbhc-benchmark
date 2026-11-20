"""Kiểm độc lập: đếm lại số liệu data card thẳng từ tệp đầu ra, không dùng biến của các bước trước."""
import json, csv, random, re
from collections import Counter
C = [json.loads(l) for l in open('data/stage4/corpus.jsonl', encoding='utf-8')]
R = [json.loads(l) for l in open('data/stage4/rejects.jsonl', encoding='utf-8')]
I = [json.loads(l) for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8') if json.loads(l)['ngay_ban_hanh'] >= '2020-03-05']
P = json.load(open('data/stage2/sample_plan.json', encoding='utf-8'))
out = {
 'chi_muc_tu_05_03_2020': len(I), 'chi_muc_khong_tep': sum(1 for r in I if not r['tep']),
 'chi_muc_ky_hieu_sai_trinh_bay': sum(1 for r in I if r['ky_hieu_sai_trinh_bay']), 'chi_muc_Ð_thay_Đ': sum(1 for r in I if r['ky_tu_la_trong_ky_hieu']),
 'chi_muc_theo_hinh_thuc': dict(Counter(r['hinh_thuc'] for r in I)), 'chi_muc_theo_loai': dict(Counter(r['loai_van_ban'] for r in I).most_common()),
 'mau_toan_van_ke_hoach': len(P), 'toan_van_giu': len(C), 'toan_van_loai': len(R), 'ly_do_loai': dict(Counter(r['reason'] for r in R)),
 'giu_theo_loai': dict(Counter(c['loai_van_ban'] for c in C).most_common()), 'giu_theo_nam': dict(sorted(Counter(c['ngay_ban_hanh'][:4] for c in C).items())),
 'giu_theo_thoi_ky': dict(Counter(c['thoi_ky'] for c in C)), 'boc_chu': dict(Counter(c['boc_chu'] for c in C)),
 'do_tin_ocr_trung_binh': round(sum(c['do_tin_ocr'] for c in C if c['do_tin_ocr']) / sum(1 for c in C if c['do_tin_ocr']), 1),
 'so_ky_hieu_toan_van': dict(Counter(c['doi_chieu']['so_ky_hieu_toan_van'] for c in C)), 'ngay_khop_toan_van': sum(c['doi_chieu']['ngay_ban_hanh_toan_van'] for c in C),
 'so_trong_ten_tep_khop': sum(c['doi_chieu']['so_trong_ten_tep'] for c in C), 'email_da_che': sum(c['da_che']['email'] for c in C), 'sdt_da_che': sum(c['da_che']['so_dien_thoai'] for c in C),
 'ky_tu_toan_van': sum(len(c['text']) for c in C),
 'con_sot_email': sum(len(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', c['text'])) for c in C),
}
json.dump(out, open('data/audit_stats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
rng = random.Random(42)
for c in rng.sample(C, 4):
    print('\n###', c['so_ky_hieu'], c['ngay_ban_hanh'], c['loai_van_ban'], '|', c['trich_yeu'][:90]); print(re.sub(r'\n{2,}', '\n', c['text'])[:700])
