"""Giao thức 2.1 (thử): sau khi mô hình soạn, một bước tất định điền số và ngày cho viện dẫn mô hình đã để "…"
nếu phần mô tả khớp ≥60% âm tiết với đúng một văn bản trong tư liệu tra cứu của đề đó. Không thêm viện dẫn mới.
Dùng: python3 scripts/dien_can_cu.py <vào.jsonl> <ra.jsonl>"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tra_cuu as t
RE = re.compile(r'…/…/(NĐ-CP|NQ-CP|QĐ-TTg|TT-[A-ZĐa-z]+)(\s+ngày\s+…)?(\s+(?:của|do)[^;.]{0,50}?(?:về|quy định|sửa đổi|hướng dẫn)([^;.]{10,160}))')
def dien(bai, ds, nguong=0.6):
    def thay(m):
        mo = set(t.am(m.group(4)))
        diem = sorted(((len(mo & set(t.am(x[2]))) / max(1, len(mo)), x) for x in ds), key=lambda z: -z[0])
        if not diem or diem[0][0] < nguong or (len(diem) > 1 and diem[1][0] == diem[0][0]): return m.group(0)
        kh, ngay = diem[0][1][0], diem[0][1][1]; y, mth, d = ngay.split('-')
        return f'{kh.replace("QĐ-TTG", "QĐ-TTg")} ngày {int(d)}/{int(mth)}/{y}{m.group(3)}'
    return RE.sub(thay, bai)
if __name__ == '__main__':
    TC = t.TraCuu(); D = {json.loads(l)['id']: json.loads(l) for l in open(os.environ.get('VBHC_DE', 'm3/test_de.jsonl'), encoding='utf-8')}
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for l in open(sys.argv[1], encoding='utf-8'):
            r = json.loads(l); t.lam_giau_de(D[r['id']]['de'], TC, 8); r['tra_loi'] = dien(r['tra_loi'], t.lam_giau_de.ds)
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
