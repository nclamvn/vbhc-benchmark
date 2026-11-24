"""M1 · Bộ luật thể thức NĐ 30/2020/NĐ-CP (Điều 8, Phụ lục I) kiểm được trên VĂN BẢN CHỮ.
Chỉ kiểm thành phần thể thức có mặt và đúng mẫu. KHÔNG kiểm phông, cỡ chữ, lề, vị trí (cần tệp gốc có bố cục).
Mỗi luật trả về None (đạt) hoặc chuỗi mô tả lỗi."""
import re, unicodedata
def nfc(s): return unicodedata.normalize('NFC', s)
def khong_dau(s):
    s = unicodedata.normalize('NFD', s.replace('Đ', 'D').replace('đ', 'd'))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').upper()
CO_TEN_LOAI = {'Thông báo': 'THONG BAO', 'Quyết định (cá biệt)': 'QUYET DINH', 'Công điện': 'CONG DIEN', 'Chỉ thị': 'CHI THI',
               'Nghị quyết (cá biệt)': 'NGHI QUYET', 'Kế hoạch': 'KE HOACH', 'Báo cáo': 'BAO CAO', 'Hướng dẫn': 'HUONG DAN'}
def chu(s): return re.sub(r'[^A-Z0-9]', '', khong_dau(s))
def du_trang(d): return d.get('tong_so_trang') is None or len(d.get('trang_da_boc') or []) >= (d.get('tong_so_trang') or 0)
KXD = 'KXĐ'  # không xác định được: bản bóc chữ thiếu trang giữa nên không kết luận
def L01(t, d): return None if 'CONGHOAXAHOICHUNGHIAVIETNAM' in chu(t[:1500]) else 'Thiếu Quốc hiệu'
def L02(t, d): return None if 'DOCLAPTUDOHANHPHUC' in chu(t[:1500]) else 'Thiếu hoặc sai Tiêu ngữ'
def L03(t, d): return None if re.search(r'S[ốôóồo]\s*[:;]', t[:2000], re.I) else 'Thiếu dòng "Số:"'
def L04(t, d):
    k = d['so_ky_hieu_chuan']; X = r'[A-Za-zĐđ0-9&.]+'
    if d['loai_van_ban'] == 'Công văn':
        return None if re.fullmatch(r'\d+/' + X + '(-' + X + ')*', k) else f'Ký hiệu công văn không theo mẫu số/CQ-ĐV: {k}'
    return None if re.fullmatch(r'\d+/[A-ZĐ]{2,6}-' + X + '(-' + X + ')*', k) else f'Ký hiệu không theo mẫu số/TL-CQ: {k}'
def vung_dau(t):
    """Phần đầu văn bản: từ đầu đến hết 6 dòng có chữ sau dòng Tiêu ngữ (nơi đặt số, ký hiệu, địa danh, ngày tháng, tên loại)."""
    ls = t[:3000].split('\n'); i0 = next((i for i, l in enumerate(ls) if 'DOCLAP' in chu(l) or 'HANHPHUC' in chu(l)), 0)
    out, n = ls[:i0 + 1], 0
    for l in ls[i0 + 1:]:
        out.append(l); n += bool(l.strip())
        if n >= 6: break
    return '\n'.join(out)
def L05(t, d): return None if re.search(r'ng[aà]y.{0,8}?th[aáả]ng.{0,8}?n[aăãầ]m\s*\d{4}', vung_dau(t), re.I) else 'Thiếu dòng địa danh, ngày tháng năm ở phần đầu'
def L06(t, d):
    ten = CO_TEN_LOAI.get(d['loai_van_ban'])
    if not ten: return None
    T = ten.replace(' ', '')
    for l in t[:3000].split('\n'):
        c = chu(l)
        if l.strip() and len(c) <= 40 and (c.startswith(T) or c.endswith(T)):
            chu_cai = [x for x in l if x.isalpha()]
            if sum(x.isupper() for x in chu_cai) >= 0.8 * len(chu_cai): return None
    return f'Thiếu dòng tên loại viết hoa ({d["loai_van_ban"]})'
def L07(t, d):
    if d['loai_van_ban'] != 'Công văn': return None
    return None if re.search(r'V\s*[/⁄]\s*[vVwW]|Về việc', t[:2500]) else 'Công văn thiếu trích yếu "V/v"'
def L08(t, d):
    if d['loai_van_ban'] != 'Công văn': return None
    return None if 'KINHGUI' in chu(t[:3500]) else 'Công văn thiếu "Kính gửi"'
def L09(t, d):
    if re.search(r'N[ơo]i\s*nh[ậa]n', t, re.I): return None
    return 'Thiếu "Nơi nhận"' if du_trang(d) else KXD
def L10(t, d):
    if re.search(r'L[ưu]u\s*:?\s*(VT|V[ăa]n th[ưu])', t, re.I): return None
    return 'Nơi nhận thiếu "Lưu: VT"' if du_trang(d) else KXD
def L11(t, d):
    if re.search(r'\b(TM|KT|TL|TUQ)\s*\.|TH[ỦU]\s*T[ƯU][ỚO]NG|CH[ỦU]\s*T[ỊI]CH|B[ỘO]\s*TR[ƯU][ỞO]NG|GI[ÁA]M\s*[ĐD][ỐO]C|CH[ỦU]\s*NHI[ỆE]M|TR[ƯU][ỞO]NG|T[ƯU]\s*L[ỆE]NH', t[len(t)//3:]): return None
    return 'Thiếu quyền hạn, chức vụ người ký' if du_trang(d) else KXD
def L12(t, d):
    if re.search(r'[/⁄]\s*\.(?!\w)', t): return None
    return 'Thiếu dấu kết thúc nội dung "./."' if du_trang(d) else KXD
LUAT = {'L01': (L01, 'Quốc hiệu', 'PL I Phần I mục II.1'), 'L02': (L02, 'Tiêu ngữ', 'PL I Phần I mục II.1.b'),
        'L03': (L03, 'Có dòng Số', 'PL I Phần I mục II.3.c'), 'L04': (L04, 'Cấu trúc ký hiệu', 'PL I Phần I mục II.3.b'),
        'L05': (L05, 'Địa danh, thời gian', 'PL I Phần I mục II.4.b'), 'L06': (L06, 'Tên loại', 'PL I Phần I mục II.5.b'),
        'L07': (L07, 'Trích yếu công văn', 'PL I Phần I mục II.5.b'), 'L08': (L08, 'Kính gửi', 'PL I Phần I mục II.9'),
        'L09': (L09, 'Nơi nhận', 'PL I Phần I mục II.9'), 'L10': (L10, 'Lưu VT', 'PL I Phần I mục II.9.d'),
        'L11': (L11, 'Quyền hạn, chức vụ người ký', 'PL I Phần I mục II.7.b'), 'L12': (L12, 'Kết thúc nội dung', 'CHƯA XÁC MINH: không tìm thấy trong Phụ lục I; có thể chỉ là mẫu trình bày')}
def kiem(d):
    t = nfc(d['text']); return {k: f(t, d) for k, (f, _, _) in LUAT.items()}
