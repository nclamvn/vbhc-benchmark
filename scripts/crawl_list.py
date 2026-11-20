"""Vòng 1: chụp danh sách vanban.chinhphu.vn, dừng khi toàn trang cũ hơn mốc.
Lưu mỗi trang thành snapshot HTML + manifest (url, page, sha256, thời điểm)."""
import re, html, time, hashlib, json, sys, os, datetime as dt
import requests
OUT = sys.argv[1]; CUTOFF = dt.date(2020, 3, 5); MAXP = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
U = 'https://vanban.chinhphu.vn/he-thong-van-ban'
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s)'
def fields(s):
    return {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', s)}
def dates(s):
    out = []
    for d in re.findall(r'<span class="issued-date">(\d\d/\d\d/\d{4})</span>', s):
        dd, mm, yy = map(int, d.split('/')); out.append(dt.date(yy, mm, dd))
    return out
man = open(os.path.join(OUT, 'manifest.jsonl'), 'a', encoding='utf-8')
done = {json.loads(l)['page'] for l in open(os.path.join(OUT, 'manifest.jsonl'), encoding='utf-8')} if os.path.getsize(os.path.join(OUT, 'manifest.jsonl')) else set()
def get_first():
    for a in range(6):
        try:
            return S.get(U, timeout=60).text
        except Exception as e:
            print('retry first', e); time.sleep(5 * (a + 1))
    raise SystemExit('cannot reach')
import glob
_ex = sorted(glob.glob(os.path.join(OUT, 'p*.html')))
if _ex:
    page = int(os.path.basename(_ex[-1])[1:5]); s = open(_ex[-1], encoding='utf-8').read(); print('resume from', page)
else:
    s = get_first(); page = 1
while page <= MAXP:
    path = os.path.join(OUT, f'p{page:04d}.html')
    if page not in done:
        open(path, 'w', encoding='utf-8').write(s)
        man.write(json.dumps({'page': page, 'url': U, 'method': 'GET' if page == 1 else f'POST Page${page}', 'sha256': hashlib.sha256(s.encode()).hexdigest(), 'captured_at': dt.datetime.utcnow().isoformat() + 'Z', 'rows': len(re.findall(r'<span class="code">', s))}, ensure_ascii=False) + '\n'); man.flush()
    ds = dates(s)
    if ds and max(ds) < CUTOFF:
        print('cutoff reached at page', page); break
    f = fields(s); f['__EVENTTARGET'] = 'ctrl_191017_163$grvDocument'; f['__EVENTARGUMENT'] = f'Page${page + 1}'
    for attempt in range(6):
        try:
            s = S.post(U, data=f, timeout=60).text
            if '<span class="code">' in s: break
        except Exception as e:
            print('retry', page + 1, e)
        time.sleep(4 * (attempt + 1))
    else:
        raise SystemExit(f'failed at page {page + 1}')
    page += 1; time.sleep(1.0)
    if page % 25 == 0: print('page', page, 'min date', min(ds) if ds else None, flush=True)
