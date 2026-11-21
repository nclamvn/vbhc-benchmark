"""Luật chọn tệp đính kèm (vòng 3, theo kết quả kiểm 21/11/2026):
văn bản có nhiều tệp -> lấy PDF đầu tiên có số trong tên tệp trùng số ký hiệu;
không có thì lấy PDF đầu tiên; không có PDF thì lấy tệp đầu."""
import re
def so_cua(code):
    m = re.match(r'^\s*0*(\d+)', code or ''); return m.group(1) if m else None
def so_trong_ten(url):
    fn = url.rsplit('/', 1)[-1].lower()
    return {x.lstrip('0') or '0' for x in re.findall(r'\d+', fn)}
def la_pdf(url): return url.lower().split('?')[0].endswith('.pdf')
def chon(code, teps):
    n = so_cua(code)
    pdfs = [u for u in teps if la_pdf(u)]
    if n:
        for u in pdfs:
            if n in so_trong_ten(u): return u, 'pdf_dung_so'
    if pdfs: return pdfs[0], 'pdf_dau'
    return (teps[0], 'tep_dau') if teps else (None, 'khong_tep')
