"""M8.1b · Kho v5 = kho v4 + các văn bản đã OCR đủ trang (data/text_du_trang). Không cào mạng.
Với mỗi văn bản đã bù: ghép trang cũ (data/text/<docid>.json) với trang mới theo số trang, rồi làm sạch và che y như kho v4
(strip_stamp, redact liên lạc, redact_person của scripts/reconcile_clean_v4.py), đặt trang_da_boc đủ trang.
Văn bản mất dấu hoặc độ tin OCR trung bình < 70 sau khi ghép thì giữ bản v4 (không thay).
Dùng: python3 scripts/m8_kho_v5.py → data/stage4_v5/corpus.jsonl, data/stage4_v5/bao_cao_bu_trang.json
"""
import json, os, re, ast, unicodedata, collections
src = open('scripts/reconcile_clean_v4.py', encoding='utf-8').read(); G = {'re': re, 'unicodedata': unicodedata}
for node in ast.parse(src).body:   # chỉ lấy các hàm và biểu thức chính quy làm sạch, che (không chạy phần đọc dữ liệu ở đầu tệp)
    if isinstance(node, ast.FunctionDef) and node.name in ('nfc', 'la_can_bo', 'redact_person', 'redact', 'strip_stamp'):
        exec(ast.get_source_segment(src, node), G)
    elif isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') in ('EMAIL', 'PHONE', 'KEY', 'NAMEW', 'HON', 'CHUC', 'SAU', 'TRUOC', 'ADDR', 'IDNO', 'DOB', 'DATE', 'STAMP', 'STAMP2', 'INLINE', 'VI'):
        exec(ast.get_source_segment(src, node), G)
VI = G.get('VI') or re.compile(r'[ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ]', re.I)
IN = os.environ.get('VBHC_TOAN_VAN', 'data/stage4_v4/corpus.jsonl'); OUTD = 'data/stage4_v5'; os.makedirs(OUTD, exist_ok=True)
BC = collections.Counter(); out = []
for l in open(IN, encoding='utf-8'):
    c = json.loads(l); f = f'data/text_du_trang/{c["docid"]}.json'
    if os.path.exists(f):
        moi = json.load(open(f, encoding='utf-8')); cu = json.load(open(f'data/text/{c["docid"]}.json', encoding='utf-8'))
        trang = {p['page']: p for p in cu['pages'] if isinstance(p, dict)}; trang.update({p['page']: p for p in moi['trang_moi']})
        ps = [trang[i] for i in sorted(trang)]
        if sorted(trang) != list(range(1, moi['pages_total'] + 1)): BC['thieu_trang_sau_ghep'] += 1; out.append(c); continue
        cf = [p['conf'] for p in ps if p.get('conf') is not None]; mconf = sum(cf) / len(cf) if cf else 100
        text = G['nfc']('\n\f\n'.join(p['text'] for p in ps))
        text, n_stamp = G['strip_stamp'](text); red, n_e, n_p = G['redact'](text); red, pc = G['redact_person'](red)
        letters = len(re.findall(r'[A-Za-zÀ-ỹ]', red[:20000])) or 1
        if mconf < 70 or len(VI.findall(red[:20000])) / letters < 0.06: BC['giu_v4_vi_ocr_kem'] += 1; out.append(c); continue
        c = dict(c, text=red, trang_da_boc=list(range(1, moi['pages_total'] + 1)), do_tin_ocr=round(mconf, 1), bu_trang_m8=len(moi['trang_moi']),
                 da_che=str({'email': n_e, 'so_dien_thoai': n_p, **pc}), dong_dau_cong_da_bo=n_stamp)
        BC['da_bu'] += 1; BC['che_ho_ten_nguoi_dan'] += pc.get('ho_ten', 0); BC['che_sdt_email'] += n_e + n_p
    out.append(c)
open(f'{OUTD}/corpus.jsonl', 'w', encoding='utf-8').write(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in out))
json.dump(dict(BC), open(f'{OUTD}/bao_cao_bu_trang.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), dict(BC))
