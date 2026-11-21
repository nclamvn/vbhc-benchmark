"""Gộp các tệp *_diem.json thành bảng điểm M5 (Markdown), luôn kèm mốc luật viết tay.
Dùng: python3 scripts/bang_diem.py ket_qua/*_diem.json > docs/bang_diem.md"""
import json, sys, os
def dong(ten, o):
    t1, t2, t3 = o.get('T1', {}), o.get('T2', {}), o.get('T3', {})
    f = lambda x: '' if x is None else str(x).replace('.', ',')
    return f"| {ten} | {f(t1.get('diem'))} | {f(t1.get('the_thuc'))} | {f(t2.get('dung'))} | {f(t3.get('diem'))} | {f(t3.get('trich_yeu'))} | {o.get('thieu_tra_loi', 0)} |"
print('# Bảng điểm VBHC-Bench bản pilot\n\nĐiểm T1 chỉ gồm phần máy chấm được (thể thức, số, ngày, bám trích yếu). Điểm nội dung T1 do người chấm, báo cáo riêng.\n')
print('| Hệ | T1 máy chấm | T1 thể thức | T2 tìm lỗi | T3 trích thông tin | T3 riêng trích yếu | Mục thiếu trả lời |\n| --- | --- | --- | --- | --- | --- | --- |')
for f in sys.argv[1:]: print(dong(os.path.basename(f).replace('_diem.json', ''), json.load(open(f, encoding='utf-8'))['tong']))
