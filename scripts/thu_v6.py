"""Chạy thử mô hình cơ sở pilot (QĐ-17): Qwen3-8B 4-bit + adapter v6, giao thức 2.1
(tư liệu tra cứu + bảng bộ máy theo ngày, phạt lặp 1,1, dừng khi lặp nguyên đoạn, rồi điền số căn cứ tất định).
Dùng trên Mac Apple Silicon có mlx-lm:
  python3 scripts/thu_v6.py              → chạy 3 ví dụ soạn sẵn, lưu kết quả vào ~/Documents/vbhc-ketqua/thu_v6/
  python3 scripts/thu_v6.py --tu-nhap    → tự nhập từng trường như thu_v4.py
Mọi bản nháp phải được người có thẩm quyền rà lại: căn cứ, họ tên, số liệu có thể sai hoặc để trống "…".
"""
import argparse, os, sys, time
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_logits_processors
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chan_lap import khoi_lap
import tra_cuu, dien_can_cu
HE = 'Bạn là trợ lý soạn thảo và rà soát văn bản hành chính Việt Nam theo Nghị định 30/2020/NĐ-CP.'
VI_DU = [  # ba đề mới, không có trong bộ đo, đều sau mốc sáp nhập bộ (03/2025) và bỏ cấp huyện (07/2025)
    ('Quyết định (cá biệt)', 'UBND tỉnh Thái Nguyên', '1520/QĐ-UBND', '15/11/2026',
     'Về việc công bố Danh mục thủ tục hành chính được sửa đổi, bổ sung trong lĩnh vực đất đai thuộc phạm vi chức năng quản lý của Sở Nông nghiệp và Môi trường tỉnh Thái Nguyên'),
    ('Công điện', 'Thủ tướng Chính phủ', '105/CĐ-TTg', '18/11/2026',
     'Về việc tập trung ứng phó với bão số 12 và mưa lũ sau bão tại các tỉnh Trung Bộ'),
    ('Công văn', 'Văn phòng Chính phủ', '9876/VPCP-KTTH', '25/11/2026',
     'V/v đẩy nhanh tiến độ giải ngân vốn đầu tư công năm 2026')]
ap = argparse.ArgumentParser()
ap.add_argument('--model', default='mlx-community/Qwen3-8B-4bit')
ap.add_argument('--adapter', default=os.path.expanduser('~/Documents/vbhc-ketqua/m7b/tot_nhat_v6'))
ap.add_argument('--tu-nhap', action='store_true'); ap.add_argument('--toi-da', type=int, default=1800)
a = ap.parse_args()
if not os.path.exists(os.path.join(a.adapter, 'adapters.safetensors')):
    sys.exit(f'Không thấy adapter ở {a.adapter}. Chạy lại scripts/chay_m7b_mac.sh hoặc chỉ --adapter.')

def de(loai, cq, so, ngay, ty):   # cùng khuôn với bộ đo (m3_dung_bo.de_T1)
    d, m, y = ngay.split('/'); mm = f'{int(m):02d}' if int(m) < 3 else str(int(m))
    return (f'Soạn hoàn chỉnh một văn bản loại "{loai}" đúng thể thức Nghị định 30/2020/NĐ-CP với thông tin sau:\n- Cơ quan ban hành: {cq}\n- Số, ký hiệu: {so}\n'
            f'- Ngày ban hành: ngày {int(d):02d} tháng {mm} năm {y}\n- Trích yếu nội dung: {ty}\nViết đủ các thành phần thể thức và phần nội dung phù hợp với trích yếu. Chỉ trả về văn bản.')

def nhap():
    L = ['Công văn', 'Thông báo', 'Quyết định (cá biệt)', 'Công điện', 'Chỉ thị']
    print('\nLoại văn bản:'); [print(f'  {i + 1}. {x}') for i, x in enumerate(L)]
    loai = L[int(input('Chọn số (1–5): ').strip() or 1) - 1]
    return (loai, input('Cơ quan ban hành: ').strip(), input('Số, ký hiệu: ').strip() or '…',
            input('Ngày ban hành dd/mm/yyyy: ').strip() or '01/12/2026', input('Trích yếu nội dung: ').strip())

print('Đang nạp bộ tra cứu và mô hình (lần đầu khoảng 30 giây)...')
TC = tra_cuu.TraCuu(); model, tok = load(a.model, adapter_path=a.adapter)
xu_ly = make_logits_processors(repetition_penalty=1.1, repetition_context_size=64)
ra = os.path.expanduser(f'~/Documents/vbhc-ketqua/thu_v6/thu_{time.strftime("%Y%m%d_%H%M")}.md'); os.makedirs(os.path.dirname(ra), exist_ok=True)
nhat_ky = [f'# Chạy thử v6 + giao thức 2.1 · {time.strftime("%d/%m/%Y %H:%M")}\n']
ds_de = [nhap()] if a.tu_nhap else VI_DU
for i, v in enumerate(ds_de, 1):
    u = tra_cuu.lam_giau_de(de(*v), TC, 8); ds = tra_cuu.lam_giau_de.ds
    p = tok.apply_chat_template([{'role': 'system', 'content': HE}, {'role': 'user', 'content': u}], add_generation_prompt=True, tokenize=False, enable_thinking=False)
    print(f'\n{"═" * 60}\nVÍ DỤ {i}: {v[0]} · {v[1]} · {v[2]} · {v[3]}\n{v[4]}\nTư liệu tra cứu: {", ".join(x[0] for x in ds) or "(không có)"}\n{"─" * 60}')
    viet, t0, dung = '', time.time(), ''
    for r in stream_generate(model, tok, p, max_tokens=a.toi_da, logits_processors=xu_ly):
        viet += r.text; print(r.text, end='', flush=True)
        if '\n' in r.text and khoi_lap(viet) is not None:
            viet = viet[:khoi_lap(viet)]; dung = '[Đã dừng vì lặp nguyên đoạn; phần sau bị bỏ.]'; print('\n' + dung); break
    dien = dien_can_cu.dien(viet, ds); them = dien != viet
    print(f'\n{"─" * 60}\n{round(time.time() - t0)} giây.' + (' Bước điền đã thêm số, ngày cho căn cứ có trong tư liệu.' if them else ''))
    nhat_ky += [f'\n## Ví dụ {i}: {v[0]} · {v[1]} · {v[2]} · {v[3]}\n\n{v[4]}\n\nTư liệu tra cứu: {", ".join(x[0] for x in ds)}\n\n```\n{dien}\n```\n{dung}\n']
open(ra, 'w', encoding='utf-8').write(''.join(nhat_ky))
print(f'\nĐã lưu cả {len(ds_de)} bài vào {ra}\nBản nháp do máy sinh. Kiểm lại căn cứ, số hiệu, ngày, họ tên và tên cơ quan trước khi dùng.')
