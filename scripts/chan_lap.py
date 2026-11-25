"""Chặn lặp nguyên khối khi sinh văn bản (giao thức 1.3, QĐ-14).
Dừng ngay khi một đoạn vừa viết xong (từ 60 ký tự, đã bỏ số thứ tự đầu đoạn) trùng một đoạn trước đó, rồi cắt bỏ đoạn trùng.
Phạt lặp (giao thức 1.2) chỉ nhìn 64 token gần nhất nên không chặn được một khối 100–200 token lặp lại."""
import re
def _chuan(x): return re.sub(r'\s+', ' ', re.sub(r'^\s*(\d+|[a-zđ])[.)]\s*', '', x.strip().lower()))
def khoi_lap(van_ban):
    """Trả về vị trí cắt nếu đoạn hoàn chỉnh cuối cùng trùng một đoạn trước; None nếu chưa lặp."""
    phan = re.split(r'(\n\s*\n)', van_ban)
    doan = phan[0::2]
    if len(doan) < 3: return None
    xong = doan[:-1]                       # đoạn cuối có thể chưa viết xong
    cuoi = _chuan(xong[-1])
    if len(cuoi) >= 60 and cuoi in {_chuan(x) for x in xong[:-1]}:
        return len(''.join(phan[:2 * (len(xong) - 1)])).__int__()
    return None
