"""M8 · Che họ tên trong mục tiêu huấn luyện, bản sửa lỗi của m7_du_lieu_v5.lam_sach (giữ bản cũ để tái lập v5, v6).
Lỗi bản cũ: "TTg", "CT", "CN" trong ký hiệu văn bản ("…/CĐ-TTg Hà Nội") bị coi là chức danh, nên "Hà Nội" bị che;
"Bộ trưởng Bộ Tài nguyên…" bị che mất "Bộ Tài". Bản này:
  - chức danh viết tắt chỉ tính khi không dính vào ký hiệu (không đứng sau "-" hoặc "/");
  - chuỗi viết hoa sau chức danh không được là địa danh, tên tỉnh, tên cơ quan (đọc từ sổ SOT và danh sách cấm);
  - tên có trong tư liệu (Thủ tướng, Phó Thủ tướng theo ngày) thì giữ.
Dùng: python3 scripts/m8_lam_sach.py   → chạy phép thử (thoát mã 2 nếu sai)
"""
import re, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sot_bo_may as SOT
CHUC_DAI = r'(?:Bộ trưởng|Thứ trưởng|Chủ nhiệm|Phó Chủ nhiệm|Chủ tịch|Phó Chủ tịch|Giám đốc|Phó Giám đốc|Chánh Văn phòng|Phó Chánh Văn phòng|Phó Thủ tướng|Thủ tướng|Bí thư|Phó Bí thư|Trưởng ban|Phó Trưởng ban|Tổng cục trưởng|Cục trưởng|Vụ trưởng)'
CHUC_TAT = r'(?:PCN|BTCN|PTTgTT|PTTg|TTgCP|PCT|CT|CN|TTg)'
# chức danh viết dài: cho phép xuống dòng giữa các từ và lỗi OCR hay gặp (Thú/Thủ, phú/phủ)
def _mem(cum):
    tu = cum.replace('Thủ', 'Th[ủúùuũ]').replace('tướng', 't[ưu][ớơo]ng').split(' ')
    return r'\s+'.join(tu)
CHUC_DAI = '(?:' + '|'.join(_mem(x) for x in sorted(CHUC_DAI[3:-1].split('|'), key=len, reverse=True)) + ')'
DUOI = r'(?:\s+Th[ưu][ờơo]ng\s+tr[ựưu]c)?(?:\s+Ch[íi]nh\s+ph[ủúùu])?'
HO = 'Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Võ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Mai|Đinh|Trương|Lưu|Tạ|Cao|Đào|Lương|Trịnh|Tô|Lại|Đoàn|Kiều|Chu|Quách|Nghiêm|Tống|Triệu|Đàm|Thân|Hà|Lâm|Châu|Vương|La|Khổng|Thái|Văn|Doãn|Mạc|Ninh|Phùng|Giang|Từ|Âu|Kim|Tăng|Lục|Tiêu|Diệp|Quan|Hứa|Bế|Nông|Lò|Hầu|Mã'
HOA = 'A-Z' + ''.join(c for c in map(chr, range(0xC0, 0x1EFA)) if c.isupper() and c.isalpha())   # chữ hoa tiếng Việt, không lẫn chữ thường có dấu
AM = rf'[{HOA}][a-zà-ỹđ]+'
TEN = rf'(?:{HO})(?:[ \t\n]+{AM}){{1,3}}'
CAM_DAU = ('Bộ ', 'Chính Phủ', 'Chính phủ', 'Văn Phòng', 'Văn phòng', 'Ủy Ban', 'Uỷ Ban', 'Ủy ban', 'Hội Đồng', 'Quốc Hội', 'Nhà Nước', 'Hồ Chí Minh', 'Thành Phố', 'Thành phố')
DIA = set(SOT.tinh_34('2025-07-01')) | {r['ten'] for r in SOT.so()['ban_ghi'] if r['loai'] == 'tinh_cu'} | {'Hà Nội', 'Thủ Dầu Một', 'Long Thành', 'Trung Bộ', 'Nam Bộ', 'Bắc Bộ', 'Tây Nguyên', 'Đồng Bằng', 'Lâm Đồng', 'Hà Tĩnh', 'Hà Giang', 'Hà Nam', 'Cao Bằng', 'Lào Cai', 'Ninh Bình', 'Ninh Thuận', 'Thái Nguyên', 'Thái Bình', 'Mai Châu', 'Hồ Gươm', 'Châu Đốc', 'Kim Bôi', 'Lục Ngạn'}

def la_dia_danh(chuoi):
    c = re.sub(r'\s+', ' ', chuoi).strip()
    return c.startswith(CAM_DAU) or any(c == d or c.startswith(d + ' ') or d.startswith(c) for d in DIA)

BAN = 'm8.1'   # 'm8.4': sửa lỗi giữ địa danh đuôi khi phần trước chỉ còn họ ("Nguyễn Hòa Bình" → "[Họ và tên] Hòa Bình"); bản cũ giữ để tái lập M8.1, M8.2

