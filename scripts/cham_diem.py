"""Chấm điểm VBHC-Bench bản pilot. Dùng: python3 scripts/cham_diem.py <tệp trả lời .jsonl> [tệp đáp án]
Tệp trả lời: mỗi dòng {"id": ..., "tra_loi": "<chuỗi mô hình trả về>"}.
T2: đúng mã lỗi. T3: số ký hiệu, ngày, loại khớp tuyệt đối; trích yếu tính F1 theo từ. T1: phần máy chấm được (thể thức, đúng số, ngày, bám trích yếu);
phần chất lượng nội dung của T1 cần người chấm theo hướng dẫn chấm, không nằm trong điểm này."""
import json, re, sys, unicodedata, collections
sys.path.insert(0, 'scripts'); import the_thuc_nd30 as v1, the_thuc_nd30_v2 as v2
def nfc(s): return unicodedata.normalize('NFC', s or '')
def lay_json(s):
    for m in re.finditer(r'\{[^{}]*\}', s or '', re.S):
        try: return json.loads(m.group(0))
        except Exception: pass
    return {}
def ch(s): return re.sub(r'[\s.]+$', '', re.sub(r'\s+', '', nfc(str(s)).replace('Ð', 'Đ'))).upper()
def tu(s): return re.findall(r'[a-zà-ỹđ0-9]+', nfc(str(s)).lower())
def f1(a, b):
    A, B = collections.Counter(tu(a)), collections.Counter(tu(b)); g = sum((A & B).values())
    return 0.0 if not g else 2 * g / (sum(A.values()) + sum(B.values()))
def cham(tl, G):
    nv, g, s = G['nhiem_vu'], G['dap_an'], tl or ''
    if nv == 'T2': return {'dung': float(str(lay_json(s).get('loi', '')).strip() == g['loi'])}
    if nv == 'T3':
        j = lay_json(s)
        r = {'so_ky_hieu': float(ch(j.get('so_ky_hieu', '')) == ch(g['so_ky_hieu'])), 'ngay_ban_hanh': float(str(j.get('ngay_ban_hanh', '')).strip() == g['ngay_ban_hanh']),
             'loai_van_ban': float(nfc(str(j.get('loai_van_ban', ''))).strip() == g['loai_van_ban']), 'trich_yeu': f1(j.get('trich_yeu', ''), g['trich_yeu'])}
        r['diem'] = sum(r.values()) / 4; return r
    if len(s.strip()) < 200: return {'the_thuc': 0.0, 'dung_so': 0.0, 'dung_ngay': 0.0, 'bam_trich_yeu': 0.0, 'do_dai_hop_ly': 0.0, 'diem': 0.0, 'luat_sai': ['QUA_NGAN']}
    d = {'text': s, 'so_ky_hieu_chuan': g['so_ky_hieu_chuan'], 'loai_van_ban': g['loai_van_ban']}
    k = v2.kiem(d); y, m, dd = g['ngay_ban_hanh'].split('-')
    r = {'the_thuc': sum(1 for x in k.values() if not x) / len(k), 'dung_so': float(ch(g['so_ky_hieu_chuan']) in ch(v1.vung_dau(nfc(s)))),
         'dung_ngay': float(bool(re.search(rf'ngày\s+0?{int(dd)}\s+tháng\s+0?{int(m)}\s+năm\s+{y}', v1.vung_dau(nfc(s))))),
         'bam_trich_yeu': (lambda a, b: len(a & b) / len(a) if a else 0.0)(set(tu(g['trich_yeu'])), set(tu(s))), 'do_dai_hop_ly': float(600 <= len(s) <= 12000)}
    r['diem'] = sum(r.values()) / 5; r['luat_sai'] = sorted(x for x, e in k.items() if e); return r
if __name__ == '__main__':
    G = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2] if len(sys.argv) > 2 else 'm3/test_dap_an.jsonl', encoding='utf-8')}
    P = {json.loads(l)['id']: json.loads(l).get('tra_loi', '') for l in open(sys.argv[1], encoding='utf-8')}
    R = {i: cham(P.get(i, ''), g) for i, g in G.items()}; out = {'so_muc': len(G), 'thieu_tra_loi': sum(i not in P for i in G)}
    for nv in ['T1', 'T2', 'T3']:
        rs = [R[i] for i in G if G[i]['nhiem_vu'] == nv]
        if not rs: continue
        keys = [k for k in rs[0] if k != 'luat_sai']; out[nv] = {'n': len(rs), **{k: round(100 * sum(r[k] for r in rs) / len(rs), 1) for k in keys}}
    if 'T2' in out:
        bk = collections.defaultdict(list)
        for i in G:
            if G[i]['nhiem_vu'] == 'T2': bk[G[i]['dap_an']['loi']].append(R[i]['dung'])
        out['T2']['theo_ma'] = {k: round(100 * sum(v) / len(v)) for k, v in sorted(bk.items())}
    out['tong_hop'] = round(sum(out[nv].get('diem', out[nv].get('dung')) for nv in ['T1', 'T2', 'T3'] if nv in out) / sum(nv in out for nv in ['T1', 'T2', 'T3']), 1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    json.dump({'tong': out, 'tung_muc': R}, open(sys.argv[1].replace('.jsonl', '') + '_diem.json', 'w', encoding='utf-8'), ensure_ascii=False)
