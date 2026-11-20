"""Vòng 3 + 4: đối chiếu chỉ mục với toàn văn, làm sạch, khử trùng, che liên lạc, gắn nhãn.
Ra: data/stage4/corpus.jsonl, rejects.jsonl, doi_chieu.jsonl, text snapshots đã che (cho refinery)."""
import json, glob, os, re, unicodedata, hashlib, sys
from datasketch import MinHash, MinHashLSH
os.makedirs('data/stage4/text_snapshots', exist_ok=True)
idx = {json.loads(l)['docid']: json.loads(l) for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8')}
plan = {r['docid'] for r in json.load(open('data/stage2/sample_plan.json', encoding='utf-8'))}
man = {json.loads(l)['docid']: json.loads(l) for l in open('data/raw_pdf/manifest.jsonl', encoding='utf-8')}
def nfc(s): return unicodedata.normalize('NFC', s)
def ncode(s):
    s = nfc(s).replace('Ð', 'Đ').replace('–', '-').replace('—', '-').upper()
    return re.sub(r'[\s_]', '', s).replace('O', '0') if False else re.sub(r'[\s_]', '', s)
EMAIL = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
PHONE = re.compile(r'(?<![\d.,])(?:\+?84|0)[\s(]*\d{1,3}[)\s]*(?:[\s.\-]?\d){4,9}(?![\d,]|\.\d)')
KEY = re.compile(r'(thoại|đt\b|đt:|tel|fax|di động|hotline|liên hệ|sđt|zalo)', re.I)
def redact(t):
    n_e = len(EMAIL.findall(t)); t = EMAIL.sub('[EMAIL]', t); out, last, n_p = [], 0, 0
    for m in PHONE.finditer(t):
        left = t[max(0, m.start() - 45):m.start()]
        bare = re.fullmatch(r'(?:\+84|0)\d{9,10}', m.group(0)) is not None
        if KEY.search(left) or bare:
            out.append(t[last:m.start()] + '[SĐT]'); last = m.end(); n_p += 1
    out.append(t[last:]); t = ''.join(out)
    return t, n_e, n_p
DATE = re.compile(r'ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})', re.I)
STAMP = re.compile(r'^.*(gian ký|ời g|\+07:?00|Người ký\s*:\s*Cổng|thongtinchinhphu@|Cơ quan\s*:\s*Văn phòng Chính phủ|H\s*I\s*N\s*H\s*P\s*H\s*U\s*[._\s]*[vV][nN]|Ký bởi|Ký bạt).*$', re.M)
STAMP2 = re.compile(r'^.*(thongtinchinhphu|chinhphu\s*\.\s*vn|Người ký\s*:|Ng[ưu]ời k[ýy]\s*:\s*C|Cơ quan\s*:\s*V[aăâạậ]n\s*ph).*$|^[^a-zà-ỹ\n]*C[ÔỔOÓ]NG\s*TH[ÔOÓ]NG\s*T[ÍIÌ]N[^a-zà-ỹ\n]*$|^[^a-zà-ỹ\n]*(Đ[ẾE]N|DEN)\s*[:.]?\s*(S[ốô]|Ng[àa]y|Gi[ờơ]|quy)[^\n]{0,40}$|^\s*Ng[àa]?y\s*:\s*[^\n]{0,25}$|^\s*Gi[ờơ]\s*:[^\n]{0,25}$', re.M)
INLINE = re.compile(r'[|‘\'"]?\s*C[ÔỔOÓ]NG\s*TH[ÔOÓ]NG\s*:?\s*T\S{0,2}[NM]\b[^\n]{0,30}?(PH\S{1,2}\b|\|)|k[ýy]\s*:\s*C[ổôo]ng\s*Th[ôo]ng\s*tin\s*đi[ệe]n\s*t[ửừ]\s*Ch[íi]nh\s*ph[ủùu]|C[ÔỔOÓ]NG\s*TH[ÔOÓ]NG\s*:?\s*T\S{0,2}[NM]\b')
def strip_stamp(t):
    n2 = len(STAMP2.findall(t)) + len(INLINE.findall(t)); t = INLINE.sub(' ', STAMP2.sub('', t))
    n1 = len(STAMP.findall(t)); return re.sub(r'\n{3,}', '\n\n', STAMP.sub('', t)), n1 + n2
def lev1(a, b):
    if a == b: return 0
    if abs(len(a) - len(b)) > 1: return 2
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b))
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return 1 if any(l[:i] + l[i + 1:] == s for i in range(len(l))) else 2
def code_status(idx_code, found):
    a = ncode(idx_code)
    if not found: return 'khong_doc_duoc'
    best = min(found, key=lambda f: lev1(a, ncode(f)))
    b = ncode(best)
    if a == b: return 'khop'
    if re.search(r'[^0-9A-ZĐ/.\-&]', b.split('/')[0]): return 'khong_doc_duoc'
    return 'gan_khop' if lev1(a, b) == 1 else 'khac'
