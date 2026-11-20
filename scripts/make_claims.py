import json, sys
src, out = sys.argv[1], sys.argv[2]
man = {json.loads(l)['page']: json.loads(l) for l in open('data/snapshots/list/manifest.jsonl', encoding='utf-8')}
n = 0
with open(out, 'w', encoding='utf-8') as f:
    for l in open(src, encoding='utf-8'):
        r = json.loads(l)
        if r['ngay_ban_hanh'] < '2020-03-05': continue
        page = int(r['snapshot'][1:5]); m = man[page]
        cap = {'url': 'https://vanban.chinhphu.vn/he-thong-van-ban', 'method': m['method'], 'fetched_at': m['captured_at'], 'snapshot': r['snapshot'], 'source': 'vanban.chinhphu.vn (danh sách)'}
        ent = f"{r['so_ky_hieu']} · docid {r['docid']}"
        def w(field, value, span, ext):
            global n; n += 1
            f.write(json.dumps({'entity': ent, 'field': field, 'value': value, 'evidence_span': span, 'extraction': ext, 'tier': 'A', 'capture': cap}, ensure_ascii=False) + '\n')
        w('so_ky_hieu', r['so_ky_hieu'], r['span_code'], 'verbatim')
        w('ngay_ban_hanh', r['ngay_ban_hanh'], r['span_date'], 'normalized')
        if r['trich_yeu']: w('trich_yeu', r['trich_yeu'], r['span_trich'], 'verbatim')
        if r['tep']: w('tep_dinh_kem', r['tep'][0], r['span_files'][0], 'verbatim')
        w('loai_van_ban', r['loai_van_ban'], r['span_code'], 'inferred')
        w('hinh_thuc', r['hinh_thuc'], r['span_code'], 'inferred')
        if r['co_quan_ky_hieu']: w('co_quan_ky_hieu', r['co_quan_ky_hieu'], r['span_code'], 'inferred')
print('claims', n)
