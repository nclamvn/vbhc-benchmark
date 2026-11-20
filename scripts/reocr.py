import json, os, subprocess, tempfile, sys, importlib.util
spec = importlib.util.spec_from_file_location('w', 'scripts/ocr_worker.py')
src = open('scripts/ocr_worker.py').read().split('idle = 0')[0].replace('W, NW = int(sys.argv[1]), int(sys.argv[2])', '')
ns = {}; exec(src, ns)
ids = json.load(open('data/stage4/reocr_list.json'))
part = [d for i, d in enumerate(ids) if i % int(sys.argv[2]) == int(sys.argv[1])]
for d in part:
    f = f'data/text/{d}.json'; r = json.load(open(f, encoding='utf-8'))
    if r['method'] == 'ocr_vie': continue
    p = 'data/raw_pdf/' + r['file']; n = r['pages_total']; want = sorted({i for i in (1, 2, n) if 1 <= i <= n})
    with tempfile.TemporaryDirectory() as tmp:
        pg = []
        for i in want:
            t, c = ns['ocr_page'](p, i, tmp); pg.append({'page': i, 'text': t, 'conf': round(c, 1)})
    r.update(method='ocr_vie', pages=pg, note='OCR lại: lớp chữ PDF dùng bảng mã cũ, mất dấu')
    json.dump(r, open(f, 'w', encoding='utf-8'), ensure_ascii=False)
print('done', sys.argv[1])
