#!/bin/bash
# M6 · Tinh chỉnh Qwen3-8B bằng QLoRA trên tập huấn luyện v2 (QĐ-12), chọn checkpoint theo val loss thấp nhất, chấm trên bộ kiểm tra.
# Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m6_mac.sh | bash
# Kết quả ghi vào ~/Documents/vbhc-ketqua/m6. Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Dự kiến khoảng 7 giờ, nên cắm sạc.
set -u
GOC="$HOME/Documents/vbhc-benchmark"; KQ="$HOME/Documents/vbhc-ketqua/m6"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M6 bắt đầu $(date '+%F %T')"
if [ -d "$GOC/.git" ]; then git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }; else git clone -q https://github.com/nclamvn/vbhc-benchmark "$GOC"; fi
cd "$GOC" || exit 1
[ -f m6/train.jsonl ] || xz -dk m6/train.jsonl.xz
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python3 -c "import mlx_lm" 2>/dev/null || pip install -q -U pip "mlx-lm[train]" || { echo "LỖI: cài mlx-lm"; exit 1; }
df -h "$HOME" | tail -1
MH="mlx-community/Qwen3-8B-4bit"
# 1. Lượt 1 (24/11, 19:45) hỏng ở vòng 500: hai ví dụ dài hơn 3.072 token bị cắt mất phần trả lời, loss thành nan.
#    Lượt 2 tiếp từ checkpoint vòng 250 của lượt 1 với dữ liệu đã bỏ ví dụ quá 3.000 token; thêm 1.750 vòng.
#    Đánh giá trên 60 ví dụ đầu của tập thẩm định để mỗi lần chấm chỉ còn khoảng 6 phút.
A1="$KQ/adapter"; AD="$KQ/adapter_luot2"
[ -f "$A1/0000250_adapters.safetensors" ] || { echo "LỖI: thiếu checkpoint vòng 250 của lượt 1"; exit 1; }
if [ ! -f "$AD/adapters.safetensors" ] || ! grep -q "=== LƯỢT 2 XONG" "$KQ/nhat_ky.txt"; then
  echo "=== LƯỢT 2 BẮT ĐẦU"
  caffeinate -i mlx_lm.lora --model "$MH" --train --data m6 -c m6/qlora_qwen3_tiep.yaml --resume-adapter-file "$A1/0000250_adapters.safetensors" \
    --iters 1750 --batch-size 1 --num-layers 16 --max-seq-length 3072 --grad-checkpoint --mask-prompt \
    --steps-per-report 50 --steps-per-eval 250 --val-batches 60 --save-every 250 --adapter-path "$AD" \
  || { echo "LỖI khi tinh chỉnh lượt 2"; exit 1; }
  echo "=== LƯỢT 2 XONG"
fi
# 2. chọn checkpoint lượt 2 có val loss thấp nhất và hữu hạn (đọc bảng trong nhật ký, bỏ mã màu)
python3 - "$KQ" <<'PY'
import re, sys, shutil, os, json, math
kq = sys.argv[1]; ad = f'{kq}/adapter_luot2'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== LƯỢT 2 BẮT ĐẦU'):]
v = {int(i): float(x) for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', log, re.M)}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(f'{ad}/{i:07d}_adapters.safetensors')}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn nào')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat', exist_ok=True)
shutil.copy(f'{ad}/{best:07d}_adapters.safetensors', f'{kq}/tot_nhat/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat/adapter_config.json')
json.dump({'val_loss_luot2_60vd': v, 'chon_vong_luot2': best, 'tuong_ung_vong_tong': 250 + best}, open(f'{kq}/chon_checkpoint.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best, '(tổng', 250 + best, ')')
PY
[ -f "$KQ/tot_nhat/adapters.safetensors" ] || exit 1
# 3. chấm checkpoint tốt nhất trên bộ kiểm tra
caffeinate -i python3 scripts/chay_mlx.py --model "$MH" --adapter "$KQ/tot_nhat" --ra "$KQ/qwen3_8b_tinh_chinh_v2.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v2.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v2_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v2_tong.txt"
echo "=== M6 XONG $(date '+%F %T')"
