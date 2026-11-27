"""M8.4 · Đợt cào C, cổng UBND tỉnh Lai Châu (laichau.gov.vn, không có robots.txt, 1 yêu cầu/giây).
Danh sách lấy qua dịch vụ mà chính trang /he-thong-van-ban gọi (/api/Content/Article/selectAll), trả JSON có số ký hiệu,
loại văn bản, ngày ban hành, tệp đính kèm. Chỉ giữ các trường văn bản; bỏ tên người đăng tin (creatorTitle, creatorCode).
Dùng:
  python3 scripts/m8_dot_c_lc.py ds <giây>    → data/dot_c/lc/chi_muc.jsonl (mọi loại; lọc loại ở bước tải)
  python3 scripts/m8_dot_c_lc.py tai <giây>   → data/raw_pdf/lc-<id>.pdf, data/dot_c/lc/manifest.jsonl
"""
import json, os, re, sys, time, hashlib, base64, datetime as dt
from urllib.parse import quote
import requests
D = 'data/dot_c/lc'; os.makedirs(D, exist_ok=True); GOC = 'https://laichau.gov.vn'
UA = 'vbhc-benchmark/0.1 (nghien cuu du lieu mo; 1 req/s)'
LOAI = {'Kế hoạch': 'Kế hoạch', 'Chỉ thị': 'Chỉ thị', 'Báo cáo': 'Báo cáo'}
MOC = '2020-03-05'   # NĐ 30/2020 có hiệu lực

def phien():
    S = requests.Session(); S.headers['User-Agent'] = UA
    h = S.get(GOC + '/he-thong-van-ban', timeout=60).text
    tok = re.search(r'name="securityToken" value="([^"]+)"', h)[1]
    cfg = json.loads(base64.b64decode(re.search(r"decode64\('([^']+)'\)\),\{\"module\":\"Content.Listing\",\"page\":\"Article.LegalDocument.list\"", h)[1]))
    return S, tok, cfg

def ngay(ts): return (dt.datetime.fromtimestamp(int(ts), dt.timezone(dt.timedelta(hours=7)))).strftime('%Y-%m-%d') if ts else ''

def ds(han):
    S, tok, cfg = phien(); t0 = time.time(); f = f'{D}/chi_muc.jsonl'
    da = {json.loads(l)['id'] for l in open(f, encoding='utf-8')} if os.path.exists(f) else set()
    out = open(f, 'a', encoding='utf-8'); trang = len(da) // 50 + 1; tong = None
    while time.time() - t0 < han:
        time.sleep(1.0)
        d = {'securityToken': tok, 'site': '2000066', 'type': cfg['type'], 'parentId': cfg['parentId'], 'categoryId': cfg['categoryId'],
             'itemsPerPage': 50, 'pageNo': trang, 'orderBy': cfg['orderBy'], 'extraFields': cfg['extraFields']}
        j = S.post(GOC + '/api/Content/Article/selectAll', data=d, timeout=90).json(); tong = j.get('totalItems', tong)
        it = list((j.get('items') or {}).values())
        if not it: break
        for x in it:
            if x['id'] in da: continue
            of = x.get('otherFiles') or {}; of = of if isinstance(of, list) else [v for k, v in sorted(of.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 99)]
            tep = [v['file'] for v in of if isinstance(v, dict) and str(v.get('file', '')).lower().endswith('.pdf')]
            out.write(json.dumps({'id': x['id'], 'so_ky_hieu': x.get('code', ''), 'loai_van_ban': x.get('documentType', ''), 'trich_yeu': x.get('title', ''),
                                  'ngay_ban_hanh': ngay(x.get('issueTime')), 'chi_tiet': GOC + '/' + x.get('rewriteURL', ''), 'tep': (GOC + '/' + tep[0]) if tep else '',
                                  'so_tep': len(tep), 'linh_vuc': x.get('element', ''), 'co_quan_ten': ''}, ensure_ascii=False) + '\n'); da.add(x['id'])
        out.flush(); trang += 1
    print('chỉ mục', len(da), 'trên', tong, 'trang tới', trang, flush=True)

def tai(han):
    S = requests.Session(); S.headers['User-Agent'] = UA; t0 = time.time(); mf = f'{D}/manifest.jsonl'
    xong = {json.loads(l)['id'] for l in open(mf, encoding='utf-8') if json.loads(l).get('file') or json.loads(l).get('bo_qua')} if os.path.exists(mf) else set()
    out = open(mf, 'a', encoding='utf-8'); n = 0
    R = [json.loads(l) for l in open(f'{D}/chi_muc.jsonl', encoding='utf-8')]
    R = [r for r in R if r['loai_van_ban'] in LOAI and r['ngay_ban_hanh'] >= MOC and r['tep']]
    R.sort(key=lambda r: (['Chỉ thị', 'Kế hoạch', 'Báo cáo'].index(r['loai_van_ban']), r['ngay_ban_hanh']), reverse=False)
    for r in R:
        if r['id'] in xong: continue
        if time.time() - t0 > han: break
        rec = {'id': r['id'], 'url': r['tep'], 'fetched_at': dt.datetime.now(dt.UTC).isoformat()}
        try:
            u = GOC + '/' + quote(r['tep'][len(GOC) + 1:], safe='/')
            h = S.head(u, timeout=60, allow_redirects=True); n_b = int(h.headers.get('content-length') or 0)
            if n_b > 6_000_000: rec.update(status=h.status_code, bo_qua='tep_qua_6MB', bytes_khai=n_b)
            else:
                time.sleep(1.0); resp = S.get(u, timeout=180); rec['status'] = resp.status_code
                if resp.status_code == 200 and b'%PDF' in resp.content[:1024]:
                    p = f"data/raw_pdf/lc-{r['id']}.pdf"; open(p, 'wb').write(resp.content)
                    rec.update(file=os.path.basename(p), bytes=len(resp.content), sha256=hashlib.sha256(resp.content).hexdigest())
        except Exception as e: rec['error'] = str(e)[:200]
        out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush(); n += 1; time.sleep(1.0)
    print('tải lượt này', n, flush=True)

if __name__ == '__main__':
    (ds if sys.argv[1] == 'ds' else tai)(float(sys.argv[2]))
