"""Kiểm tay mô phỏng (chuyên gia mô phỏng, AI) 100 mẫu thông tin cá nhân của một đợt cào.
Bước 1 (máy): với mỗi mẫu trong phiếu, quét bản đã che trong kho, rút mọi đoạn có thể là thông tin người dân:
  họ tên dạng 2–4 âm tiết viết hoa không đi cùng chức vụ, ngày sinh, năm sinh, số định danh, số điện thoại, địa chỉ thường trú, biển số xe.
Bước 2 (chuyên gia mô phỏng đọc từng đoạn): ghi phán quyết vào tệp phán quyết; tệp kết quả gộp lại thành phiếu đã điền.
Dùng: python3 scripts/m8_kiem_tay_mo_phong.py rut <b|c>    → ket_qua/dot_cao/ung_vien_kiem_tay_<đợt>.jsonl
      python3 scripts/m8_kiem_tay_mo_phong.py dien <b|c>   → ket_qua/dot_cao/mau_kiem_tay_dot_<đợt>_da_dien.md
"""
import json, re, sys
KHO = {'b': 'data/stage4_v6/corpus.jsonl', 'c': 'data/stage4_v7/corpus.jsonl'}
HOA = r'[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ]'
THUONG = r'[a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]'
HO = 'Nguyễn Trần Lê Phạm Hoàng Huỳnh Phan Vũ Võ Đặng Bùi Đỗ Hồ Ngô Dương Lý Đinh Trịnh Lương Đào Cao Hà Lò Lù Tòng Vàng Giàng Sùng Mùa Hầu Thào Lầu Tẩn Chảo Tráng Quàng Điêu Lường Cầm Mai Tô Tạ Chu Đoàn Lâm Thái Kiều Triệu Nông Hứa Lục Mạc Văn'.split()
MAU = {
 'ho_ten': re.compile(r'\b(?:%s)(?:\s%s%s+){1,3}\b' % ('|'.join(HO), HOA, THUONG)),
 'ngay_sinh': re.compile(r'(sinh ngày|ngày sinh|năm sinh|sinh năm)[^\n]{0,40}', re.I),
 'dinh_danh': re.compile(r'(CCCD|CMND|căn cước|định danh cá nhân|hộ chiếu)[^\n]{0,40}', re.I),
 'dien_thoai': re.compile(r'(?<![\d.,/])0\d{2,3}[ .]?\d{3}[ .]?\d{3,4}(?![\d.,/])'),
 'thuong_tru': re.compile(r'(thường trú|trú tại|tạm trú|quê quán|nơi ở)[^\n]{0,50}', re.I),
 'bien_so': re.compile(r'\b\d{2}[A-Z]{1,2}[- ]?\d{3}\.?\d{2}\b'),
}
def rut(d):
    phieu = open(f'ket_qua/dot_cao/mau_kiem_tay_dot_{d}.md', encoding='utf-8').read()
    ma = re.findall(r'^\| \d+ \| ([^ |]+) \|', phieu, re.M)
    can = set(ma); kho = {}
    for l in open(KHO[d], encoding='utf-8'):
        c = json.loads(l)
        if c['docid'] in can: kho[c['docid']] = c
    out = open(f'ket_qua/dot_cao/ung_vien_kiem_tay_{d}.jsonl', 'w', encoding='utf-8')
    for i, m in enumerate(ma, 1):
        t = kho[m]['text']; uv = []
        for k, p in MAU.items():
            for x in p.finditer(t):
                uv.append({'kieu': k, 'doan': x.group(0), 'ngu_canh': t[max(0, x.start() - 70):x.end() + 40].replace('\n', ' ')})
        out.write(json.dumps({'stt': i, 'docid': m, 'loai': kho[m]['loai_van_ban'], 'trich_yeu': kho[m]['trich_yeu'][:90], 'ung_vien': uv}, ensure_ascii=False) + '\n')
    print(d, len(ma), 'mẫu')
if __name__ == '__main__':
    if sys.argv[1] == 'rut': rut(sys.argv[2])
