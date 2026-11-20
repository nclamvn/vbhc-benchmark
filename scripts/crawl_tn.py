"""Thái Nguyên: danh sách văn bản chỉ đạo (ASP.NET GridView, phân trang postback). Lưu snapshot từng trang."""
import re, html, time, hashlib, json, sys, os, datetime as dt, requests
OUT = 'data/prov/tn'; U = 'https://thainguyen.gov.vn/van-ban-phap-luat'; MAXP = int(sys.argv[1]); T = float(sys.argv[2])
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s)'
def fields(s): return {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', s)}
def get(fn, *a, **k):
    for i in range(5):
        try:
            r = fn(*a, timeout=60, **k)
            txt = r.content.decode('utf-8', 'replace')
            if r.status_code == 200 and 'lbSoHieuVB_' in txt: return txt
        except Exception as e: print('retry', e)
        time.sleep(4 * (i + 1))
    raise SystemExit('fail')
man = open(f'{OUT}/manifest.jsonl', 'a', encoding='utf-8'); t0 = time.time()
import glob
ex = sorted(glob.glob(f'{OUT}/p*.html'))
if ex: page = int(os.path.basename(ex[-1])[1:5]); s = open(ex[-1], encoding='utf-8').read()
else: page = 1; s = get(S.get, U)
while page <= MAXP and time.time() - t0 < T:
    p = f'{OUT}/p{page:04d}.html'
    if not os.path.exists(p):
        open(p, 'w', encoding='utf-8').write(s)
        man.write(json.dumps({'page': page, 'url': U, 'method': 'GET' if page == 1 else f'POST Page${page}', 'sha256': hashlib.sha256(s.encode()).hexdigest(), 'captured_at': dt.datetime.now(dt.UTC).isoformat()}) + '\n'); man.flush()
    ds = [dt.date(int(y), int(m), int(d)) for d, m, y in re.findall(r'lbNgayBanHanh_\d+">(\d\d)/(\d\d)/(\d{4})<', s)]
    if ds and max(ds) < dt.date(2020, 3, 5): print('cutoff', page); break
    f = fields(s); f['__EVENTTARGET'] = 'ctrl_51405_98$gvDanhSach'; f['__EVENTARGUMENT'] = f'Page${page + 1}'
    s = get(S.post, U, data=f); page += 1; time.sleep(1.0)
print('last page', page, 'min date', min(ds) if ds else None)
