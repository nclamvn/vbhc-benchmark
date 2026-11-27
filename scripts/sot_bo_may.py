"""Đọc sổ SOT bộ máy nhà nước theo thời điểm (sot/bo_may.json) và kiểm sổ trước khi dùng.
Mọi script cần tên bộ, Thủ tướng, cấp chính quyền, tỉnh theo ngày đều đọc từ đây (bộ chấm, bộ tra cứu, dữ liệu huấn luyện).
Dùng: python3 scripts/sot_bo_may.py          → kiểm sổ (thoát mã 2 nếu có lỗi), in tóm tắt
      python3 scripts/sot_bo_may.py 2026-05-01 → in bộ máy tại ngày đó
"""
import json, os, sys, lzma, csv, re
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_S = None

def so(p=None):
    global _S
    if _S is None or p: _S = json.load(open(p or os.path.join(GOC, 'sot', 'bo_may.json'), encoding='utf-8'))
    return _S

def _con(r, ngay): return (r['tu'] is None or r['tu'] <= ngay) and (r['den'] is None or ngay <= r['den'])
def _loc(loai, ngay): return [r for r in so()['ban_ghi'] if r['loai'] == loai and _con(r, ngay)]
def _xep(loai, ngay):
    k = 'moi' if ngay >= '2025-03-01' else 'cu'
    return [r['ten'] for r in sorted(_loc(loai, ngay), key=lambda r: r['thu_tu'][k])]
def bo(ngay): return _xep('bo', ngay)
def ngang_bo(ngay): return _xep('co_quan_ngang_bo', ngay)
def thu_tuong(ngay):
    t = _loc('thu_tuong', ngay); return t[0]['ten'] if t else None
def pho_thu_tuong(ngay): return [r['ten'] for r in _loc('pho_thu_tuong', ngay)]
def cap_chinh_quyen(ngay): return _loc('cap_chinh_quyen', ngay)[0]['ten']
def tinh_34(ngay): return [r['ten'] for r in _loc('tinh_34', ngay)]
def thanh_pho_tw(ngay): return [r['ten'] for r in _loc('thanh_pho_tw', ngay)]
def tinh_da_len_thanh_pho(ngay):
    """Tên các đơn vị đã từ tỉnh lên thành phố trực thuộc trung ương tại ngày đó (gọi 'tỉnh X' sau mốc là sai thời điểm)."""
    return [r['ten'] for r in so()['ban_ghi'] if r['loai'] == 'thanh_pho_tw' and r['tu'] and r['tu'] >= '2026-01-01' and ngay >= r['tu']]
def nhiem_ky_thu_tuong(): return [(r['ten'], r['tu'], r['den']) for r in so()['ban_ghi'] if r['loai'] == 'thu_tuong']
def ten_bo_da_doi(ngay):
    """Tên đầy đủ (kèm biến thể) của các bộ, cơ quan ngang bộ đã không còn tại ngày đó."""
    out = []
    for r in so()['ban_ghi']:
        if r['loai'] in ('bo', 'co_quan_ngang_bo') and r['den'] and ngay > r['den']:
            tien = 'Bộ ' if r['loai'] == 'bo' else ''
            out += [tien + x for x in [r['ten']] + r.get('bien_the', [])]
    return out
def tinh_cu(ngay): return [r['ten'] for r in so()['ban_ghi'] if r['loai'] == 'tinh_cu' and r['den'] and ngay > r['den']]

def kiem(p=None):
    """Cổng kiểm sổ. Trả về danh sách lỗi; rỗng là đạt."""
    S = so(p); L = []; ids = set()
    I = {r['so_ky_hieu_chuan'] for r in csv.DictReader(lzma.open(os.path.join(GOC, 'm3', 'chi_muc_kiem_trung_thuc.csv.xz'), 'rt', encoding='utf-8'))}
    for r in S['ban_ghi']:
        if r['id'] in ids: L.append('TRUNG_ID ' + r['id'])
        ids.add(r['id'])
        for k in ('tu', 'den'):
            if r[k] is not None and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', r[k]): L.append(f'NGAY_SAI {r["id"]} {k}')
        if r['tu'] and r['den'] and r['tu'] > r['den']: L.append('TU_SAU_DEN ' + r['id'])
        m = r.get('muc_xac_minh')
        if m not in S['quy_uoc']['muc_xac_minh']: L.append('MUC_XAC_MINH_LA ' + r['id'])
        if m in ('chi_muc', 'chi_muc_can_doi_chieu') and r.get('can_cu') not in I: L.append(f'CAN_CU_KHONG_CO_TRONG_CHI_MUC {r["id"]} {r.get("can_cu")}')
        if m == 'nguon_web' and not str(r.get('nguon', '')).startswith('https://'): L.append('THIEU_NGUON ' + r['id'])
        if r.get('nay_la') and not any(x['ten'] == r['nay_la'] and x['loai'] in ('bo', 'co_quan_ngang_bo') for x in S['ban_ghi']): L.append('NAY_LA_KHONG_CO ' + r['id'])
    nk = sorted(nhiem_ky_thu_tuong(), key=lambda x: x[1] or '')
    for (a, _, d1), (b, t2, _) in zip(nk, nk[1:]):
        if d1 is None or t2 is None or d1 >= t2: L.append(f'NHIEM_KY_CHONG {a}/{b}')
    for ngay in ('2020-06-01', '2025-01-15', '2025-03-01', '2025-07-01', '2026-05-01'):
        if len(_loc('cap_chinh_quyen', ngay)) != 1: L.append('CAP_CHINH_QUYEN_KHONG_DUY_NHAT ' + ngay)
    if len(bo('2025-03-01')) != 14 or len(bo('2025-02-28')) != 18: L.append('SO_BO_SAI')
    if len(tinh_34('2025-07-01')) != 34: L.append('SO_TINH_SAI')
    return L

if __name__ == '__main__':
    if len(sys.argv) > 1:
        n = sys.argv[1]; print(json.dumps({'bo': bo(n), 'ngang_bo': ngang_bo(n), 'thu_tuong': thu_tuong(n), 'pho_thu_tuong': pho_thu_tuong(n), 'cap': cap_chinh_quyen(n), 'so_tinh': len(tinh_34(n)) or None}, ensure_ascii=False, indent=1))
        sys.exit(0)
    L = kiem(); S = so()
    from collections import Counter
    print(f"{S['ten']} {S['phien_ban']}: {len(S['ban_ghi'])} bản ghi; mức xác minh {dict(Counter(r['muc_xac_minh'] for r in S['ban_ghi']))}")
    if L: print('LỖI:', *L, sep='\n  '); sys.exit(2)
    print('ĐẠT: sổ hợp lệ')
