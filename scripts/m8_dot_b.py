"""M8.2 · Đợt cào B (QĐ-18): văn bản hành chính trung ương từ 03/2025 đã có trong chỉ mục nhưng chưa có toàn văn.
Lớp 1 (chọn nguồn): vanban.chinhphu.vn (robots.txt cho phép); tệp ở datafiles.chinhphu.vn do cổng công bố; 1 yêu cầu mỗi giây.
Mục tiêu đợt ghi trước: đưa văn bản từ 03/2025 lên ≥ 40% bể soạn văn bản; không làm công văn vượt 35%.
Loại ngay từ trích yếu các văn bản về cá nhân (khen thưởng, danh hiệu, nhân sự, quốc tịch, liệt sĩ, kỷ luật) để hạn chế thông tin cá nhân.
Dùng:
  python3 scripts/m8_dot_b.py chon             → data/dot_b/ke_hoach.json
  python3 scripts/m8_dot_b.py tai <giây>        → tải PDF (tiếp tục được), data/dot_b/manifest.jsonl, tệp ở data/raw_pdf/
"""
import json, os, re, sys, time, hashlib, datetime as dt, collections
D = 'data/dot_b'; os.makedirs(D, exist_ok=True)
LOAI = {'Quyết định (cá biệt)', 'Công điện', 'Chỉ thị', 'Công văn', 'Thông báo', 'Báo cáo', 'Kế hoạch'}
TRU = re.compile(r'khen thưởng|tặng|bằng khen|huân chương|huy chương|danh hiệu|kỷ luật|truy tặng|liệt sĩ|thi đua|chiến sĩ|nhà giáo|thầy thuốc|nghệ sĩ|bổ nhiệm|miễn nhiệm|phê chuẩn|cho thôi|nghỉ hưu|điều động|xóa tên|đặc xá|quốc tịch', re.I)

def chon():
    co = {json.loads(l)['docid'] for l in open('data/stage4_v4/corpus.jsonl', encoding='utf-8')}
    R = [json.loads(l) for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8')]
    kh, bo = [], collections.Counter()
    for r in sorted(R, key=lambda r: r['docid']):
        if r['docid'] in co or not r.get('tep') or r['ngay_ban_hanh'] < '2025-03-01' or r['loai_van_ban'] not in LOAI or r.get('hinh_thuc') != 'Hành chính': continue
        m = TRU.search(r['trich_yeu'])
        if m: bo[m.group(0).lower()] += 1; continue
        kh.append({k: r[k] for k in ('docid', 'so_ky_hieu', 'ngay_ban_hanh', 'trich_yeu', 'tep', 'loai_van_ban', 'hinh_thuc', 'co_quan_ky_hieu')})
    json.dump(kh, open(f'{D}/ke_hoach.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(kh), 'văn bản;', dict(collections.Counter(r['loai_van_ban'] for r in kh)), '; loại từ trích yếu:', sum(bo.values()))

def tai(han):
    import requests
    kh = json.load(open(f'{D}/ke_hoach.json', encoding='utf-8')); mf = f'{D}/manifest.jsonl'
    xong = {json.loads(l)['docid'] for l in open(mf, encoding='utf-8')} if os.path.exists(mf) else set()
    S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite, 1 req/s; VBHC-Bench open dataset)'
    t0 = time.time(); out = open(mf, 'a', encoding='utf-8'); n = 0
    for r in kh:
        if r['docid'] in xong: continue
        if time.time() - t0 > han: break
        url = r['tep'][0]; rec = {'docid': r['docid'], 'url': url, 'fetched_at': dt.datetime.now(dt.UTC).isoformat()}
        for a in range(3):
            try:
                resp = S.get(url, timeout=90); rec['status'] = resp.status_code
                if resp.status_code == 200 and resp.content[:4] == b'%PDF':
                    p = f"data/raw_pdf/{r['docid']}.pdf"; open(p, 'wb').write(resp.content)
                    rec.update(file=os.path.basename(p), bytes=len(resp.content), sha256=hashlib.sha256(resp.content).hexdigest())
                break
            except Exception as e:
                rec['error'] = str(e)[:200]; time.sleep(4 * (a + 1))
        out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush(); n += 1
        time.sleep(1.0)
    print('tải lượt này', n, '; tổng', len(xong) + n, '/', len(kh), flush=True)

if __name__ == '__main__':
    {'chon': lambda: chon(), 'tai': lambda: tai(float(sys.argv[2]) if len(sys.argv) > 2 else 540)}[sys.argv[1]]()
