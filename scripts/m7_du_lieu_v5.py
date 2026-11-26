"""M7 · Tập huấn luyện v5 (QĐ-15), dựng từ m6b/ (v4). Bộ kiểm tra giữ nguyên; T1 đánh giá theo giao thức 2.0 (có tư liệu tra cứu).
1. T1: lời yêu cầu kèm tư liệu tra cứu (scripts/tra_cuu.py). Khi dựng, bỏ chính văn bản đó khỏi láng giềng đồng viện dẫn,
   để danh sách giống điều kiện lúc kiểm tra. Viện dẫn quy phạm trung ương trong mục tiêu mà không có trong danh sách
   bị thay bằng "…" (dạy mô hình chỉ dẫn từ tư liệu).
2. Làm sạch nơi nhận và khối ký: chức danh kèm họ tên → chức danh kèm "[Họ và tên]"; bỏ rác OCR ("na 4", "Công TTĐT").
3. T2 300 và T3 300 lấy từ m6b, T4 200 (mốc thời gian), để giữ các nhiệm vụ khác không tụt.
Dùng: python3 scripts/m7_du_lieu_v5.py   → m7/train.jsonl, m7/valid.jsonl, m7/thong_ke.json (cần m7/dong_vien_dan.json)
"""
import json, re, os, sys, random, collections, copy
sys.path.insert(0, 'scripts'); import tra_cuu as tcu, kiem_trung_thuc as k
rng = random.Random(20261126); TC = tcu.TraCuu()
def nv(r):
    u = r['messages'][1]['content']
    return ('T1' if u.startswith('Soạn') else 'T2' if u.startswith('Văn bản dưới') else 'T3' if u.startswith('Đọc văn bản')
            else 'T4' if u.startswith('Văn bản hành chính ban hành') or u.startswith('Văn bản của Thủ tướng') else '?')

CHUC = r'(?:PCN|CN|BTCN|PTTg|TTg|TTgCP|Bộ trưởng|Thứ trưởng|Chủ nhiệm|Phó Chủ nhiệm|Chủ tịch|Phó Chủ tịch|PCT|CT|Giám đốc|Phó Giám đốc|Chánh Văn phòng|Phó Thủ tướng|Thủ tướng)'
TEN = r'[A-ZĐ][a-zà-ỹđ]+(?:[ \t\n]+[A-ZĐ][a-zà-ỹđ]+){1,3}'
def lam_sach(t, giu_ten=()):
    """giu_ten: họ tên có trong tư liệu tra cứu (Thủ tướng theo ngày) thì giữ; mọi họ tên khác sau chức danh bị che."""
    n = collections.Counter()
    def thay(m):
        if m.group(2) in ('Chính Phủ', 'Văn Phòng', 'Ủy Ban', 'Uỷ Ban') or m.group(2) in giu_ten: return m.group(0)
        n['ho_ten'] += 1; return m.group(1) + '[Họ và tên]'
    t = re.sub(r'(' + CHUC + r'(?:[ \t]+Chính phủ)?[ \t\n]+)(' + TEN + r')', thay, t)
    # Trong khối nơi nhận: mọi họ tên 3-4 âm tiết bắt đầu bằng họ phổ biến (danh sách PCN, Trợ lý...) cũng bị che
    HO = 'Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Võ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Mai|Đinh|Trương|Lưu|Tạ|Cao|Đào|Lương|Trịnh|Tô|Lại|Đoàn|Kiều|Chu|Quách|Nghiêm|Tống|Triệu|Đàm|Thân|Hà|Lâm|Châu|Vương|La'
    vt = t.find('Nơi nhận')
    if vt >= 0:
        def thay2(m):
            if m.group(0) in giu_ten or m.group(0).startswith('Hồ Chí Minh'): return m.group(0)
            n['ho_ten_noi_nhan'] += 1; return '[Họ và tên]'
        t = t[:vt] + re.sub(r'(?<![A-Za-zÀ-ỹđĐ])(?:' + HO + r')(?:[ \t\n]+[A-ZĐ][a-zà-ỹđ]+){2,3}(?![a-zà-ỹđ])', thay2, t[vt:])
    t, a = re.subn(r'\s+na \d\b', '', t); n['rac_na'] += a
    t = t.replace('Công TTĐT', 'Cổng TTĐT').replace('CHỈ THÍ', 'CHỈ THỊ')
    return t, n

