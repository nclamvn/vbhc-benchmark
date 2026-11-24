#!/bin/bash
# M6 · Tinh chỉnh Qwen3-8B bằng QLoRA trên tập huấn luyện v2 (QĐ-12), chọn checkpoint theo val loss thấp nhất, chấm trên bộ kiểm tra.
# Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m6_mac.sh | bash
# Kết quả ghi vào ~/Documents/vbhc-ketqua/m6. Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Dự kiến 5–6 giờ, nên cắm sạc.
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
MH="mlx-community/Qwen3-8B-4bit"; AD="$KQ/adapter"
# 1. huấn luyện khoảng một lượt dữ liệu (2.004 ví dụ), đánh giá toàn bộ tập thẩm định mỗi 250 vòng
if [ ! -f "$AD/adapters.safetensors" ]; then
  caffeinate -i mlx_lm.lora --model "$MH" --train --data m6 -c m6/qlora_qwen3.yaml --iters 2000 --batch-size 1 --num-layers 16 \
    --max-seq-length 3072 --grad-checkpoint --mask-prompt --steps-per-report 50 --steps-per-eval 250 --val-batches -1 --save-every 250 --adapter-path "$AD" \
  || { echo "=== tệp cấu hình không nhận, chạy lại với LR cố định 2e-5"; caffeinate -i mlx_lm.lora --model "$MH" --train --data m6 --learning-rate 2e-5 --iters 2000 --batch-size 1 --num-layers 16 \
    --max-seq-length 3072 --grad-checkpoint --mask-prompt --steps-per-report 50 --steps-per-eval 250 --val-batches -1 --save-every 250 --adapter-path "$AD"; } \
  || { echo "LỖI khi tinh chỉnh"; exit 1; }
fi
# 2. chọn checkpoint có val loss thấp nhất (đọc từ nhật ký)
python3 - "$KQ" <<'PY'
import re, sys, shutil, os, json
kq = sys.argv[1]; ad = f'{kq}/adapter'; log = open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read()
v = {int(i): float(x) for i, x in re.findall(r'Iter (\d+): Val loss ([\d.]+)', log)}
co = {i: x for i, x in v.items() if os.path.exists(f'{ad}/{i:07d}_adapters.safetensors')}
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat', exist_ok=True)
shutil.copy(f'{ad}/{best:07d}_adapters.safetensors', f'{kq}/tot_nhat/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat/adapter_config.json')
json.dump({'val_loss': v, 'chon': best}, open(f'{kq}/chon_checkpoint.json', 'w'), indent=1); print('val loss', v, '→ chọn vòng', best)
PY
# 3. chấm checkpoint tốt nhất trên bộ kiểm tra
caffeinate -i python3 scripts/chay_mlx.py --model "$MH" --adapter "$KQ/tot_nhat" --ra "$KQ/qwen3_8b_tinh_chinh_v2.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v2.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v2_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v2_tong.txt"
echo "=== M6 XONG $(date '+%F %T')"
