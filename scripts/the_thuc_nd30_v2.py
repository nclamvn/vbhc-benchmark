"""M1 bản 2: thêm 3 luật sau khi bản 1 bỏ sót lỗi cài (hoa/thường của Tiêu ngữ, chữ viết tắt tên loại trong ký hiệu, số 0 trong ngày tháng)."""
import re
from the_thuc_nd30 import *
from the_thuc_nd30 import LUAT as _L1, nfc, chu, KXD, vung_dau, du_trang
TL = {'Thông báo': 'TB', 'Quyết định (cá biệt)': 'QĐ', 'Công điện': 'CĐ', 'Chỉ thị': 'CT', 'Nghị quyết (cá biệt)': 'NQ', 'Kế hoạch': 'KH', 'Báo cáo': 'BC', 'Hướng dẫn': 'HD'}
def L13(t, d):  # tiêu ngữ: chỉ viết hoa chữ đầu mỗi cụm
    m = re.search(r'Độc\s+[Ll]ập\s*[-–—]\s*Tự\s+[Dd]o\s*[-–—]\s*Hạnh\s+[Pp]húc', t[:1500])
    return 'Tiêu ngữ viết hoa sai (đúng: Độc lập - Tự do - Hạnh phúc)' if m and re.search(r'Lập|Do\b|Phúc', m.group(0)) else None
def L14(t, d):  # chữ viết tắt tên loại trong ký hiệu
    tl = TL.get(d['loai_van_ban'])
    if not tl: return None
    m = re.fullmatch(r'\d+/([A-ZĐ]+)-.+', d['so_ky_hieu_chuan'])
    return None if (m and m.group(1) == tl) else f'Ký hiệu không mang chữ viết tắt tên loại {tl}: {d["so_ky_hieu_chuan"]}'
def L15(t, d):  # ngày < 10 và tháng 1, 2 phải có số 0
    m = re.search(r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+\d{4}', t[:2500])
    if not m: return None
    dd, mm = m.groups()
    return f'Ngày tháng thiếu số 0 ở trước: {m.group(0)}' if (len(dd) == 1 and int(dd) < 10) or (len(mm) == 1 and int(mm) < 3) else None
LUAT = dict(_L1, L13=(L13, 'Hoa thường của Tiêu ngữ', 'PL I mục II.1'), L14=(L14, 'Chữ viết tắt tên loại trong ký hiệu', 'PL I mục II.3; PL III'), L15=(L15, 'Số 0 trong ngày tháng', 'PL I mục II.4'))
def kiem(d):
    t = nfc(d['text']); return {k: f(t, d) for k, (f, _, _) in LUAT.items()}
