import json, os, time, hashlib, datetime as dt, requests, sys
plan = json.load(open('data/stage2/sample_plan.json', encoding='utf-8'))
os.makedirs('data/raw_pdf', exist_ok=True)
mf = 'data/raw_pdf/manifest.jsonl'
done = {json.loads(l)['docid'] for l in open(mf, encoding='utf-8')} if os.path.exists(mf) else set()
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (research crawler; polite)'
t0 = time.time(); out = open(mf, 'a', encoding='utf-8'); n = 0
for r in plan:
    if r['docid'] in done: continue
    if time.time() - t0 > float(sys.argv[1]): break
    url = r['tep'][0]; rec = {'docid': r['docid'], 'url': url, 'fetched_at': dt.datetime.now(dt.UTC).isoformat()}
    for a in range(4):
        try:
            resp = S.get(url, timeout=90); rec['status'] = resp.status_code
            if resp.status_code == 200:
                ext = '.pdf' if resp.content[:4] == b'%PDF' else ('.docx' if resp.content[:2] == b'PK' else '.bin')
                p = f"data/raw_pdf/{r['docid']}{ext}"; open(p, 'wb').write(resp.content)
                rec.update(file=os.path.basename(p), bytes=len(resp.content), sha256=hashlib.sha256(resp.content).hexdigest())
            break
        except Exception as e:
            rec['error'] = str(e)[:200]; time.sleep(4 * (a + 1))
    out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush(); n += 1; time.sleep(0.7)
print('fetched this run', n, 'total', len(done) + n, 'of', len(plan))
