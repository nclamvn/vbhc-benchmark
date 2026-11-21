"""Đếm lại độc lập số liệu vòng 3 thẳng từ tệp đầu ra."""
import json, re
from collections import Counter
C = [json.loads(l) for l in open('data/stage4_v3/corpus.jsonl', encoding='utf-8')]
R = [json.loads(l) for l in open('data/stage4_v3/rejects.jsonl', encoding='utf-8')]
I = [json.loads(l) for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8') if json.loads(l)['ngay_ban_hanh'] >= '2020-03-05']
P = [json.loads(l) for l in open('data/prov/index_prov.jsonl', encoding='utf-8') if json.loads(l)['ngay_ban_hanh'] >= '2020-03-05']
a = {
 'chi_muc': {'vanban.chinhphu.vn': len(I), **dict(Counter(r['nguon'] for r in P))},
 'chi_muc_tong': len(I) + len(P),
 'toan_van_vao': len(C) + len(R), 'toan_van_giu': len(C), 'toan_van_loai': len(R), 'ly_do_loai': dict(Counter(r['reason'] for r in R)),
 'giu_theo_nguon': dict(Counter(c['nguon'] for c in C)), 'giu_theo_cap': dict(Counter(c['cap'] for c in C)),
 'giu_theo_loai': dict(Counter(c['loai_van_ban'] for c in C).most_common()), 'giu_theo_nam': dict(sorted(Counter(c['ngay_ban_hanh'][:4] for c in C).items())),
 'giu_theo_thoi_ky': dict(Counter(c['thoi_ky'] for c in C)), 'boc_chu': dict(Counter(c['boc_chu'] for c in C)),
 'do_tin_ocr_tb': round(sum(c['do_tin_ocr'] for c in C if c['do_tin_ocr']) / sum(1 for c in C if c['do_tin_ocr']), 1),
 'so_ky_hieu_toan_van': dict(Counter(c['doi_chieu']['so_ky_hieu_toan_van'] for c in C)), 'ngay_khop': sum(c['doi_chieu']['ngay_ban_hanh_toan_van'] for c in C),
 'ten_tep_khop': sum(c['doi_chieu']['so_trong_ten_tep'] for c in C),
 'da_che': {k: sum(c['da_che'].get(k, 0) for c in C) for k in ['email', 'so_dien_thoai', 'ho_ten', 'dia_chi', 'so_dinh_danh', 'ngay_sinh']},
 'ky_tu': sum(len(c['text']) for c in C), 'con_sot_email': sum(len(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', c['text'])) for c in C),
 'co_nguon_100pct': all(c['nguon_tep'] and c['nguon_chi_muc'] and c['sha256_tep'] for c in C),
}
json.dump(a, open('data/audit_stats_v3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(json.dumps(a, ensure_ascii=False, indent=1))
