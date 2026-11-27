"""M8.4 · Xử lý đợt cào C (cổng tỉnh) theo lớp 2–3, dùng chung các hàm của đợt B (scripts/m8_dot_b_xu_ly.py).
Khác đợt B: chỉ mục lấy từ chính danh sách cổng tỉnh; loại văn bản kiểm lại theo ký hiệu (KH, CT, BC) để tránh dòng lọt loại;
cơ quan ban hành đọc từ cột "Cơ quan ban hành" của cổng.
Dùng:
  python3 scripts/m8_dot_c_xu_ly.py boc qn <giây>   → data/dot_c/qn/text/<docid>.json
  python3 scripts/m8_dot_c_xu_ly.py ghep            → data/stage4_v7/corpus.jsonl (kho v6 + đợt C), m8/chia_tap_dot_c.json, data/dot_c/bao_cao.json
"""
import json, os, re, sys, time, collections, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m8_dot_b_xu_ly as B
G, VI, nfc, STOPW, NHAN_SU = B.G, B.VI, B.nfc, B.STOPW, B.NHAN_SU
KY = {'Kế hoạch': r'/KH[-.]', 'Chỉ thị': r'/CT[-.]', 'Báo cáo': r'/BC[-.]'}
NGUON = {'qn': ('data/dot_c/qn', 'quangninh.gov.vn', 'Quảng Ninh'), 'lc': ('data/dot_c/lc', 'laichau.gov.vn', 'Lai Châu')}
KHOA = {'qn': 'vbId', 'lc': 'id'}

CAP_DV = r'(TỈNH|THÀNH PHỐ|HUYỆN|THỊ XÃ|THỊ TRẤN|ĐẶC KHU|PHƯỜNG|XÃ)'
def co_quan_dau(red):
    """Tên UBND đọc từ phần đầu văn bản (dòng dưới 'ỦY BAN NHÂN DÂN'); cổng tỉnh ghi cơ quan theo đơn vị đăng, không theo đơn vị ban hành."""
    m = re.search(r'(?:ỦY|UỶ) BAN NHÂN DÂN[^\n]*\n\s*' + CAP_DV + r'\s+([A-ZÀ-ỸĐ][A-ZÀ-ỸĐ ]{1,30}?)(?=\s{2,}|\s*Độc|\s*\n)', red[:800].upper())
    if not m: return None
    return 'UBND ' + m[1].lower() + ' ' + ' '.join(w.capitalize() for w in m[2].split())

def boc(ma, han):
    D = NGUON[ma][0]; os.makedirs(f'{D}/text', exist_ok=True)
    mf = [json.loads(l) for l in open(f'{D}/manifest.jsonl', encoding='utf-8') if json.loads(l).get('file')]
    t0 = time.time(); n = 0
    with ThreadPoolExecutor(2) as ex:
        for r in mf:
            if time.time() - t0 > han: break
            docid = f'{ma}-{r[KHOA[ma]]}'; f = f'{D}/text/{docid}.json'
            if os.path.exists(f): continue
            p = 'data/raw_pdf/' + r['file']; tp = B.trang(p); rec = {'docid': docid, 'pages_total': tp, 'sha256': r['sha256']}
            if tp == 0 or tp > 12: rec.update(method='bo_qua', ly_do='qua_12_trang' if tp else 'khong_doc_duoc_pdf')
            else:
                lop = [subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), p, '-'], capture_output=True, text=True).stdout for i in range(1, tp + 1)]
                if B.lop_chu_tot(''.join(lop), tp): rec.update(method='text_layer', pages=[{'page': i + 1, 'text': x, 'conf': None} for i, x in enumerate(lop)])
                else: rec.update(method='ocr_vie', pages=list(ex.map(lambda i: B.ocr(p, i), range(1, tp + 1))))
            json.dump(rec, open(f, 'w', encoding='utf-8'), ensure_ascii=False); n += 1
    print(f'bóc lượt này {n}', flush=True)