def che(t, giu_ten=()):
    """Thay họ tên đi sau chức danh, và họ tên trong khối nơi nhận, bằng "[Họ và tên]". Trả (văn bản, bộ đếm)."""
    n = collections.Counter()
    def thay(m):
        ten = re.sub(r'\s+', ' ', m.group('ten'))
        if ten in giu_ten or la_dia_danh(ten): n['giu'] += 1; return m.group(0)
        duoi = next((d for d in DIA if ten.endswith(' ' + d)), None)   # "Tô Lâm Hà Nội": giữ phần địa danh dính phía sau
        if duoi and BAN != 'm8.1' and len(ten[:-len(duoi)].split()) < 2: duoi = None   # chỉ còn họ phía trước: cả cụm là họ tên
        n['che'] += 1; return m.group('dau') + '[Họ và tên]' + (' ' + duoi if duoi else '')
    t = re.sub(rf'(?P<dau>(?<![\w])(?:{CHUC_DAI}{DUOI}|(?<![-/]){CHUC_TAT})[ \t\n:]+)(?P<ten>{TEN})(?![a-zà-ỹđ])', thay, t)
    vt = t.find('Nơi nhận')
    if vt >= 0:
        def thay2(m):
            ten = re.sub(r'\s+', ' ', m.group(0))
            if ten in giu_ten or la_dia_danh(ten): return m.group(0)
            n['che_noi_nhan'] += 1; return '[Họ và tên]'
        t = t[:vt] + re.sub(rf'(?<![\w\[])(?:{HO})(?:[ \t\n]+{AM}){{2,3}}(?![a-zà-ỹđ])', thay2, t[vt:])
    t, a = re.subn(r'\s+na \d\b', '', t); n['rac_na'] += a
    return t.replace('Công TTĐT', 'Cổng TTĐT').replace('CHỈ THÍ', 'CHỈ THỊ'), n

THU = [  # (đầu vào, phải chứa, không được chứa)
    ('Số: 39/CĐ-TTg Hà Nội, ngày 17 tháng 4 năm 2025', 'Hà Nội, ngày', '[Họ và tên]'),
    ('Căn cứ Thông tư số 02/2022/TT-BTNMT của Bộ trưởng Bộ Tài nguyên và Môi trường', 'Bộ Tài nguyên và Môi trường', '[Họ và tên]'),
    ('Phó Thủ tướng Chính phủ Trần Hồng Hà có ý kiến như sau', 'Phó Thủ tướng Chính phủ [Họ và tên] có ý kiến', 'Trần Hồng Hà'),
    ('Giám đốc Sở Tài chính tỉnh Thái Nguyên', 'Sở Tài chính tỉnh Thái Nguyên', '[Họ và tên]'),
    ('Chủ tịch UBND tỉnh Lâm Đồng', 'tỉnh Lâm Đồng', '[Họ và tên]'),
    ('Chủ tịch Hồ Chí Minh', 'Hồ Chí Minh', '[Họ và tên]'),
    ('Nơi nhận:\n- VPCP: BTCN, các PCN: Cao Huy,\nNguyễn Sỹ Hiệp, Đỗ Ngọc Huỳnh', '[Họ và tên]', 'Nguyễn Sỹ Hiệp'),
    ('Thủ tướng Chính phủ Phạm Minh Chính chủ trì', 'Phạm Minh Chính', '[Họ và tên]'),   # giữ khi có trong tư liệu
    ('Số: 228/CĐ-TTg Hà Nội, ngày 25 tháng 11 năm 2025', 'Hà Nội', '[Họ và tên]'),
    ('Thủ tướng Chính phủ Trần Lưu Quang đã chỉ đạo', '[Họ và tên] đã chỉ đạo', 'Trần Lưu Quang'),
    ('Tổng Bí thư Tô Lâm Hà Nội', '[Họ và tên] Hà Nội', 'Tô Lâm'),
    ('ý kiến của Phó Thủ tướng\nChính phủ Trần Hồng Hà như sau', '[Họ và tên] như sau', 'Trần Hồng Hà'),
    ('Phó Thủ tướng Thường trực Chính phủ Phạm Gia Túc chỉ đạo', '[Họ và tên] chỉ đạo', 'Phạm Gia Túc'),
    ('kết luận của Phó Thú tướng Vũ Đức Đam', '[Họ và tên]', 'Vũ Đức Đam'),
    ('- Thủ tướng, PTTgTT Phạm Gia Túc;', '[Họ và tên]', 'Phạm Gia Túc'),
    ('KT. BỘ TRƯỞNG, CHỦ NHIỆM\nPHÓ CHỦ NHIỆM\n\nNguyễn Sỹ Hiệp', 'Nguyễn Sỹ Hiệp', 'xxx'),   # khối ký viết hoa: không thuộc phạm vi hàm này
]
if __name__ == '__main__':
    sai = 0
    for vao, co, khong in THU:
        ra, _ = che(vao, giu_ten={'Phạm Minh Chính'})
        ok = co in ra and khong not in ra
        sai += not ok; print('ĐẠT ' if ok else 'SAI ', repr(vao[:60]), '→', repr(ra[:80]))
    THU_84 = [('Phó Thủ tướng Thường trực Chính phủ Nguyễn Hòa Bình.', '[Họ và tên].', 'Hòa Bình'), ('Tổng Bí thư Tô Lâm Hà Nội', '[Họ và tên] Hà Nội', 'Tô Lâm'),
              ('Chủ tịch UBND tỉnh Hòa Bình', 'tỉnh Hòa Bình', '[Họ và tên]')]
    BAN = 'm8.4'
    for vao, co, khong in THU_84:   # bản M8.4
        ra, _ = che(vao); ok = co in ra and khong not in ra
        sai += not ok; print('ĐẠT ' if ok else 'SAI ', '[m8.4]', repr(vao[:60]), '→', repr(ra[:80]))
    if sai: sys.exit(2)
    print('ĐẠT cả', len(THU) + len(THU_84), 'phép thử')
