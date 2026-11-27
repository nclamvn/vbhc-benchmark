"""Kiểm trung thực bài soạn T1 bằng máy (bộ chấm 1.2, phần bổ sung; không đổi tong_hop của bộ chấm 1.1).

Bốn nhóm lỗi, mỗi nhóm chỉ bắt khi kiểm được, còn lại để trống (không đoán):
  trich_dan   số ký hiệu văn bản trung ương 2020–2026 được viện dẫn: không có trong chỉ mục, sai ngày,
              ban hành sau ngày của văn bản đang soạn, hoặc mô tả không khớp trích yếu thật.
  vai         người ký không khớp cơ quan ban hành (Chủ tịch nước ký văn bản của Thủ tướng/Chính phủ/VPCP),
              Thủ tướng nêu tên ngoài nhiệm kỳ (nhiệm kỳ đọc từ sổ SOT sot/bo_may.json).
  thoi_diem   gọi tên bộ đã hợp nhất (từ 01/3/2025) hoặc cấp huyện (từ 01/7/2025) trong văn bản ban hành sau mốc.
  lap         một chuỗi 8 âm tiết lặp chiếm từ 20% bài trở lên.

Dùng: python3 scripts/kiem_trung_thuc.py <chỉ mục .csv> <đáp án .jsonl> <tệp trả lời .jsonl>... [--tham-chieu]
--tham-chieu chạy trên chính văn bản thật làm bài, để đo tỷ lệ báo nhầm của bộ kiểm.
"""
import csv, json, re, sys, os, collections

def chuan(k):
    k = re.sub(r'^0+(?=\d)', '', k.strip())
    k = k.upper().replace('ND-', 'NĐ-').replace('QD-', 'QĐ-').replace('Đ', 'Đ')
    return re.sub(r'\s+', '', k)

def nap_chi_muc(p='m3/chi_muc_kiem_trung_thuc.csv.xz'):
    import lzma
    I = collections.defaultdict(list)
    f = lzma.open(p, 'rt', encoding='utf-8-sig') if p.endswith('.xz') else open(p, encoding='utf-8-sig')
    for r in csv.DictReader(f):
        I[chuan(r['so_ky_hieu_chuan'])].append((r['ngay_ban_hanh'], r['trich_yeu']))
    return I

TW = re.compile(r'^(NĐ-CP|NQ-CP|QĐ-TTG|CT-TTG|CĐ-TTG|TB-VPCP|VPCP-[A-ZĐ]+|TTG-[A-ZĐ]+|QH1[45]|UBTVQH1[45]|TT-B[A-ZĐ]+|TT-NHNN|TT-VPCP)$')
RE_KH = re.compile(r'(?<![\d/])(\d{1,5})/(?:(\d{4})/)?([A-ZĐ]{1,8}\d{0,2}(?:-[A-ZĐa-zđ0-9]{1,12}){0,3})')
RE_NGAY = re.compile(r'^\W{0,6}(?:ngày\s*)?(\d{1,2})\s*(?:tháng|/|-)\s*(\d{1,2})\s*(?:năm|/|-)\s*(\d{4})', re.I)
DUNG = set('của và về việc các một số điều quy định chi tiết thi hành ban hành theo trong cho tại với đối là được những này đã có năm ngày tháng chính phủ thủ tướng nghị định nghị quyết thông tư quyết định luật'.split())

def am_tiet(s):
    return [w for w in re.findall(r'\w+', s.lower()) if w not in DUNG and not w.isdigit()]

