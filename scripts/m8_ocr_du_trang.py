"""M8.1b · OCR các trang còn thiếu cho văn bản chỉ được bóc trang 1, 2 và trang cuối (đợt OCR cũ), để văn bản đủ trang dùng được cho T1.
Chỉ chạy trên PDF đã có trong data/raw_pdf (không cào mạng). Tesseract tiếng Việt, 200 dpi, psm 4 (giống đợt OCR cũ).
Chọn văn bản: loại cần bù (mặc định Chỉ thị), thuộc tập train/valid, trích yếu khớp chỉ mục ≥ 0,8, số ký hiệu không mâu thuẫn, ≤ 8 trang.
Kết quả: data/text_du_trang/<docid>.json (từng trang, có độ tin). Chạy lại sẽ bỏ qua văn bản đã xong.
Dùng: python3 scripts/m8_ocr_du_trang.py "Chỉ thị,Công điện" [giây_tối_đa] [số_luồng]
"""
import json, os, sys, time, tempfile, subprocess, csv, collections
from concurrent.futures import ThreadPoolExecutor
LOAI = sys.argv[1].split(',') if len(sys.argv) > 1 else ['Chỉ thị']
HAN = float(sys.argv[2]) if len(sys.argv) > 2 else 540
NL = int(sys.argv[3]) if len(sys.argv) > 3 else 2
OUT = 'data/text_du_trang'; os.makedirs(OUT, exist_ok=True)
SP = json.load(open('m3/chia_tap.json', encoding='utf-8'))['chia_tap']

def ocr_trang(p, i):
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, 'p')
        subprocess.run(['pdftoppm', '-r', '200', '-f', str(i), '-l', str(i), '-gray', p, base], timeout=180, check=True)
        img = next(f for f in os.listdir(tmp) if f.endswith('.pgm'))
        subprocess.run(['tesseract', os.path.join(tmp, img), base + 'o', '-l', 'vie', '--psm', '4', 'txt', 'tsv'], capture_output=True, timeout=300)
        txt = open(base + 'o.txt', encoding='utf-8').read(); cf = []
        for row in csv.DictReader(open(base + 'o.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            try:
                c = float(row['conf'])
                if c >= 0 and row['text'].strip(): cf.append(c)
            except Exception: pass
    return {'page': i, 'text': txt, 'conf': round(sum(cf) / len(cf), 1) if cf else 0.0}

def chon():
    out = []
    for l in open(os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'), encoding='utf-8'):
        c = json.loads(l)
        if c['loai_van_ban'] not in LOAI or SP.get(c['docid']) not in ('train', 'valid'): continue
        d = c['doi_chieu'] if isinstance(c['doi_chieu'], dict) else eval(c['doi_chieu'])
        n = c['tong_so_trang'] or 0; da = set(c['trang_da_boc'] or [])
        if (d.get('trung_trich_yeu') or 0) < 0.8 or d.get('so_ky_hieu_toan_van') == 'khac' or not (len(da) < n <= 8): continue
        if os.path.exists(f'{OUT}/{c["docid"]}.json') or not os.path.exists(f'data/raw_pdf/{c["docid"]}.pdf'): continue
        out.append((c['docid'], n, sorted(set(range(1, n + 1)) - da)))
    return out

if __name__ == '__main__':
    ds = chon(); t0 = time.time(); xong = 0; trang = 0
    print(f'còn {len(ds)} văn bản, {sum(len(x[2]) for x in ds)} trang thiếu, loại {LOAI}', flush=True)
    with ThreadPoolExecutor(NL) as ex:
        for docid, n, thieu in ds:
            if time.time() - t0 > HAN: break
            p = f'data/raw_pdf/{docid}.pdf'
            pages = list(ex.map(lambda i: ocr_trang(p, i), thieu))
            json.dump({'docid': docid, 'pages_total': n, 'trang_moi': pages, 'cach': 'tesseract vie 200dpi psm4'}, open(f'{OUT}/{docid}.json', 'w', encoding='utf-8'), ensure_ascii=False)
            xong += 1; trang += len(thieu)
    print(f'xong {xong} văn bản, {trang} trang, {round(time.time() - t0)} giây; còn {len(ds) - xong}', flush=True)
