"""Bóc chữ: lớp chữ PDF nếu đủ dài, không thì OCR tesseract (vie) trang 1-2 và trang cuối, 200 dpi.
Ghi data/text/<docid>.json gồm từng trang, phương pháp, độ tin OCR trung bình."""
import json, os, subprocess, sys, time, tempfile, csv, io, hashlib
W, NW = int(sys.argv[1]), int(sys.argv[2])
os.makedirs('data/text', exist_ok=True)
def pages_of(p):
    try:
        out = subprocess.run(['pdfinfo', p], capture_output=True, text=True, timeout=60).stdout
        return int([l for l in out.splitlines() if l.startswith('Pages:')][0].split()[1])
    except Exception: return 0
def ocr_page(p, i, tmp):
    base = os.path.join(tmp, f'p{i}')
    subprocess.run(['pdftoppm', '-r', '200', '-f', str(i), '-l', str(i), '-gray', p, base], timeout=180)
    img = [f for f in os.listdir(tmp) if f.startswith(f'p{i}') and f.endswith('.pgm')][0]
    subprocess.run(['tesseract', os.path.join(tmp, img), base + 'o', '-l', 'vie', '--psm', '4', 'txt', 'tsv'], capture_output=True, timeout=300)
    txt = open(base + 'o.txt', encoding='utf-8').read()
    confs = []
    for row in csv.DictReader(open(base + 'o.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        try:
            c = float(row['conf'])
            if c >= 0 and row['text'].strip(): confs.append(c)
        except Exception: pass
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    return txt, (sum(confs) / len(confs) if confs else 0.0)
idle = 0
while True:
    import glob as _g
    man = [json.loads(l) for p in sorted(_g.glob('data/raw_pdf/manifest*.jsonl')) for l in open(p, encoding='utf-8')]
    todo = [m for m in man if m.get('file') and (int(hashlib.md5(m['docid'].encode()).hexdigest(), 16) % NW == W) and not os.path.exists(f"data/text/{m['docid']}.json")]
    if not todo:
        idle += 1
        if idle > 40: break
        time.sleep(30); continue
    idle = 0
    for m in todo:
        p = 'data/raw_pdf/' + m['file']; rec = {'docid': m['docid'], 'file': m['file'], 'sha256': m.get('sha256')}
        if not p.endswith('.pdf'):
            rec.update(method='skip_not_pdf', pages_total=0, pages=[])
        else:
            n = pages_of(p); rec['pages_total'] = n
            layer = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, timeout=120).stdout
            stamp_only = len(layer.replace('Cổng Thông tin điện tử Chính phủ', '').strip()) < 400
            import re as _re
            _l = len(_re.findall(r'[A-Za-zÀ-ỹ]', layer[:20000])) or 1
            _v = len(_re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', layer[:20000], _re.I))
            if not stamp_only and _v / _l < 0.06: stamp_only = True; rec['note'] = 'OCR thay lớp chữ: bảng mã cũ, mất dấu'
            if not stamp_only:
                pages = layer.split('\f')
                rec.update(method='text_layer', pages=[{'page': i + 1, 'text': t, 'conf': None} for i, t in enumerate(pages) if t.strip()])
            else:
                want = sorted({i for i in (1, 2, n) if 1 <= i <= n})
                with tempfile.TemporaryDirectory() as tmp:
                    pg = []
                    for i in want:
                        try:
                            t, c = ocr_page(p, i, tmp); pg.append({'page': i, 'text': t, 'conf': round(c, 1)})
                        except Exception as e:
                            pg.append({'page': i, 'text': '', 'conf': 0.0, 'error': str(e)[:120]})
                rec.update(method='ocr_vie', pages=pg, stamp_text=layer[:400])
        json.dump(rec, open(f"data/text/{m['docid']}.json", 'w', encoding='utf-8'), ensure_ascii=False)
print('worker', W, 'done')