SO = re.compile(r'Số\s*[:;.]?\s*([0-9][0-9A-Za-zĐÐđ/.\-–\s]{2,45}?)(?=\s{2,}|\n|Hà Nội|$)')
VI = re.compile(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', re.I)
def toks(x): return set(re.findall(r'[a-zà-ỹđ]{2,}', nfc(x.lower())))
STOPW = toks('về việc của và các cho trong theo năm tại với được đến từ một những này đã v/v')
corpus, rejects, dc = [], [], []
lsh = MinHashLSH(threshold=0.9, num_perm=64); mh = {}; seen_sha = {}
for f in sorted(glob.glob('data/text/*.json')):
    r = json.load(open(f, encoding='utf-8')); d = r['docid']
    if d not in plan: continue
    meta = idx[d]
    def rej(stage, reason, **kw):
        rejects.append({'docid': d, 'so_ky_hieu': meta['so_ky_hieu'], 'stage': stage, 'reason': reason, **kw})
    if r['method'] == 'skip_not_pdf': rej('thu_thap', 'tệp không phải PDF'); continue
    if r.get('sha256') in seen_sha: rej('khu_trung', 'trùng tệp y hệt', with_docid=seen_sha[r['sha256']]); continue
    seen_sha[r.get('sha256')] = d
    text = nfc('\n\f\n'.join(p['text'] for p in r['pages']))
    body = text.replace('Cổng Thông tin điện tử Chính phủ', '')
    if len(body.strip()) < 200: rej('boc_chu', 'không bóc được chữ đủ dài (<200 ký tự)', chars=len(body.strip())); continue
    confs = [p['conf'] for p in r['pages'] if p.get('conf') is not None]
    mconf = round(sum(confs) / len(confs), 1) if confs else None
    if mconf is not None and mconf < 70: rej('boc_chu', 'độ tin OCR trung bình dưới 70', conf=mconf); continue
    text, n_stamp = strip_stamp(text)
    red, n_e, n_p = redact(text)
    letters = len(re.findall(r'[A-Za-zÀ-ỹ]', red[:20000])) or 1
    vi_ratio = len(VI.findall(red[:20000])) / letters
    if vi_ratio < 0.06: rej('boc_chu', 'chữ mất dấu tiếng Việt (bảng mã hoặc OCR hỏng)', vi_ratio=round(vi_ratio, 3)); continue
    tt = toks(meta['trich_yeu']) - STOPW; head = toks(red[:6000])
    overlap = round(len(tt & head) / len(tt), 2) if tt else 1.0
    # đối chiếu số ký hiệu và ngày
    code_ok = ncode(meta['so_ky_hieu']) in ncode(red)
    so_found = [nfc(m.group(1)).strip() for m in SO.finditer(red)][:3]
    dates = {f'{y}-{int(mo):02d}-{int(dd):02d}' for dd, mo, y in DATE.findall(red)}
    date_ok = meta['ngay_ban_hanh'] in dates
    cst = 'khop' if code_ok else code_status(meta['so_ky_hieu'], so_found)
    fn = man[d]['url'].rsplit('/', 1)[-1]; num = re.match(r'^0*(\d+)', fn)
    fn_ok = bool(num) and re.match(r'^0*(\d+)', meta['so_ky_hieu'].strip()) is not None and num.group(1) == re.match(r'^0*(\d+)', meta['so_ky_hieu'].strip()).group(1)
    res = {'docid': d, 'so_ky_hieu_chi_muc': meta['so_ky_hieu'], 'so_ky_hieu_khop': code_ok, 'trang_thai_so_ky_hieu': cst, 'ten_tep': fn, 'so_trong_ten_tep_khop': fn_ok, 'so_trong_van_ban': so_found,
           'ngay_chi_muc': meta['ngay_ban_hanh'], 'ngay_khop': date_ok, 'ngay_trong_van_ban': sorted(dates)[:5], 'method': r['method'], 'conf': mconf}
    res['trung_trich_yeu'] = overlap
    dc.append(res)
    if overlap < 0.25:
        rej('doi_chieu', 'nội dung tệp không khớp trích yếu (có thể đính kèm nhầm, hoặc OCR quá kém)', overlap=overlap, so_ky_hieu_toan_van=cst); continue
    # khử trùng gần đúng
    flat = re.sub(r'\s+', ' ', red.lower())
    sh = set(flat[i:i + 7] for i in range(0, max(0, len(flat) - 7), 3))
    m = MinHash(num_perm=64); [m.update(x.encode()) for x in sh]
    near = lsh.query(m)
    if near: rej('khu_trung', 'gần trùng (Jaccard ước lượng ≥0,9)', with_docid=near[0]); continue
    lsh.insert(d, m)
    snap = f'txt_{d}.txt'; open(f'data/stage4/text_snapshots/{snap}', 'w', encoding='utf-8').write(red)
    corpus.append({'docid': d, 'so_ky_hieu': meta['so_ky_hieu'], 'ngay_ban_hanh': meta['ngay_ban_hanh'], 'trich_yeu': meta['trich_yeu'],
                   'loai_van_ban': meta['loai_van_ban'], 'hinh_thuc': meta['hinh_thuc'], 'co_quan_ky_hieu': meta['co_quan_ky_hieu'],
                   'cap': 'Trung ương', 'thoi_ky': 'sau 01/7/2025' if meta['ngay_ban_hanh'] >= '2025-07-01' else 'trước 01/7/2025',
                   'nguon_chi_muc': 'https://vanban.chinhphu.vn/?pageid=27160&docid=' + d, 'nguon_tep': man[d]['url'], 'sha256_tep': r.get('sha256'),
                   'boc_chu': r['method'], 'trang_da_boc': [p['page'] for p in r['pages']], 'tong_so_trang': r.get('pages_total'), 'do_tin_ocr': mconf,
                   'da_che': {'email': n_e, 'so_dien_thoai': n_p}, 'doi_chieu': {'trung_trich_yeu': overlap, 'so_ky_hieu_toan_van': cst, 'ngay_ban_hanh_toan_van': date_ok, 'so_trong_ten_tep': fn_ok}, 'dong_dau_cong_da_bo': n_stamp,
                   'snapshot': snap, 'text': red})
w = lambda name, rows: open(f'data/stage4/{name}', 'w', encoding='utf-8').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))
w('corpus.jsonl', corpus); w('rejects.jsonl', rejects); w('doi_chieu.jsonl', dc)
from collections import Counter
print('docs in', len(corpus) + len(rejects), 'kept', len(corpus), 'rejected', len(rejects), Counter(x['reason'] for x in rejects))
print(Counter(x['trang_thai_so_ky_hieu'] for x in dc), 'filename num match', sum(x['so_trong_ten_tep_khop'] for x in dc), '/', len(dc))
print('code match', sum(x['so_ky_hieu_khop'] for x in dc), '/', len(dc), ' date match', sum(x['ngay_khop'] for x in dc))
print(Counter(x['loai_van_ban'] for x in corpus))
print('redacted emails', sum(x['da_che']['email'] for x in corpus), 'phones', sum(x['da_che']['so_dien_thoai'] for x in corpus))
