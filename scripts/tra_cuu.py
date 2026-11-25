"""M7 · Bộ tra cứu cho giao thức 2.0 (QĐ-15): lời yêu cầu soạn văn bản kèm "tư liệu tra cứu".
Tư liệu gồm hai phần, đều suy được từ lời yêu cầu và dữ liệu công khai, không nhìn đáp án:
  1. Văn bản quy phạm trung ương ban hành trước ngày soạn, xếp theo độ gần với trích yếu (BM25 trên âm tiết, chỉ mục 24.874 văn bản).
  2. Bộ máy tại ngày ban hành: danh sách bộ, Thủ tướng, số cấp chính quyền địa phương, các tỉnh sau sáp nhập.
Dùng: python3 scripts/tra_cuu.py --do-phu     → đo độ phủ trên văn bản thật của bộ kiểm tra (không dùng để huấn luyện)
"""
import re, math, json, sys, collections, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kiem_trung_thuc as k

QP = re.compile(r'^(\d{1,4})/(\d{4})/(NĐ-CP|NQ-CP|QĐ-TTG|QH1[45]|UBTVQH1[45]|TT-[A-ZĐ]+|TTLT-[A-ZĐ-]+)$')
TEN_LOAI = {'NĐ-CP': ('Nghị định', 'Chính phủ'), 'NQ-CP': ('Nghị quyết', 'Chính phủ'), 'QĐ-TTG': ('Quyết định', 'Thủ tướng Chính phủ'),
            'QH14': ('Luật/Nghị quyết', 'Quốc hội'), 'QH15': ('Luật/Nghị quyết', 'Quốc hội'), 'UBTVQH14': ('Nghị quyết', 'Ủy ban Thường vụ Quốc hội'),
            'UBTVQH15': ('Nghị quyết', 'Ủy ban Thường vụ Quốc hội')}
DUNG = set('của và về việc các một những này đó cho tại với đối là được đã có theo trong từ đến năm ngày tháng vv'.split())   # chỉ hư từ: âm tiết như "hành", "chính" mang nghĩa
def am(s):
    w = [x for x in re.findall(r'\w+', s.lower()) if x not in DUNG and not x.isdigit() and len(x) > 1]
    return w + [a + '_' + b for a, b in zip(w, w[1:])]   # thêm cặp âm tiết liền nhau để thưởng cụm từ khớp

class TraCuu:
    """Hai nguồn ứng viên: (a) văn bản quy phạm mà các văn bản huấn luyện có trích yếu gần nhất đã viện dẫn (đồng viện dẫn,
    chỉ dùng tập huấn luyện, viện dẫn đã kiểm khớp chỉ mục); (b) văn bản quy phạm có trích yếu gần nhất. Mọi ứng viên phải ban hành trước ngày soạn."""
    def __init__(self, chi_muc='m3/chi_muc_kiem_trung_thuc.csv.xz', dong_vien_dan='m7/dong_vien_dan.json'):
        I = k.nap_chi_muc(chi_muc); self.vb = []
        for kh, ds in I.items():
            m = QP.match(kh)
            if not m: continue
            for ngay, ty in ds:
                if ngay and ty: self.vb.append((kh, ngay, ty, am(ty)))
        self.df = collections.Counter(w for v in self.vb for w in set(v[3])); self.N = len(self.vb)
        self.tb = sum(len(v[3]) for v in self.vb) / max(1, self.N)
        self.ngay = {}
        for kh, ngay, ty, w in self.vb: self.ngay.setdefault(kh, (ngay, ty))
        self.lang = []
        if os.path.exists(dong_vien_dan):
            for r in json.load(open(dong_vien_dan, encoding='utf-8')): self.lang.append((am(r['trich_yeu']), r['vien_dan']))
            self.df2 = collections.Counter(w for w, _ in self.lang for w in set(w)); self.tb2 = sum(len(w) for w, _ in self.lang) / max(1, len(self.lang))
    def _bm25(self, q, w, df, N, tb):
        tf = collections.Counter(w); s = 0.0
        for t in q:
            if t in tf:
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * 2.2 / (tf[t] + 1.2 * (0.25 + 0.75 * len(w) / tb))
        return s
    def tim(self, truy_van, truoc_ngay, k_=8, lang_gieng=30, bo_trich_yeu=None):
        q = set(am(truy_van)); diem = collections.Counter()
        if self.lang:   # (a) đồng viện dẫn từ các văn bản huấn luyện gần nhất
            bo = am(bo_trich_yeu) if bo_trich_yeu else None   # khi dựng dữ liệu huấn luyện: bỏ chính văn bản đó khỏi láng giềng
            gan = sorted(((self._bm25(q, w, self.df2, len(self.lang), self.tb2), vd) for w, vd in self.lang if w != bo), key=lambda x: -x[0])[:lang_gieng]
            for s, vd in gan:
                for kh in vd:
                    if kh in self.ngay and self.ngay[kh][0] < truoc_ngay: diem[kh] += s
        kq = [(kh, *self.ngay[kh]) for kh, _ in diem.most_common(k_)]
        if len(kq) >= k_: return kq
        seen = {x[0] for x in kq}
        for x in self._tim_tu_vung(q, truoc_ngay, k_ * 2):
            if x[0] not in seen: kq.append(x); seen.add(x[0])
            if len(kq) == k_: break
        return kq
    def _tim_tu_vung(self, q, truoc_ngay, k_):
        out = []
        for kh, ngay, ty, w in self.vb:
            if ngay >= truoc_ngay: continue
            s = self._bm25(q, w, self.df, self.N, self.tb)
            if s > 0: out.append((s, kh, ngay, ty))
        out.sort(key=lambda x: (-x[0], x[2]))
        seen, kq = set(), []
        for s, kh, ngay, ty in out:
            if kh in seen: continue
            seen.add(kh); kq.append((kh, ngay, ty))
            if len(kq) == k_: break
        return kq

