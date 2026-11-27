"""M8.4 · Đợt cào C, cổng Quảng Ninh (quangninh.gov.vn, không có robots.txt; 1 yêu cầu mỗi giây).
Mục tiêu ghi trước: bù kế hoạch, chỉ thị, báo cáo cho tập soạn văn bản (ngưỡng M8: kế hoạch ≥ 5%, chỉ thị ≥ 5%, báo cáo ≥ 2%).
Lọc danh sách theo loại (?Search=VB&LoaiVanBan=…), lật trang bằng nút "Next" (postback ASP.NET), lưu bản chụp từng trang.
Dùng:
  python3 scripts/m8_dot_c_qn.py ds <giây> [tối đa mỗi loại]   → data/dot_c/qn/ds_<loại>_pNNNN.html, data/dot_c/qn/chi_muc.jsonl
  python3 scripts/m8_dot_c_qn.py tai <giây>                    → tải tệp đính kèm vào data/raw_pdf/qn-<vbId>.pdf, data/dot_c/qn/manifest.jsonl
"""
import re, os, sys, json, time, html, hashlib, datetime as dt
D = 'data/dot_c/qn'; os.makedirs(D, exist_ok=True)
U = 'https://www.quangninh.gov.vn/Trang/van-ban-chi-dao.aspx'
LOAI = {'11': 'Kế hoạch', '14': 'Chỉ thị', '40': 'Báo cáo'}
MOC = '2020-03-05'

def phien():
    import requests
    s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s; VBHC-Bench open dataset)'; return s
def an(s): return {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', s)}
def dong(s):
    out = []
    for m in re.finditer(r'href="(https://www\.quangninh\.gov\.vn/Trang/van-ban-quy-pham-chi-tiet\.aspx\?vbId=(\d+)[^"]*)">\s*([^<]+?)\s*</a>(.*?)(?=href="https://www\.quangninh\.gov\.vn/Trang/van-ban-quy-pham-chi-tiet\.aspx\?vbId=|</table>)', s, re.S):
        than = m.group(4); o = [html.unescape(x).strip() for x in re.findall(r'>([^<>]+)<', than) if x.strip()]
        ngay = next((x for x in o if re.fullmatch(r'\d\d/\d\d/\d{4}', x)), None)
        tep = re.search(r"href='([^']+\.(?:pdf|docx?))'", than, re.I)
        if not ngay: continue
        i = o.index(ngay); ty = o[i + 1] if i + 1 < len(o) else ''; cq = o[i + 2] if i + 2 < len(o) else ''
        d, mo, y = ngay.split('/')
        out.append({'vbId': m.group(2), 'chi_tiet': m.group(1), 'so_ky_hieu': m.group(3), 'ngay_ban_hanh': f'{y}-{mo}-{d}', 'trich_yeu': ty, 'co_quan_ten': cq, 'tep': tep.group(1) if tep else None})
    return out

def ds(han, toi_da):
    S = phien(); t0 = time.time(); cm = f'{D}/chi_muc.jsonl'
    co = {json.loads(l)['vbId'] for l in open(cm, encoding='utf-8')} if os.path.exists(cm) else set()
    f = open(cm, 'a', encoding='utf-8')
    for ma, ten in LOAI.items():
        n_loai = sum(1 for l in open(cm, encoding='utf-8') if json.loads(l)['loai_van_ban'] == ten) if os.path.exists(cm) else 0
        url = f'{U}?Search=VB&LoaiVanBan={ma}'; s = S.get(url, timeout=60).text; trang = 1
        while time.time() - t0 < han and n_loai < toi_da:
            p = f'{D}/ds_{ma}_p{trang:04d}.html'; open(p, 'w', encoding='utf-8').write(s)
            rows = dong(s)
            for r in rows:
                if r['vbId'] in co or r['ngay_ban_hanh'] < MOC: continue
                r.update(loai_van_ban=ten, nguon='quangninh.gov.vn', snapshot=os.path.basename(p), sha256_trang=hashlib.sha256(s.encode()).hexdigest(),
                         captured_at=dt.datetime.now(dt.UTC).isoformat())
                f.write(json.dumps(r, ensure_ascii=False) + '\n'); f.flush(); co.add(r['vbId']); n_loai += 1
            if not rows or min(r['ngay_ban_hanh'] for r in rows) < MOC: break
            h = an(s); nut = re.search(r'WebForm_PostBackOptions\(&quot;([^&]+btnNext)&quot;', s)
            if not nut: break
            h['__EVENTTARGET'] = nut.group(1); h['__EVENTARGUMENT'] = ''
            time.sleep(1.0); s = S.post(url, data=h, timeout=60).text; trang += 1
        print(ten, 'đã có', n_loai, 'dòng; trang cuối', trang, flush=True)

def tai(han):
    S = phien(); t0 = time.time(); mf = f'{D}/manifest.jsonl'
    xong_tot = {json.loads(l)['vbId'] for l in open(mf, encoding='utf-8') if json.loads(l).get('file')} if os.path.exists(mf) else set()   # tải lại các lần hỏng
    out = open(mf, 'a', encoding='utf-8'); n = 0
    # máy chủ trả chậm (~100 KB/giây): ưu tiên chỉ thị, rồi báo cáo, rồi kế hoạch; mỗi loại tối đa TRAN văn bản
    R = [json.loads(l) for l in open(f'{D}/chi_muc.jsonl', encoding='utf-8')]
    TRAN = {'Chỉ thị': 10**6, 'Báo cáo': 150, 'Kế hoạch': 150}; dem = {}
    R = sorted(R, key=lambda r: ['Chỉ thị', 'Báo cáo', 'Kế hoạch'].index(r['loai_van_ban']))
    for r in R:
        dem[r['loai_van_ban']] = dem.get(r['loai_van_ban'], 0) + 1
        if dem[r['loai_van_ban']] > TRAN[r['loai_van_ban']]: continue
        if r['vbId'] in xong_tot or not r['tep'] or not r['tep'].lower().endswith('.pdf'): continue
        if time.time() - t0 > han: break
        rec = {'vbId': r['vbId'], 'url': r['tep'], 'fetched_at': dt.datetime.now(dt.UTC).isoformat()}
        try:
            from urllib.parse import quote
            u = r['tep'].split('/Attachments/')[0] + '/Attachments/' + quote(r['tep'].split('/Attachments/')[1], safe='/')   # tên tệp có ngoặc, dấu cách
            resp = S.get(u, timeout=90); rec['status'] = resp.status_code
            if resp.status_code == 200 and resp.content[:4] == b'%PDF':
                p = f"data/raw_pdf/qn-{r['vbId']}.pdf"; open(p, 'wb').write(resp.content)
                rec.update(file=os.path.basename(p), bytes=len(resp.content), sha256=hashlib.sha256(resp.content).hexdigest())
        except Exception as e: rec['error'] = str(e)[:200]
        out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush(); n += 1; time.sleep(1.0)
    print('tải lượt này', n, flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'ds': ds(float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 400)
    else: tai(float(sys.argv[2]))
