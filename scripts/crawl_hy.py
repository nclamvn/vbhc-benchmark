"""Hưng Yên: danh mục văn bản ban hành, phân trang GET ?page=N. Lưu snapshot từng trang."""
import re, time, hashlib, json, sys, os, datetime as dt, requests
OUT = 'data/prov/hy'; B = 'https://hungyen.gov.vn/cate-vb-van-ban-ban-hanh-vb215.html'; MAXP = int(sys.argv[1])
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s)'
man = open(f'{OUT}/manifest.jsonl', 'a', encoding='utf-8')
for page in range(1, MAXP + 1):
    p = f'{OUT}/p{page:04d}.html'
    if os.path.exists(p): continue
    url = B if page == 1 else f'{B}?field=0&type=0&q=&page={page}'
    for i in range(5):
        try:
            r = S.get(url, timeout=60); s = r.content.decode('utf-8', 'replace')
            if r.status_code == 200: break
        except Exception as e: print('retry', e)
        time.sleep(4 * (i + 1))
    rows = re.findall(r'<tr><td>\d+</td><td><strong>', s)
    if not rows: print('no rows at', page); break
    open(p, 'w', encoding='utf-8').write(s)
    man.write(json.dumps({'page': page, 'url': url, 'sha256': hashlib.sha256(s.encode()).hexdigest(), 'captured_at': dt.datetime.now(dt.UTC).isoformat(), 'rows': len(rows)}) + '\n'); man.flush()
    time.sleep(1.0)
print('done', page)