BO_CU = ['Quốc phòng', 'Công an', 'Ngoại giao', 'Nội vụ', 'Tư pháp', 'Kế hoạch và Đầu tư', 'Tài chính', 'Công Thương', 'Nông nghiệp và Phát triển nông thôn',
         'Giao thông vận tải', 'Xây dựng', 'Tài nguyên và Môi trường', 'Thông tin và Truyền thông', 'Lao động - Thương binh và Xã hội',
         'Văn hóa, Thể thao và Du lịch', 'Khoa học và Công nghệ', 'Giáo dục và Đào tạo', 'Y tế']
NGANG_BO_CU = ['Ủy ban Dân tộc', 'Ngân hàng Nhà nước Việt Nam', 'Thanh tra Chính phủ', 'Văn phòng Chính phủ']
BO_MOI = ['Quốc phòng', 'Công an', 'Ngoại giao', 'Nội vụ', 'Tư pháp', 'Tài chính', 'Công Thương', 'Nông nghiệp và Môi trường', 'Xây dựng',
          'Văn hóa, Thể thao và Du lịch', 'Khoa học và Công nghệ', 'Giáo dục và Đào tạo', 'Y tế', 'Dân tộc và Tôn giáo']
NGANG_BO_MOI = ['Ngân hàng Nhà nước Việt Nam', 'Thanh tra Chính phủ', 'Văn phòng Chính phủ']
TINH_34 = ['Hà Nội', 'Huế', 'Lai Châu', 'Điện Biên', 'Sơn La', 'Lạng Sơn', 'Quảng Ninh', 'Thanh Hóa', 'Nghệ An', 'Hà Tĩnh', 'Cao Bằng', 'Tuyên Quang',
           'Lào Cai', 'Thái Nguyên', 'Phú Thọ', 'Bắc Ninh', 'Hưng Yên', 'Hải Phòng', 'Ninh Bình', 'Quảng Trị', 'Đà Nẵng', 'Quảng Ngãi', 'Gia Lai',
           'Khánh Hòa', 'Lâm Đồng', 'Đắk Lắk', 'Thành phố Hồ Chí Minh', 'Đồng Nai', 'Tây Ninh', 'Cần Thơ', 'Vĩnh Long', 'Đồng Tháp', 'Cà Mau', 'An Giang']

def bo_may(ngay):
    moi = ngay >= '2025-03-01'
    d = [f"- Các bộ: {', '.join(BO_MOI if moi else BO_CU)}.", f"- Cơ quan ngang bộ: {', '.join(NGANG_BO_MOI if moi else NGANG_BO_CU)}."]
    if ngay < '2026-01-01':
        d.append(f"- Thủ tướng Chính phủ: {'Nguyễn Xuân Phúc' if ngay < '2021-04-05' else 'Phạm Minh Chính'}.")
    d.append('- Chính quyền địa phương: ' + ('hai cấp (tỉnh và xã), không còn cấp huyện.' if ngay >= '2025-07-01' else 'ba cấp (tỉnh, huyện, xã).'))
    if ngay >= '2025-07-01':
        d.append(f"- 34 đơn vị hành chính cấp tỉnh: {', '.join(TINH_34)}.")
    return '\n'.join(d)

