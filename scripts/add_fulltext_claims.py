"""Thêm claim đối chiếu từ toàn văn: chỉ khi số ký hiệu (nguyên văn) và ngày tìm thấy trong toàn văn.
Không biến lệch thành claim (lệch chủ yếu do số, ngày viết tay mà OCR đọc sai); lệch đưa vào danh sách cần người xem."""
import json, re, shutil, sys, os
D = sys.argv[1]
corpus = [json.loads(l) for l in open('data/stage4/corpus.jsonl', encoding='utf-8')]
idx = {json.loads(l)['docid']: json.loads(l) for l in open('data/stage2/index_all_rows.jsonl', encoding='utf-8')}
DATE = re.compile(r'ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})', re.I)
base = [l for l in open(os.path.join(D, 'claims.jsonl'), encoding='utf-8') if '"datafiles.chinhphu.vn' not in l]
add = []
for c in corpus:
    t = c['text']; ent = f"{c['so_ky_hieu']} · docid {c['docid']}"
    tier = 'A' if c['boc_chu'] == 'text_layer' else 'B'
    cap = {'url': c['nguon_tep'], 'fetched_at': None, 'snapshot': c['snapshot'], 'source': 'datafiles.chinhphu.vn (toàn văn)', 'method': c['boc_chu']}
    if c['so_ky_hieu'] in t:
        add.append({'entity': ent, 'field': 'so_ky_hieu', 'value': c['so_ky_hieu'], 'evidence_span': c['so_ky_hieu'], 'extraction': 'verbatim', 'tier': tier, 'capture': cap})
    for m in DATE.finditer(t):
        dd, mo, y = m.groups()
        if f'{y}-{int(mo):02d}-{int(dd):02d}' == c['ngay_ban_hanh']:
            add.append({'entity': ent, 'field': 'ngay_ban_hanh', 'value': c['ngay_ban_hanh'], 'evidence_span': m.group(0), 'extraction': 'normalized', 'tier': tier, 'capture': cap}); break
    dc = c['doi_chieu']
    if dc['so_ky_hieu_toan_van'] == 'khac' and not dc['so_trong_ten_tep']:
        fn_num = re.match(r'^0*(\d+)', c['nguon_tep'].rsplit('/', 1)[-1])
        for m in re.finditer(r'Số\s*[:;.]?\s*(\d+\s*/\s*[^\s,;]+)', t):
            found = m.group(1)
            if fn_num and re.match(r'^0*(\d+)', found).group(1) == fn_num.group(1):
                add.append({'entity': ent, 'field': 'so_ky_hieu', 'value': re.sub(r'\s+', '', found), 'evidence_span': found, 'extraction': 'normalized', 'tier': tier, 'capture': cap, 'note': 'Toàn văn và tên tệp cùng lệch với chỉ mục'})
                break
    shutil.copy(f"data/stage4/text_snapshots/{c['snapshot']}", os.path.join(D, 'snapshots', c['snapshot']))
man = {json.loads(l)['docid']: json.loads(l) for l in open('data/raw_pdf/manifest.jsonl', encoding='utf-8')}
for a in add: a['capture']['fetched_at'] = man[a['entity'].split('docid ')[1]]['fetched_at']
open(os.path.join(D, 'claims.jsonl'), 'w', encoding='utf-8').write(''.join(base) + ''.join(json.dumps(a, ensure_ascii=False) + '\n' for a in add))
print('base', len(base), 'added', len(add), 'so', sum(a['field'] == 'so_ky_hieu' for a in add), 'ngay', sum(a['field'] == 'ngay_ban_hanh' for a in add))