def ghep():
    kho = [json.loads(l) for l in open('data/stage4_v6/corpus.jsonl', encoding='utf-8')]
    sha_co = {c.get('sha256_tep') for c in kho}; byid = {c['docid']: c for c in kho}
    test_ty = [G['toks'](byid[json.loads(l)['docid']]['trich_yeu']) for l in open('m3/test_dap_an.jsonl', encoding='utf-8') if json.loads(l)['docid'] in byid]
    BC = collections.Counter(); moi = []
    for ma, (D, nguon, tinh) in NGUON.items():
        if not os.path.isdir(f'{D}/text'): continue
        cm = {f'{ma}-{json.loads(l)[KHOA[ma]]}': json.loads(l) for l in open(f'{D}/chi_muc.jsonl', encoding='utf-8')}
        for f in sorted(os.listdir(f'{D}/text')):
            r = json.load(open(f'{D}/text/{f}', encoding='utf-8')); m = cm[r['docid']]
            if r['method'] == 'bo_qua': BC['loai_' + r['ly_do']] += 1; continue
            if not re.search(KY[m['loai_van_ban']], m['so_ky_hieu']): BC['loai_ky_hieu_khong_khop_loai'] += 1; continue
            if re.search(r'[-/](TU|HU|ĐU|BCĐ)\b', m['so_ky_hieu']) or 'ủy' in (m['co_quan_ten'] or '').lower() and 'UBND' not in (m['co_quan_ten'] or ''): BC['loai_van_ban_dang'] += 1; continue   # văn bản Đảng theo HD 36, không theo NĐ 30
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
            ngay = any(f'{y}-{int(a2):02d}-{int(a1):02d}' == m['ngay_ban_hanh'] for a1, a2, y in G['DATE'].findall(red[:3000]))
            moi.append({'docid': r['docid'], 'so_ky_hieu': m['so_ky_hieu'], 'so_ky_hieu_chuan': kc, 'gan_trung_mau_voi': [], 'cho_xac_minh': None,
                        'ngay_ban_hanh': m['ngay_ban_hanh'], 'trich_yeu': m['trich_yeu'], 'loai_van_ban': m['loai_van_ban'], 'hinh_thuc': 'Hành chính',
                        'co_quan_ky_hieu': (re.search(r'/[A-ZĐa-z]+-([A-ZĐ]+)', m['so_ky_hieu']) or re.search(r'-(\w+)', m['so_ky_hieu']) or [None, ''])[1],
                        'nguon': nguon, 'cap': 'Tỉnh' if re.search(r'(TỈNH|THÀNH PHỐ)\s+' + r'\s+'.join(tinh.upper().split()), red[:600].upper()) else 'Dưới tỉnh', 'co_quan_ten': co_quan_dau(red) or m['co_quan_ten'] or f'UBND {tinh}',
                        'thoi_ky': 'từ 01/7/2025' if m['ngay_ban_hanh'] >= '2025-07-01' else 'trước 01/7/2025',
                        'nguon_chi_muc': m['chi_tiet'], 'nguon_tep': m['tep'], 'sha256_tep': r['sha256'], 'boc_chu': r['method'],
                        'trang_da_boc': list(range(1, r['pages_total'] + 1)), 'tong_so_trang': r['pages_total'], 'do_tin_ocr': mconf,
                        'da_che': str({'email': n_e, 'so_dien_thoai': n_p, **pc}), 'doi_chieu': {'nguoi_kiem_xac_nhan': None, 'trung_trich_yeu': trung,
                        'so_ky_hieu_toan_van': so, 'ngay_ban_hanh_toan_van': ngay}, 'dong_dau_cong_da_bo': n_st, 'dot_cao': 'M8.4-C-' + ma, 'text': red})
            BC['nhan:' + m['loai_van_ban']] += 1
    moi.sort(key=lambda c: (c['ngay_ban_hanh'], c['docid']))
    CT = json.load(open('m8/chia_tap_dot_b.json', encoding='utf-8'))
    CT.update({c['docid']: 'train' for c in moi}); CT.update({c['docid']: 'de_moi' for c in moi[-10:]})   # 10 văn bản mới nhất để ngoài huấn luyện (cho bộ đề M8.6)
    os.makedirs('data/stage4_v7', exist_ok=True)
    open('data/stage4_v7/corpus.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in kho + moi))
    json.dump(CT, open('m8/chia_tap_dot_c.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(dict(BC), open('data/dot_c/bao_cao.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(kho), '+', len(moi), dict(BC))
    import random; mau = random.Random(20261127).sample(moi, min(100, len(moi)))
    dong = ['# Mẫu kiểm tay thông tin cá nhân · đợt cào C (M8.4)', '',
            f'100 văn bản chọn ngẫu nhiên (hạt giống 20261127) trong {len(moi)} văn bản đợt C (Quảng Ninh, Lai Châu). Mỗi dòng: mở bản gốc, đối chiếu với bản đã che trong kho v7 '
            '(`data/stage4_v7/corpus.jsonl`, tìm theo mã). Đánh dấu nếu còn họ tên người dân, địa chỉ, số định danh, số điện thoại, ngày sinh. Họ tên cán bộ đi cùng chức vụ được giữ (QĐ-03, QĐ-09).', '',
            '| # | Mã | Loại | Ngày | Trích yếu | Bản gốc | Còn thông tin cá nhân? |', '|---|---|---|---|---|---|---|']
    dong += [f"| {i} | {c['docid']} | {c['loai_van_ban']} | {c['ngay_ban_hanh']} | {c['trich_yeu'][:70].replace('|', '/')} | [mở]({c['nguon_tep']}) | ☐ |" for i, c in enumerate(mau, 1)]
    open('ket_qua/dot_cao/mau_kiem_tay_dot_c.md', 'w', encoding='utf-8').write('\n'.join(dong) + '\n')

if __name__ == '__main__':
    if sys.argv[1] == 'boc': boc(sys.argv[2], float(sys.argv[3]))
    else: ghep()