def kiem_trich_dan(bai, I, ngay_vb, kh_ban_than):
    out = []
    for m in RE_KH.finditer(bai):
        so, nam, ky = m.group(1), m.group(2), m.group(3).upper()
        if not TW.match(ky) and not (ky.startswith('TT-') and nam):
            continue
        kh = chuan(f'{so}/{nam}/{ky}' if nam else f'{so}/{ky}')
        if kh == chuan(kh_ban_than):
            continue
        sau = bai[m.end():m.end() + 260]
        d = RE_NGAY.match(sau)
        ngay = f'{int(d.group(3)):04d}-{int(d.group(2)):02d}-{int(d.group(1)):02d}' if d else None
        nam_xet = int(nam) if nam else (int(ngay[:4]) if ngay else None)
        if nam_xet is None or not 2020 <= nam_xet <= 2026:
            out.append((kh, 'khong_kiem_duoc')); continue
        if re.match(r'^(UBTV)?QH1[45]$', ky):   # luật, nghị quyết Quốc hội: chỉ mục thiếu một số luật, và văn bản hay dẫn ngày thông qua thay vì ngày ký công bố
            out.append((kh, 'khong_kiem_duoc')); continue
        ung = [x for x in I.get(kh, []) if x[0][:4] == str(nam_xet)] if not nam else I.get(kh, [])
        if not ung:  # chỉ mục chỉ đủ với nghị định và luật; loại khác vắng mặt không chứng minh là bịa
            out.append((kh, 'khong_co' if re.match(r'^NĐ-CP$', ky) else 'khong_kiem_duoc')); continue
        if ngay and not any(x[0] == ngay for x in ung):
            out.append((kh, 'sai_ngay')); continue
        that = [x for x in ung if not ngay or x[0] == ngay]
        if ngay_vb and min(x[0] for x in that) > ngay_vb:
            out.append((kh, 'sau_ngay_van_ban')); continue
        mo_ta = re.split(r'[;\n]|,\s*(?:Căn|Xét|Theo)', sau[d.end() if d else 0:])[0]
        mt = set(am_tiet(re.sub(r'^.*?(?:Chính phủ|Thủ tướng[^,]*?|Quốc hội|Bộ [^,]*?)\s', '', mo_ta, count=1)))
        if len(mt) >= 5:
            ty = max((set(am_tiet(x[1])) for x in that), key=lambda s: len(s & mt))
            if ty and len(mt & ty) / len(ty) < 0.25:
                out.append((kh, 'sai_noi_dung')); continue
        out.append((kh, 'dung'))
    return out

# Tên bộ, tỉnh, Thủ tướng theo thời điểm đọc từ sổ SOT (sot/bo_may.json, scripts/sot_bo_may.py), không viết cứng ở đây.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sot_bo_may as SOT

def kiem_khac(bai, co_quan, ngay_vb):
    v, t = [], []
    tw = any(x in co_quan for x in ('TTg', 'VPCP', 'NĐ-CP', 'NQ-CP'))
    if tw and re.search(r'(?<!Văn phòng )(?<!VP )Chủ tịch nước|^\s*\**\s*CHỦ TỊCH\b', bai, re.M):
        v.append('chu_tich_nuoc_ky_thay')
    if ngay_vb:
        for ten, tu, den in SOT.nhiem_ky_thu_tuong():
            ngoai = (tu and ngay_vb < tu) or (den and ngay_vb > den)
            if ngoai and re.search(r'Thủ tướng(?: Chính phủ)?\s+' + re.escape(ten), bai):
                v.append('thu_tuong_sai_nhiem_ky'); break
    if ngay_vb and SOT.ten_bo_da_doi(ngay_vb):
        cd = [m.end() for m in RE_KH.finditer(bai)]
        for b in SOT.ten_bo_da_doi(ngay_vb):
            for m in re.finditer(re.escape(b), bai, re.I):
                if re.match(r'\s*\(nay', bai[m.end():m.end() + 12]) or any(0 <= m.start() - e <= 160 for e in cd):
                    continue  # nhắc tên cũ khi dẫn văn bản cũ hoặc có chú "nay là" là đúng
                t.append('bo_cu:' + b); break
            if t: break
    if ngay_vb and ngay_vb >= '2025-07-01' and re.search(r'(UBND|Ủy ban nhân dân|Uỷ ban nhân dân)\s+(các\s+)?huyện', bai):
        t.append('cap_huyen')
    if ngay_vb and ngay_vb >= '2025-07-01':
        cd = [m.end() for m in RE_KH.finditer(bai)]
        for ten in [x for x in SOT.tinh_cu(ngay_vb) if x != 'Thừa Thiên Huế']:
            # chỉ tính khi tên đứng sau chữ "tỉnh" trong cùng vế câu (tên cũ còn sống làm tên phường, xã, công ty)
            m = next((m for m in re.finditer(r'(?<!\w)' + re.escape(ten) + r'(?!\w)', bai)
                      if re.search(r'(?i)\btỉnh\b(?:(?!\b(?:xã|phường|thị trấn|công ty|huyện)\b)[^.;])*$', bai[max(0, m.start() - 200):m.start()])
                      and not re.match(r'\s*\(?\s*(cũ|trước đây)', bai[m.end():m.end() + 14]) and not any(0 <= m.start() - e <= 160 for e in cd)), None)
            if m: t.append('tinh_cu:' + ten); break
    if ngay_vb and 'Thừa Thiên Huế' in SOT.tinh_cu(ngay_vb) and re.search(r'Thừa Thiên\s*[-–]?\s*Huế', bai):
        t.append('tinh_cu:Thừa Thiên Huế')
    return v, t

