"""Claims cho chỉ mục ba tỉnh. Tự kiểm: chỉ ghi claim khi evidence_span có nguyên văn trong bản chụp (sau chuẩn hoá như engine)."""
import json, sys, os, shutil, html, unicodedata
D = sys.argv[1]; os.makedirs(os.path.join(D, 'snapshots'), exist_ok=True)
def norm(s): return unicodedata.normalize('NFC', html.unescape(s))
pref = {'thainguyen.gov.vn': 'tn', 'hungyen.gov.vn': 'hy', 'tracuuvanban.quangtri.gov.vn': 'qt'}
mans = {k: {json.loads(l)['page']: json.loads(l) for l in open(f'data/prov/{k}/manifest.jsonl', encoding='utf-8')} for k in ['tn', 'hy', 'qt']}
cache = {}; out = []; skipped = 0
for l in open('data/prov/index_prov.jsonl', encoding='utf-8'):
    r = json.loads(l)
    if r['ngay_ban_hanh'] < '2020-03-05': continue
    k = pref[r['nguon']]; snap = f"{k}_{r['snapshot']}"; sp = os.path.join(D, 'snapshots', snap)
    if not os.path.exists(sp): shutil.copy(f"data/prov/{k}/{r['snapshot']}", sp)
    if snap not in cache: cache[snap] = norm(open(sp, encoding='utf-8').read())
    m = mans[k][int(r['snapshot'][1:5])]
    cap = {'url': m['url'], 'fetched_at': m['captured_at'], 'snapshot': snap, 'source': r['nguon'] + ' (danh sách)'}
    ent = f"{r['so_ky_hieu']} · {r['docid']}"
    def w(field, value, span, ext):
        global skipped
        if not span or norm(span) not in cache[snap]: skipped += 1; return
        out.append({'entity': ent, 'field': field, 'value': value, 'evidence_span': span, 'extraction': ext, 'tier': 'A', 'capture': cap})
    w('so_ky_hieu', r['so_ky_hieu'], r['spans']['code'], 'normalized' if k == 'qt' else 'verbatim')
    w('ngay_ban_hanh', r['ngay_ban_hanh'], r['spans']['date'], 'normalized')
    if r['trich_yeu']: w('trich_yeu', r['trich_yeu'], r['trich_yeu'][:60], 'verbatim')
    if r['tep']: w('tep_dinh_kem', r['tep'][0], r['tep'][0].replace('https://hungyen.gov.vn', ''), 'verbatim' if k == 'tn' else 'normalized')
    w('loai_van_ban', r['loai_van_ban'], r['spans']['code'], 'inferred'); w('hinh_thuc', r['hinh_thuc'], r['spans']['code'], 'inferred')
    if r['co_quan_ky_hieu']: w('co_quan_ky_hieu', r['co_quan_ky_hieu'], r['spans']['code'], 'inferred')
open(os.path.join(D, 'claims_prov.jsonl'), 'w', encoding='utf-8').write(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in out))
print('prov claims', len(out), 'skipped (span not verbatim)', skipped, 'snapshots', len(cache))
