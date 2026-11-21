"""Lượt kiểm thông tin cá nhân trên 100 mẫu v4 (seed 100): gom mọi đoạn đáng ngờ theo lưới rộng hơn bộ che,
để người kiểm (hoặc chuyên gia mô phỏng) đọc và phân loại từng đoạn."""
import json, re, random, sys
C = [json.loads(l) for l in open('data/stage4_v4/corpus.jsonl', encoding='utf-8')]
S = random.Random(100).sample(C, 100)
W = r'[A-ZĐÂĂÊÔƠƯÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ][a-zà-ỹđ]+'
HO = r'(?:Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Võ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Đinh|Đoàn|Trịnh|Lương|Mai|Đào|Hà|Tạ|Chu|Cao|Lưu|Triệu|Vương|Tô|Lâm|Thái|Quách|Nông|Lò|Ma)'
ROLE = re.compile(r'Thủ tướng|Phó|Bộ trưởng|Thứ trưởng|Chủ tịch|Chủ nhiệm|Giám đốc|Trưởng|Tổng|Bí thư|Ủy viên|Uỷ viên|đồng chí|Đồng chí|KT\.|TM\.|TL\.|TUQ|Nơi nhận|Thư ký|Trợ lý|Chánh|Cục trưởng|Vụ trưởng|Đại tướng|Thượng tướng|Trung tướng|Thiếu tướng|Đại tá|Tổng Bí thư|Chủ tịch nước|Người ký|ký:|Hiệu trưởng|Viện trưởng|Tư lệnh|Chính ủy|Kiểm sát|Chánh án|Thống đốc|Tổng Kiểm toán|Tổng Thanh tra|Giáo sư|GS\.|PGS|TS\.|Tiến sĩ|Anh hùng|Nhà giáo|Nghệ sĩ|Thầy thuốc')
P = {
 'ten_khong_vai': re.compile(HO + r'(?:\s' + W + r'){1,3}'),
 'so_dai': re.compile(r'(?<![\d./,\-])\d{9,12}(?![\d./,\-])'),
 'sdt': re.compile(r'(?<![\d.,])0\d{2,3}[\s.\-]\d{3}[\s.\-]\d{3,4}(?![\d.,])'),
 'email': re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
 'tai_khoan_bien_so': re.compile(r'(tài khoản|Tài khoản|biển số|biển kiểm soát|BKS|mã số thuế)[^\n]{0,30}\d{4,}'),
 'noi_o': re.compile(r'(?<!\w)(thôn|xóm|tổ dân phố|số nhà|ngõ|hẻm|ấp)\s+[^\n,;]{2,25},\s*(xã|phường|thị trấn)'),
 'sinh': re.compile(r'(sinh năm|sinh ngày|Sinh năm|Sinh ngày)\s*:?\s*(?!\[)[^\n]{0,15}'),
}
out = []
for c in S:
    t = c['text']
    for k, p in P.items():
        for m in p.finditer(t):
            ctx = t[max(0, m.start() - 110):m.end() + 60]
            if k == 'ten_khong_vai' and ROLE.search(ctx): continue
            out.append({'docid': c['docid'], 'so': c['so_ky_hieu'], 'loai': c['loai_van_ban'], 'kieu': k, 'khop': m.group(0), 'ngu_canh': ctx.replace('\n', ' ⏎ ')})
json.dump({'mau': [c['docid'] for c in S], 'ung_vien': out}, open('data/pii_review_v4_ung_vien.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
print(len(S), 'mau;', len(out), 'ung vien', Counter(o['kieu'] for o in out), 'so van ban co ung vien', len({o['docid'] for o in out}))
print(Counter(c['nguon'] for c in S), Counter(c['loai_van_ban'] for c in S))