def lap(bai):
    """Lặp ngắn (một chuỗi 8 âm tiết chiếm từ 20% bài) hoặc lặp nguyên khối (từ 26/11: một đoạn từ 60 ký tự xuất hiện lại,
    sau khi bỏ số thứ tự đầu đoạn; giao thức phạt lặp 1.2 không chặn được kiểu này)."""
    w = re.findall(r'\w+', bai.lower())
    if len(w) < 40: return False
    g = collections.Counter(tuple(w[i:i + 8]) for i in range(len(w) - 7))
    if g.most_common(1)[0][1] * 8 / len(w) >= 0.2: return True
    doan = [re.sub(r'\s+', ' ', re.sub(r'^\s*(\d+|[a-zđ])[.)]\s*', '', x.strip().lower())) for x in re.split(r'\n\s*\n', bai)]
    c = collections.Counter(x for x in doan if len(x) >= 60)
    return bool(c) and c.most_common(1)[0][1] >= 2

def cham(I, DA, TL, tham_chieu=False):
    hang = []
    for i, d in DA.items():
        if d['nhiem_vu'] != 'T1': continue
        a = d['dap_an']; bai = a['van_ban_tham_chieu'] if tham_chieu else TL.get(i, '')
        cq = a['so_ky_hieu_chuan'].split('/')[-1]
        td = kiem_trich_dan(bai, I, a['ngay_ban_hanh'], a['so_ky_hieu_chuan'])
        v, t = kiem_khac(bai, cq, a['ngay_ban_hanh'])
        hang.append({'id': i, 'trich_dan': td, 'vai': v, 'thoi_diem': t, 'lap': lap(bai)})
    n = len(hang)
    kd = [x for h in hang for x in h['trich_dan'] if x[1] != 'khong_kiem_duoc']
    loai = collections.Counter(x[1] for h in hang for x in h['trich_dan'])
    def loi(h): return sum(x[1] not in ('dung', 'khong_kiem_duoc') for x in h['trich_dan']) + len(h['vai']) + len(h['thoi_diem']) + h['lap']
    return {'n': n,
            'bai_sach_pct': round(100 * sum(loi(h) == 0 for h in hang) / n, 1),
            'trich_dan_kiem_duoc': len(kd),
            'trich_dan_dung_pct': round(100 * sum(x[1] == 'dung' for x in kd) / len(kd), 1) if kd else None,
            'trich_dan_sai_moi_bai': round(sum(x[1] != 'dung' for x in kd) / n, 2),
            'loai_trich_dan': dict(loai),
            'bai_sai_vai_pct': round(100 * sum(bool(h['vai']) for h in hang) / n, 1),
            'bai_sai_thoi_diem_pct': round(100 * sum(bool(h['thoi_diem']) for h in hang) / n, 1),
            'bai_lap_pct': round(100 * sum(h['lap'] for h in hang) / n, 1)}, hang

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    I = nap_chi_muc(a[0])
    DA = {json.loads(l)['id']: json.loads(l) for l in open(a[1], encoding='utf-8')}
    if '--tham-chieu' in sys.argv:
        tong, _ = cham(I, DA, {}, True); print(json.dumps({'tham_chieu': tong}, ensure_ascii=False))
    for p in a[2:]:
        TL = {}
        for l in open(p, encoding='utf-8'):
            r = json.loads(l); TL[r['id']] = r.get('tra_loi', '')
        tong, hang = cham(I, DA, TL)
        print(json.dumps({p.split('/')[-1]: tong}, ensure_ascii=False))
