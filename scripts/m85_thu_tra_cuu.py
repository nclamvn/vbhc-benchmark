"""M8.5a · Thử biến thể bộ tra cứu trên tập dò 400 văn bản huấn luyện (bỏ chính nó khỏi láng giềng), chỉ chấm bộ đề 41 bài một lần sau khi chọn.
Dùng: python3 scripts/m85_thu_tra_cuu.py '[{}, {\"ro\":1,\"gan_ngay\":24,\"cung_cq\":1.0,\"lam\":0.5}]' [--test]
ro: ưu tiên văn bản nêu thẳng trong trích yếu; gan_ngay: láng giềng gần ngày nặng hơn (tháng); cung_cq: cùng cơ quan; lam: trộn thêm tra theo từ vựng."""
import sys, json, random, math, collections, os
sys.path.insert(0, 'scripts'); os.environ['VBHC_SOT_BAN'] = 'v1.1'
import tra_cuu as T, kiem_trung_thuc as k
DV = json.load(open('m8/dong_vien_dan_c.json', encoding='utf-8')); ids = {d['docid'] for d in DV}
META = {}
for l in open('data/stage4_v7/corpus.jsonl', encoding='utf-8'):
    c = json.loads(l)
    if c['docid'] in ids: META[c['docid']] = (c['ngay_ban_hanh'], c['loai_van_ban'], c.get('co_quan_ky_hieu') or '', c['trich_yeu'])
tc = T.TraCuu(dong_vien_dan='m8/dong_vien_dan_c.json')
tc.meta = [META.get(d['docid']) for d in json.load(open('m8/dong_vien_dan_c.json', encoding='utf-8'))]
rng = random.Random(7); DEV = rng.sample([d for d in DV if d['docid'] in META], 400)
I = k.nap_chi_muc()
TEST = []
DE = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_de.jsonl', encoding='utf-8')}; DA = {json.loads(l)['id']: json.loads(l) for l in open('m3/test_dap_an.jsonl', encoding='utf-8')}
for i, d in DE.items():
    if d['nhiem_vu'] != 'T1': continue
    a = DA[i]['dap_an']; m = T.RE_DE.search(d['de']); ngay = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
    can = {kh for kh, kq in k.kiem_trich_dan(a['van_ban_tham_chieu'], I, a['ngay_ban_hanh'], a['so_ky_hieu_chuan']) if kq == 'dung' and T.QP.match(kh)}
    cq = __import__('re').search(r'Số, ký hiệu: \S+?-(\S+)', d['de']); TEST.append((m.group(4), ngay, a['loai_van_ban'], cq[1] if cq else '', can))

def tim(q_ty, ngay, loai, cq, k_=8, lg=30, lam=0.0, cung_cq=0.0, gan_ngay=0.0, bo=None, ro=0):
    q = set(T.am(q_ty + ' ' + loai)); diem = collections.Counter(); bo_w = T.am(bo) if bo else None
    gan = []
    for j, (w, vd) in enumerate(tc.lang):
        if w == bo_w: continue
        s = tc._bm25(q, w, tc.df2, len(tc.lang), tc.tb2)
        if s <= 0: continue
        mt = tc.meta[j]
        if mt and cung_cq and mt[2] and mt[2] == cq: s *= (1 + cung_cq)
        if mt and gan_ngay: s *= math.exp(-abs((int(mt[0][:4]) * 12 + int(mt[0][5:7])) - (int(ngay[:4]) * 12 + int(ngay[5:7]))) / gan_ngay)
        gan.append((s, vd))
    gan.sort(key=lambda x: -x[0])
    for s, vd in gan[:lg]:
        for kh in vd:
            if kh in tc.ngay and tc.ngay[kh][0] < ngay: diem[kh] += s
    if lam:
        mx = max(diem.values()) if diem else 1
        lex = tc._tim_tu_vung(q, ngay, 20)
        for r, x in enumerate(lex): diem[x[0]] += lam * mx / (r + 2)
    if ro:
        import re
        for m in re.finditer(r'(\d{1,4})/(\d{4})/(NĐ-CP|NQ-CP|QĐ-TTg|QH1[45]|UBTVQH1[45]|TT-[A-ZĐ]+|TTLT-[A-ZĐ-]+)', q_ty):
            kh = k.chuan(m.group(0))
            if kh in tc.ngay and tc.ngay[kh][0] < ngay: diem[kh] += 1e6
    kq = [kh for kh, _ in diem.most_common(k_)]
    if len(kq) < k_:
        for x in tc._tim_tu_vung(q, ngay, k_ * 2):
            if x[0] not in kq: kq.append(x[0])
            if len(kq) == k_: break
    return kq
def do(tap, **kw):
    co = tr = lay = 0
    for q, ngay, loai, cq, can, bo in tap:
        r = set(tim(q, ngay, loai, cq, bo=bo, **kw)); co += len(can); tr += len(can & r); lay += len(r)
    return round(100 * tr / co, 1), round(100 * tr / max(1, lay), 1)
dev = [(META[d['docid']][3], META[d['docid']][0], META[d['docid']][1], META[d['docid']][2], set(d['vien_dan']), META[d['docid']][3]) for d in DEV]
test = [t + (None,) for t in TEST]
if __name__ == '__main__':
    for kw in json.loads(sys.argv[1]):
        print(kw, 'dev phủ/đúng', do(dev, **kw), ('test ' + str(do(test, **kw))) if '--test' in sys.argv else '', flush=True)
