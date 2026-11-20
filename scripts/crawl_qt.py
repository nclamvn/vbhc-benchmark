"""Quảng Trị: chỉ chỉ mục từ trang HTML được robots cho phép (/ubnd-tinh?page=N). Không gọi /api/ (robots cấm)."""
import re, time, hashlib, json, os, datetime as dt, requests
OUT = 'data/prov/qt'; B = 'https://tracuuvanban.quangtri.gov.vn/ubnd-tinh'
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s)'
man = open(f'{OUT}/manifest.jsonl', 'a', encoding='utf-8')
for page in range(1, 200):
    url = B if page == 1 else f'{B}?page={page}'
    for i in range(5):
        try:
            r = S.get(url, timeout=60); s = r.content.decode('utf-8', 'replace')
            if r.status_code == 200: break
        except Exception as e: print('retry', e)
        time.sleep(4 * (i + 1))
    n = len(re.findall(r'href="/van-ban/[0-9a-f-]{36}"', s))
    if n == 0: print('no rows at', page); break
    open(f'{OUT}/p{page:04d}.html', 'w', encoding='utf-8').write(s)
    man.write(json.dumps({'page': page, 'url': url, 'sha256': hashlib.sha256(s.encode()).hexdigest(), 'captured_at': dt.datetime.now(dt.UTC).isoformat(), 'rows': n}) + '\n'); man.flush()
    time.sleep(1.0)
print('done', page)
