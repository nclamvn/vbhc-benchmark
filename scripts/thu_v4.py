"""Chạy thử mô hình cơ sở của pilot: Qwen3-8B 4-bit + adapter v4, giải mã theo giao thức 1.2 (phạt lặp 1,1, cửa sổ 64).
Dùng trên Mac Apple Silicon có mlx-lm:
  python3 scripts/thu_v4.py                         → hỏi từng trường rồi soạn văn bản (T1)
  python3 scripts/thu_v4.py --tu-do                 → gõ lời yêu cầu tự do (ngoài khuôn bộ đo, chất lượng không được đo)
  python3 scripts/thu_v4.py --adapter <thư mục>     → mặc định ~/Documents/vbhc-ketqua/m6b/tot_nhat_v4
Lưu ý: mô hình vẫn có thể bịa căn cứ, họ tên, ngày ban hành văn bản viện dẫn. Mọi bản nháp phải được người có thẩm quyền rà lại.
"""
import argparse, os, sys
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_logits_processors
HE = 'Bạn là trợ lý soạn thảo và rà soát văn bản hành chính Việt Nam theo Nghị định 30/2020/NĐ-CP.'   # trùng lời hệ thống lúc huấn luyện
LOAI = ['Công văn', 'Thông báo', 'Quyết định (cá biệt)', 'Công điện', 'Chỉ thị']
ap = argparse.ArgumentParser()
ap.add_argument('--model', default='mlx-community/Qwen3-8B-4bit')
ap.add_argument('--adapter', default=os.path.expanduser('~/Documents/vbhc-ketqua/m6b/tot_nhat_v4'))
ap.add_argument('--tu-do', action='store_true'); ap.add_argument('--toi-da', type=int, default=1800)
a = ap.parse_args()
if not os.path.exists(os.path.join(a.adapter, 'adapters.safetensors')):
    sys.exit(f'Không thấy adapter ở {a.adapter}. Chạy lại scripts/chay_m6b_mac.sh hoặc chỉ --adapter.')
print('Đang nạp mô hình (lần đầu mất khoảng 30 giây)...')
model, tok = load(a.model, adapter_path=a.adapter)
xu_ly = make_logits_processors(repetition_penalty=1.1, repetition_context_size=64)

def de_T1():   # cùng khuôn lời yêu cầu với bộ đo (scripts/m3_dung_bo.py, hàm de_T1)
    print('\nLoại văn bản:'); [print(f'  {i + 1}. {x}') for i, x in enumerate(LOAI)]
    loai = LOAI[int(input('Chọn số (1–5): ').strip() or 1) - 1]
    cq = input('Cơ quan ban hành (ví dụ: Thủ tướng Chính phủ, Văn phòng Chính phủ, UBND tỉnh Thái Nguyên): ').strip()
    so = input('Số, ký hiệu (ví dụ: 123/TTg-KTTH; để trống nếu chưa có số): ').strip() or '…'
    d, m, y = (input('Ngày ban hành dd/mm/yyyy: ').strip() or '01/12/2026').split('/')
    ty = input('Trích yếu nội dung: ').strip()
    mm = f'{int(m):02d}' if int(m) < 3 else str(int(m))   # bộ đo viết tháng 1, 2 có số 0 ở trước
    return (f'Soạn hoàn chỉnh một văn bản loại "{loai}" đúng thể thức Nghị định 30/2020/NĐ-CP với thông tin sau:\n- Cơ quan ban hành: {cq}\n- Số, ký hiệu: {so}\n'
            f'- Ngày ban hành: ngày {int(d):02d} tháng {mm} năm {y}\n- Trích yếu nội dung: {ty}\nViết đủ các thành phần thể thức và phần nội dung phù hợp với trích yếu. Chỉ trả về văn bản.')

while True:
    try:
        u = input('\nLời yêu cầu (Enter để kết thúc): ').strip() if a.tu_do else de_T1()
    except (EOFError, KeyboardInterrupt):
        break
    if not u: break
    p = tok.apply_chat_template([{'role': 'system', 'content': HE}, {'role': 'user', 'content': u}], add_generation_prompt=True, tokenize=False, enable_thinking=False)
    print('\n' + '─' * 60)
    for r in stream_generate(model, tok, p, max_tokens=a.toi_da, logits_processors=xu_ly):
        print(r.text, end='', flush=True)
    print('\n' + '─' * 60 + '\nBản nháp do máy sinh. Kiểm lại căn cứ, số hiệu, ngày, họ tên và tên cơ quan trước khi dùng.')
    if input('\nSoạn văn bản khác? (c/k): ').strip().lower() != 'c': break
