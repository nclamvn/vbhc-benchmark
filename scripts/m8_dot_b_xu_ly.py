"""M8.2 · Xử lý đợt cào B theo lớp 2–3 của bộ tiêu chuẩn (QĐ-18), rồi ghép vào kho.
Mỗi văn bản: bóc lớp chữ PDF nếu lớp chữ tốt, không thì OCR đủ trang (Tesseract vie 200 dpi); bỏ văn bản > 12 trang (phần lớn là phụ lục bảng biểu).
Làm sạch và che như kho v4 (strip_stamp, redact, redact_person của reconcile_clean_v4); đối chiếu với chỉ mục (trích yếu, số ký hiệu, ngày);
loại: trùng tệp, mất dấu, độ tin OCR < 70, trích yếu gần trùng một văn bản của bộ đo; 10 văn bản mới nhất để riêng cho bộ đề mới (M8.6).
Dùng:
  python3 scripts/m8_dot_b_xu_ly.py boc <giây>   → data/dot_b/text/<docid>.json (tiếp tục được)
  python3 scripts/m8_dot_b_xu_ly.py ghep         → data/stage4_v6/corpus.jsonl (kho v5 + đợt B), m8/chia_tap_dot_b.json, data/dot_b/bao_cao.json
"""
import json, os, re, sys, ast, time, subprocess, tempfile, csv, collections, unicodedata
from concurrent.futures import ThreadPoolExecutor
D = 'data/dot_b'; os.makedirs(f'{D}/text', exist_ok=True)
src = open('scripts/reconcile_clean_v4.py', encoding='utf-8').read(); G = {'re': re, 'unicodedata': unicodedata}
for node in ast.parse(src).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('nfc', 'chuan', 'la_can_bo', 'redact_person', 'redact', 'strip_stamp', 'toks'):
        exec(ast.get_source_segment(src, node), G)
    elif isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('EMAIL', 'PHONE', 'KEY', 'NAMEW', 'HON', 'CHUC', 'SAU', 'TRUOC', 'ADDR', 'IDNO', 'DOB', 'DATE', 'STAMP', 'STAMP2', 'INLINE', 'VI', 'STOPW'):
        exec(ast.get_source_segment(src, node), G)
nfc = G['nfc']; VI = G['VI']; STOPW = G.get('STOPW', set())

# quyết định nhân sự về một người cụ thể (chỉ định, giao, cử, tiếp nhận, đình chỉ, thôi giữ chức...): ít giá trị cho soạn văn bản, có yếu tố cá nhân
NHAN_SU = re.compile(r'chỉ định (ông|bà)|\b(cử|giao|tiếp nhận|điều động|cho thôi|thôi giữ chức|đình chỉ|tạm đình chỉ)\s+(ông|bà)\b|về việc (ông|bà)\s+[A-ZĐ]|đối với (\d+\s+)?(ông|bà)\s+[A-ZĐ]', re.I)
def trang(p):
    out = subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout
    m = re.search(r'Pages:\s+(\d+)', out); return int(m.group(1)) if m else 0
def ocr(p, i):
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, 'p')
        subprocess.run(['pdftoppm', '-r', '200', '-f', str(i), '-l', str(i), '-gray', p, base], timeout=180, check=True)
        img = next(f for f in os.listdir(tmp) if f.endswith('.pgm'))
        subprocess.run(['tesseract', os.path.join(tmp, img), base + 'o', '-l', 'vie', '--psm', '4', 'txt', 'tsv'], capture_output=True, timeout=300)
        txt = open(base + 'o.txt', encoding='utf-8').read(); cf = []
        for row in csv.DictReader(open(base + 'o.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
            try:
                c = float(row['conf'])
                if c >= 0 and row['text'].strip(): cf.append(c)
            except Exception: pass
    return {'page': i, 'text': txt, 'conf': round(sum(cf) / len(cf), 1) if cf else 0.0}
def lop_chu_tot(t, n):
    letters = len(re.findall(r'[A-Za-zÀ-ỹ]', t)) or 1
    return len(t.strip()) >= 200 * n and len(VI.findall(t)) / letters >= 0.06

def boc(han):
    mf = [json.loads(l) for l in open(f'{D}/manifest.jsonl', encoding='utf-8')]
    t0 = time.time(); n = 0
    with ThreadPoolExecutor(2) as ex:
        for r in mf:
            if time.time() - t0 > han: break
            f = f'{D}/text/{r["docid"]}.json'
            if not r.get('file') or os.path.exists(f): continue
            p = 'data/raw_pdf/' + r['file']; tp = trang(p); rec = {'docid': r['docid'], 'pages_total': tp, 'sha256': r['sha256']}
            if tp == 0 or tp > 12: rec.update(method='bo_qua', ly_do='qua_12_trang' if tp else 'khong_doc_duoc_pdf')
            else:
                lop = [subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), p, '-'], capture_output=True, text=True).stdout for i in range(1, tp + 1)]
                if lop_chu_tot(''.join(lop), tp): rec.update(method='text_layer', pages=[{'page': i + 1, 'text': x, 'conf': None} for i, x in enumerate(lop)])
                else: rec.update(method='ocr_vie', pages=list(ex.map(lambda i: ocr(p, i), range(1, tp + 1))))
            json.dump(rec, open(f, 'w', encoding='utf-8'), ensure_ascii=False); n += 1
    con = sum(1 for r in mf if r.get('file') and not os.path.exists(f'{D}/text/{r["docid"]}.json'))
    print(f'bóc lượt này {n}; còn {con} trong số đã tải ({len(mf)})', flush=True)