RE_QP = re.compile(r'(?<![\d/…])(\d{1,4})/(\d{4})/(NĐ-CP|NQ-CP|QĐ-TTg|TT-[A-ZĐ]+|TTLT-[A-ZĐ-]+)')
NGAY = re.compile(r'(\s*(?:,\s*)?ngày\s*)(\S{1,2})(\s*tháng\s*)(\S{1,2})(\s*n\S{1,3}\s*)(\S{4})|(\s*(?:,\s*)?ngày\s*)(\d{1,2}/\d{1,2}/\d{4})', re.I)
def che_ngoai_danh_sach(t, cho_phep, kh_ban_than):
    out, i, n = [], 0, collections.Counter()
    for m in RE_QP.finditer(t):
        kh = k.chuan(m.group(0))
        if kh in cho_phep or m.group(0) == kh_ban_than: n['giu'] += 1; continue
        out.append(t[i:m.start()]); out.append(f'…/…/{m.group(3)}'); i = m.end(); n['che'] += 1
        d = NGAY.match(t, i)
        if d: out.append(f'{d.group(1)}… tháng … năm …' if d.group(1) is not None else f'{d.group(7)}…'); i = d.end()
    out.append(t[i:]); return ''.join(out), n

def main():
    O = 'm7'; os.makedirs(O, exist_ok=True); TK = {}
    for s, n2, n3, n4 in (('train', 300, 300, 200), ('valid', 30, 30, 20)):
        R = [json.loads(l) for l in open(f'm6b/{s}.jsonl', encoding='utf-8')]
        T1, dem = [], collections.Counter()
        for r in R:
            if nv(r) != 'T1': continue
            r = copy.deepcopy(r); de = r['messages'][1]['content']
            r['messages'][1]['content'] = tcu.lam_giau_de(de, TC, 8, bo_chinh_no=True)
            giu = set(re.findall(r'Thủ tướng Chính phủ: ([^.]+)\.', r['messages'][1]['content']))
            cho = {x[0] for x in tcu.lam_giau_de.ds}
            kh = re.search(r'Số, ký hiệu: (.*)', de).group(1)
            t, a = che_ngoai_danh_sach(r['messages'][2]['content'], cho, kh); t, b = lam_sach(t, giu)
            r['messages'][2]['content'] = t; dem.update(a); dem.update(b); T1.append(r)
        nhom = collections.defaultdict(list)
        for r in R: nhom[nv(r)].append(r)
        for x in nhom.values(): rng.shuffle(x)
        from transformers import AutoTokenizer
        TOK = AutoTokenizer.from_pretrained(os.environ.get('VBHC_TOKENIZER', '/home/claude/m4/qwen25_05b'))
        vua = lambda r: len(TOK(TOK.apply_chat_template(r['messages'], tokenize=False))['input_ids']) <= 3000
        n_truoc = len(T1); T1 = [r for r in T1 if vua(r)]; dem['bo_qua_3000_token'] = n_truoc - len(T1)
        rows = T1 + nhom['T2'][:n2] + nhom['T3'][:n3] + nhom['T4'][:n4]; rng.shuffle(rows)
        open(f'{O}/{s}.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
        TK[s] = {'tong': len(rows), 'T1': len(T1), 'T2': min(n2, len(nhom['T2'])), 'T3': min(n3, len(nhom['T3'])), 'T4': min(n4, len(nhom['T4'])), 'T1_xu_ly': dict(dem)}
    json.dump(TK, open(f'{O}/thong_ke.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(TK, ensure_ascii=False))

if __name__ == '__main__': main()
