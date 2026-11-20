"""Kiểm thông tin cá nhân trên 100 văn bản ngẫu nhiên của corpus đã làm sạch. In mọi đoạn đáng ngờ để người đọc xem."""
import json, re, random, sys
C = [json.loads(l) for l in open(sys.argv[1], encoding='utf-8')]
rng = random.Random(100); S = rng.sample(C, min(100, len(C)))
NAMEW = r'[A-ZĐÂĂÊÔƠƯÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ][a-zà-ỹđ]+'
checks = {
 'email': re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
 'so_dai_9_12': re.compile(r'(?<![\d./,])\d{9,12}(?![\d./,])'),
 'sdt_dang_0xxx': re.compile(r'(?<![\d.,])0\d{2,3}[\s.]\d{3}[\s.]\d{3,4}(?![\d.,])'),
 'ong_ba_ten_con_sot': re.compile(r'\b(ông|bà|Ông|Bà|anh|chị)\s+' + NAMEW + r'(\s' + NAMEW + r'){1,3}'),
 'dia_chi_con_sot': re.compile(r'(địa chỉ|trú tại|thường trú)\s*:?\s*(?!\[ĐỊA CHỈ\])[^\n]{0,40}\d'),
 'cccd_cmnd': re.compile(r'(CCCD|CMND|căn cước)[^\n]{0,20}\d{6,}'),
}
tot = {k: 0 for k in checks}; ex = {k: [] for k in checks}
for c in S:
    for k, p in checks.items():
        for m in p.finditer(c['text']):
            tot[k] += 1
            if len(ex[k]) < 6: ex[k].append((c['docid'], c['text'][max(0, m.start() - 50):m.end() + 30].replace('\n', ' ')))
print('docs', len(S), 'hits', tot)
for k in ex:
    for d, s in ex[k]: print(f'[{k}] {d}: {s}')
print('che da ap tren mau:', {k: sum(c['da_che'].get(k, 0) for c in S) for k in ['email', 'so_dien_thoai', 'ho_ten', 'dia_chi', 'so_dinh_danh', 'ngay_sinh']})