def ghep():
    kh = {r['docid']: r for r in json.load(open(f'{D}/ke_hoach.json', encoding='utf-8'))}
    kho = [json.loads(l) for l in open('data/stage4_v5/corpus.jsonl', encoding='utf-8')]
    sha_co = {c.get('sha256_tep') for c in kho}
    DA = [json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')]; byid = {c['docid']: c for c in kho}
    test_ty = [G['toks'](byid[d['docid']]['trich_yeu']) for d in DA if d['docid'] in byid]
    BC = collections.Counter(); moi = []
    for f in sorted(os.listdir(f'{D}/text')):
        r = json.load(open(f'{D}/text/{f}', encoding='utf-8')); m = kh[r['docid']]
        if r['method'] == 'bo_qua': BC['loai_' + r['ly_do']] += 1; continue
        if NHAN_SU.search(m['trich_yeu']) or NHAN_SU.search(r['pages'][0]['text'][:1500]): BC['loai_nhan_su_ca_nhan'] += 1; continue
        if r['sha256'] in sha_co: BC['loai_trung_tep'] += 1; continue
        sha_co.add(r['sha256'])
        cf = [p['conf'] for p in r['pages'] if p.get('conf') is not None]; mconf = round(sum(cf) / len(cf), 1) if cf else None
        if mconf is not None and mconf < 70: BC['loai_do_tin_ocr'] += 1; continue
        text = nfc('\n\f\n'.join(p['text'] for p in r['pages']))
        text, n_st = G['strip_stamp'](text); red, n_e, n_p = G['redact'](text); red, pc = G['redact_person'](red)
        letters = len(re.findall(r'[A-Za-zÀ-ỹ]', red[:20000])) or 1
        if len(VI.findall(red[:20000])) / letters < 0.06: BC['loai_mat_dau'] += 1; continue
        tt = G['toks'](m['trich_yeu']) - STOPW; head = G['toks'](red[:6000]); trung = round(len(tt & head) / len(tt), 2) if tt else 1.0
        if any(len(tt & x) / max(1, len(tt | x)) >= 0.8 for x in test_ty): BC['loai_gan_trung_bo_do'] += 1; continue
        kc = G['chuan'](m['so_ky_hieu']); phang = re.sub(r'\s+', '', red[:3000])
        so = 'khop' if kc in G['chuan'](phang) else ('gan_khop' if kc.split('/')[0] in phang else 'khong_doc_duoc')
        y, mo, dd = m['ngay_ban_hanh'].split('-')
        ngay = any(f'{y}-{int(a2):02d}-{int(a1):02d}' == m['ngay_ban_hanh'] for a1, a2, _ in G['DATE'].findall(red[:3000]))
        moi.append({'docid': m['docid'], 'so_ky_hieu': m['so_ky_hieu'], 'so_ky_hieu_chuan': kc, 'gan_trung_mau_voi': [], 'cho_xac_minh': None,
                    'ngay_ban_hanh': m['ngay_ban_hanh'], 'trich_yeu': m['trich_yeu'], 'loai_van_ban': m['loai_van_ban'], 'hinh_thuc': m['hinh_thuc'],
                    'co_quan_ky_hieu': m['co_quan_ky_hieu'], 'nguon': 'vanban.chinhphu.vn', 'cap': 'Trung ương', 'co_quan_ten': '',
                    'thoi_ky': 'từ 01/7/2025' if m['ngay_ban_hanh'] >= '2025-07-01' else 'trước 01/7/2025',
                    'nguon_chi_muc': f'https://vanban.chinhphu.vn/?pageid=27160&docid={m["docid"]}', 'nguon_tep': m['tep'][0], 'sha256_tep': r['sha256'],
                    'boc_chu': r['method'], 'trang_da_boc': list(range(1, r['pages_total'] + 1)), 'tong_so_trang': r['pages_total'], 'do_tin_ocr': mconf,
                    'da_che': str({'email': n_e, 'so_dien_thoai': n_p, **pc}), 'doi_chieu': {'nguoi_kiem_xac_nhan': None, 'trung_trich_yeu': trung,
                    'so_ky_hieu_toan_van': so, 'ngay_ban_hanh_toan_van': ngay}, 'dong_dau_cong_da_bo': n_st, 'dot_cao': 'M8.2-B', 'text': red})
        BC['nhan'] += 1
    moi.sort(key=lambda c: (c['ngay_ban_hanh'], c['docid']))
    de_moi = {c['docid'] for c in moi[-10:]}
    CT = {c['docid']: ('de_moi' if c['docid'] in de_moi else 'train') for c in moi}
    os.makedirs('data/stage4_v6', exist_ok=True); os.makedirs('m8', exist_ok=True)
    open('data/stage4_v6/corpus.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in kho + moi))
    json.dump(CT, open('m8/chia_tap_dot_b.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump({**BC, 'de_moi': sorted(de_moi)}, open(f'{D}/bao_cao.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(kho), '+', len(moi), dict(BC))

if __name__ == '__main__':
    {'boc': lambda: boc(float(sys.argv[2]) if len(sys.argv) > 2 else 540), 'ghep': ghep}[sys.argv[1]]()
