"""Dựng domain vbhc_v2: chỉ mục Cổng Chính phủ + chỉ mục 3 tỉnh + claims đối chiếu toàn văn (chỉ khi khớp nguyên văn)."""
import json, os, re, shutil, glob, unicodedata, html
D = 'engine/domains/vbhc_v4'; S4 = 'data/stage4_v4'; snapd = os.path.join(D, 'snapshots')
for f in glob.glob('engine/domains/vbhc_chinhphu/snapshots/p*.html'):
    t = os.path.join(snapd, os.path.basename(f))
    if not os.path.exists(t): shutil.copy(f, t)
for f in glob.glob(os.path.join(snapd, 'txt_*.txt')): os.remove(f)
base = [l for l in open('engine/domains/vbhc_chinhphu/claims.jsonl', encoding='utf-8') if '"datafiles.chinhphu.vn' not in l]
prov = open(os.path.join(D, 'claims_prov.jsonl'), encoding='utf-8').read().splitlines(keepends=True)
DATE = re.compile(r'ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})', re.I)
mans = {}
for mf in sorted(glob.glob('data/raw_pdf/manifest*.jsonl')):
    for l in open(mf, encoding='utf-8'):
        x = json.loads(l)
        if x.get('file'): mans[x['docid']] = x
add = []
for l in open(f'{S4}/corpus.jsonl', encoding='utf-8'):
    c = json.loads(l); t = c['text']; d = c['docid']
    ent = f"{c['so_ky_hieu']} · docid {d}" if c['nguon'] == 'vanban.chinhphu.vn' else f"{c['so_ky_hieu']} · {d}"
    tier = 'A' if c['boc_chu'] == 'text_layer' else 'B'
    src = ('datafiles.chinhphu.vn' if c['nguon'] == 'vanban.chinhphu.vn' else c['nguon']) + ' (toàn văn)'
    cap = {'url': c['nguon_tep'], 'fetched_at': mans[d]['fetched_at'], 'snapshot': c['snapshot'], 'source': src, 'method': c['boc_chu']}
    if c['so_ky_hieu'] in t:
        add.append({'entity': ent, 'field': 'so_ky_hieu', 'value': c['so_ky_hieu'], 'evidence_span': c['so_ky_hieu'], 'extraction': 'verbatim', 'tier': tier, 'capture': cap})
    for m in DATE.finditer(t):
        dd, mo, y = m.groups()
        if f'{y}-{int(mo):02d}-{int(dd):02d}' == c['ngay_ban_hanh']:
            add.append({'entity': ent, 'field': 'ngay_ban_hanh', 'value': c['ngay_ban_hanh'], 'evidence_span': m.group(0), 'extraction': 'normalized', 'tier': tier, 'capture': cap}); break
    dc = c['doi_chieu']
    if dc['so_ky_hieu_toan_van'] == 'khac' and not dc['so_trong_ten_tep']:
        fn_num = re.search(r'0*(\d+)', c['nguon_tep'].rsplit('/', 1)[-1])
        for m in re.finditer(r'Số\s*[:;.]?\s*(\d+\s*/\s*[^\s,;]+)', t):
            if fn_num and re.match(r'^0*(\d+)', m.group(1)).group(1) == fn_num.group(1):
                add.append({'entity': ent, 'field': 'so_ky_hieu', 'value': re.sub(r'\s+', '', m.group(1)), 'evidence_span': m.group(1), 'extraction': 'normalized', 'tier': tier, 'capture': cap, 'note': 'Toàn văn và tên tệp cùng lệch với chỉ mục'}); break
    shutil.copy(f"{S4}/text_snapshots/{c['snapshot']}", os.path.join(snapd, c['snapshot']))
open(os.path.join(D, 'claims.jsonl'), 'w', encoding='utf-8').write(''.join(base) + ''.join(prov) + ''.join(json.dumps(a, ensure_ascii=False) + '\n' for a in add))
ents = set()
for l in open(os.path.join(D, 'claims.jsonl'), encoding='utf-8'): ents.add(json.loads(l)['entity'])
y = open('engine/domains/vbhc_chinhphu/domain.yaml', encoding='utf-8').read()
y = y.replace('domain: vbhc_chinhphu', 'domain: vbhc_v4').replace('entity_label: "Văn bản trên Hệ thống văn bản của Cổng TTĐT Chính phủ, ban hành từ 05/03/2020"', 'entity_label: "Văn bản hành chính và quy phạm từ Cổng TTĐT Chính phủ và cổng 3 tỉnh (Thái Nguyên, Hưng Yên, Quảng Trị), ban hành từ 05/03/2020"')
y = re.sub(r'estimate: \d+', f'estimate: {len(ents)}', y); y = re.sub(r'basis: ".*"', f'basis: "Tổng số dòng chỉ mục từ 4 nguồn chụp ngày 20/11/2026 (Cổng Chính phủ 407 trang, Thái Nguyên 150 trang, Hưng Yên 120 trang, Quảng Trị 43 trang)"', y)
open(os.path.join(D, 'domain.yaml'), 'w', encoding='utf-8').write(y)
print('base', len(base), 'prov', len(prov), 'fulltext', len(add), 'entities', len(ents))
# QĐ-09: loại Giấy phép theo chữ viết tắt GP* trong ký hiệu (áp cho mọi thực thể trong registry)
import re as _re
_p = os.path.join(D, 'claims.jsonl'); _n = 0; _out = []
for l in open(_p, encoding='utf-8'):
    c = json.loads(l)
    if c['field'] == 'loai_van_ban' and _re.match(r'^\s*(?:Số:?\s*)?\d+[a-z]?\s*/\s*GP[A-ZĐ]*\b', c['entity']) and c['value'] != 'Giấy phép':
        c['note'] = (c.get('note', '') + ' Loại gốc theo luật cũ: ' + c['value'] + '; QĐ-09 tách loại Giấy phép theo ký hiệu GP*').strip(); c['value'] = 'Giấy phép'; c['extraction'] = 'inferred' if c.get('extraction') == 'inferred' else 'normalized'; _n += 1
    _out.append(json.dumps(c, ensure_ascii=False) + '\n')
open(_p, 'w', encoding='utf-8').write(''.join(_out)); print('claims loai Giấy phép:', _n)