def dong_vb(kh, ngay, ty):
    so, nam, ky = QP.match(kh).groups()
    loai, cq = TEN_LOAI.get(ky, ('Thông tư', 'Bộ trưởng'))
    y, m, d = ngay.split('-')
    ty = ty.strip(); ty = ty if len(ty) <= 180 else ty[:177].rsplit(' ', 1)[0] + '…'   # trích yếu dài cắt gọn cho vừa khung
    return f'- {loai} số {kh.replace("QĐ-TTG", "QĐ-TTg")} ngày {int(d):02d}/{int(m):02d}/{y} của {cq}: {ty}'

RE_DE = re.compile(r'Ngày ban hành: ngày (\d{1,2}) tháng (\d{1,2}) năm (\d{4})\n- Trích yếu nội dung: (.*)\n')
def lam_giau_de(de, tc, k_=8, bo_chinh_no=False):
    """Thêm tư liệu tra cứu vào lời yêu cầu T1 (giao thức 2.0). Chỉ dùng ngày và trích yếu có trong lời yêu cầu."""
    m = RE_DE.search(de)
    if not m: return de
    ngay = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
    loai = re.search(r'loại "([^"]+)"', de).group(1)
    ds = tc.tim(m.group(4) + ' ' + loai, ngay, k_, bo_trich_yeu=m.group(4) if bo_chinh_no else None)
    lam_giau_de.ds = ds
    tl = ('\n\nTư liệu tra cứu (chỉ viện dẫn văn bản có trong danh sách này; văn bản khác thì để "…" cho số và ngày):\n'
          + ('\n'.join(dong_vb(*x) for x in ds) if ds else '- (không tìm được văn bản phù hợp)')
          + '\nBộ máy tại ngày ban hành:\n' + bo_may(ngay))
    return de.replace('\nViết đủ các thành phần', tl + '\nViết đủ các thành phần', 1)

def do_phu(k_=8):
    tc = TraCuu(); DE = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_de.jsonl', encoding='utf-8')}
    DA = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')}
    co, trung = 0, 0; I = k.nap_chi_muc()
    for i, d in DE.items():
        if d['nhiem_vu'] != 'T1': continue
        a = DA[i]['dap_an']; ref = a['van_ban_tham_chieu']
        can = {kh for kh, kq in k.kiem_trich_dan(ref, I, a['ngay_ban_hanh'], a['so_ky_hieu_chuan']) if kq == 'dung' and QP.match(kh)}
        m = RE_DE.search(d['de']); ngay = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
        lay = {x[0] for x in tc.tim(m.group(4), ngay, k_)}
        co += len(can); trung += len(can & lay)
    return {'k': k_, 'vien_dan_qp_trong_van_ban_that': co, 'tra_duoc': trung, 'do_phu_pct': round(100 * trung / max(1, co), 1)}

def dung_dong_vien_dan(toan_van='data/stage4_v4/corpus.jsonl', ra='m7/dong_vien_dan.json'):
    """Từ tập huấn luyện (chia_tap = train): mỗi văn bản → trích yếu + các viện dẫn quy phạm trung ương đã kiểm khớp chỉ mục."""
    I = k.nap_chi_muc(); SP = json.load(open('m3/chia_tap.json', encoding='utf-8'))['chia_tap']; out = []
    for l in open(os.environ.get('VBHC_TOAN_VAN', toan_van), encoding='utf-8'):
        c = json.loads(l)
        if SP.get(c['docid']) != 'train' or not c.get('ngay_ban_hanh'): continue
        vd = sorted({kh for kh, kq in k.kiem_trich_dan(c['text'], I, c['ngay_ban_hanh'], c['so_ky_hieu_chuan']) if kq == 'dung' and QP.match(kh)})
        if vd: out.append({'docid': c['docid'], 'trich_yeu': c['trich_yeu'], 'vien_dan': vd})
    os.makedirs(os.path.dirname(ra), exist_ok=True); json.dump(out, open(ra, 'w', encoding='utf-8'), ensure_ascii=False)
    return len(out)

if __name__ == '__main__':
    if '--dung' in sys.argv: print('văn bản huấn luyện có viện dẫn:', dung_dong_vien_dan())
    if '--do-phu' in sys.argv:
        for kk in (5, 8, 12): print(json.dumps(do_phu(kk), ensure_ascii=False))
