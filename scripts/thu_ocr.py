"""Thử OCRia-nano-1 (LiteParse) với tiếng Việt trên văn bản quét của VBHC, so với Tesseract tiếng Việt và văn bản OCR đang có trong kho.
Mẫu: N văn bản quét (trang 1 không có lớp chữ), chọn ngẫu nhiên cố định; chỉ OCR 2 trang đầu.
Thước đo, so với chỉ mục (gõ máy, sạch):
  - dung_so: số ký hiệu chuẩn hoá xuất hiện trong bài OCR
  - dung_ngay: ngày ban hành (ngày, tháng, năm) xuất hiện
  - phu_trich_yeu: tỷ lệ âm tiết của trích yếu (giữ dấu) có trong bài OCR, đo khả năng giữ dấu tiếng Việt
  - am_tiet_hop_le: tỷ lệ âm tiết có trong từ điển âm tiết dựng từ trích yếu của toàn chỉ mục
Dùng: python3 scripts/thu_ocr.py [N]   (cần: pip install liteparse; lit models pull ocria-nano; tesseract + gói vie)
"""
import json, os, re, sys, random, subprocess, time, unicodedata, collections
sys.path.insert(0, 'scripts'); import kiem_trung_thuc as k
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
C = {json.loads(l)['docid']: json.loads(l) for l in open(os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'), encoding='utf-8')}
nfc = lambda s: unicodedata.normalize('NFC', s)
def am(s): return [w for w in re.findall(r'[0-9a-zà-ỹđ]+', nfc(s).lower()) if not w.isdigit()]
TD = collections.Counter(w for c in C.values() for w in am(c.get('trich_yeu', '') + ' ' + c['text'][:3000]))
TD = {w for w, n in TD.items() if n >= 20}   # âm tiết gặp từ 20 lần trở lên trong kho: lỗi OCR hiếm khi lặp nhiều như vậy

def quet(p):
    r = subprocess.run(['pdftotext', '-l', '1', p, '-'], capture_output=True, text=True)
    return len(re.sub(r'\s', '', r.stdout)) < 30
rng = random.Random(20261127); ids = sorted(d for d in C if os.path.exists(f'data/raw_pdf/{d}.pdf')); rng.shuffle(ids)
mau = []
for d in ids:
    if quet(f'data/raw_pdf/{d}.pdf') and C[d].get('trich_yeu') and C[d].get('ngay_ban_hanh'): mau.append(d)
    if len(mau) == N: break

def lit(p, backend):
    t0 = time.time()
    r = subprocess.run(['lit', 'parse', p, '--target-pages', '1-2', '--ocr-backend', backend, '--ocr-language', 'vie', '--tessdata-path', os.environ.get('TESSDATA', '/usr/share/tesseract-ocr/5/tessdata'), '--dpi', '250', '-q'],
                       capture_output=True, text=True, timeout=600)
    return nfc(r.stdout), time.time() - t0

def cham(txt, c):
    t = nfc(txt); tl = t.lower(); so = c['so_ky_hieu_chuan']; so_n = so.split('/')[0]
    flat = re.sub(r'\s+', '', t).upper()
    dung_so = re.sub(r'\s+', '', so).upper() in flat
    y, m, d = c['ngay_ban_hanh'].split('-')
    dung_ngay = bool(re.search(rf'ngày\W*0?{int(d)}\W*tháng\W*0?{int(m)}\W*năm\W*{y}', tl)) or bool(re.search(rf'\b0?{int(d)}[/.-]0?{int(m)}[/.-]{y}\b', tl))
    ty = am(c['trich_yeu']); ws = set(am(t)); aa = am(t)
    return {'dung_so': dung_so, 'dung_ngay': dung_ngay, 'phu_trich_yeu': sum(w in ws for w in ty) / max(1, len(ty)),
            'am_tiet_hop_le': sum(w in TD for w in aa) / max(1, len(aa)), 'so_am_tiet': len(aa)}

KQ = collections.defaultdict(list); chi_tiet = []
for i, d in enumerate(mau, 1):
    c = C[d]; p = f'data/raw_pdf/{d}.pdf'; dong = {'docid': d, 'so': c['so_ky_hieu_chuan']}
    dong['kho_hien_co'] = cham(c['text'][:6000], c)
    for b in ('tesseract', 'ocria-nano'):
        txt, s = lit(p, b); r = cham(txt, c); r['giay'] = round(s, 1); dong[b] = r
        if i <= 3: open(f'/tmp/ocr_{d}_{b}.txt', 'w', encoding='utf-8').write(txt)
    for h in ('kho_hien_co', 'tesseract', 'ocria-nano'): KQ[h].append(dong[h])
    chi_tiet.append(dong); print(i, d, {h: round(dong[h]['phu_trich_yeu'], 2) for h in ('kho_hien_co', 'tesseract', 'ocria-nano')}, flush=True)
tong = {}
for h, v in KQ.items():
    n = len(v); tong[h] = {'n': n, 'dung_so_pct': round(100 * sum(x['dung_so'] for x in v) / n, 1), 'dung_ngay_pct': round(100 * sum(x['dung_ngay'] for x in v) / n, 1),
                           'phu_trich_yeu_pct': round(100 * sum(x['phu_trich_yeu'] for x in v) / n, 1), 'am_tiet_hop_le_pct': round(100 * sum(x['am_tiet_hop_le'] for x in v) / n, 1)}
    if 'giay' in v[0]: tong[h]['giay_moi_van_ban'] = round(sum(x['giay'] for x in v) / n, 1)
os.makedirs('ket_qua/ocr', exist_ok=True)
json.dump({'tong': tong, 'chi_tiet': chi_tiet}, open('ket_qua/ocr/thu_ocria_nano.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(tong, ensure_ascii=False, indent=1))
