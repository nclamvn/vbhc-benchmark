#!/bin/bash
# M6b (QĐ-13). Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m6b_mac.sh | bash
# Ba phần, chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Tổng khoảng 9 giờ, cắm sạc, mở nắp, tắt ứng dụng nặng.
#   A. Giao thức 1.2: chạy lại phần soạn văn bản (T1) có phạt lặp 1,1 cho 4 hệ 8B (~1 giờ 15 phút)
#   B. Tinh chỉnh v4 từ v3 trên tập m6b (~6–7 giờ)
#   C. Chấm v4: đủ bộ kiểm tra theo giao thức 1.1, và T1 theo giao thức 1.2 (~1 giờ)
set -u
GOC="$HOME/Documents/vbhc-benchmark"; KQ="$HOME/Documents/vbhc-ketqua/m6b"; M6="$HOME/Documents/vbhc-ketqua/m6"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M6b bắt đầu $(date '+%F %T')"
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" || exit 1; source .venv/bin/activate
xz -dkf m6b/train.jsonl.xz
python3 -c "import json;n=sum(1 for _ in open('m6b/train.jsonl'));print('tệp huấn luyện v4:',n,'ví dụ')"
QW="mlx-community/Qwen3-8B-4bit"; LL="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"; V3="$M6/tot_nhat_v3"
[ -f "$V3/adapters.safetensors" ] || { echo "LỖI: thiếu adapter v3"; exit 1; }
# A. giao thức 1.2 cho T1
P="--nhiem-vu T1 --phat-lap 1.1 --cua-so-lap 64"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --ra "$KQ/p12_qwen3_8b_goc.jsonl" $P || echo "LỖI A qwen3 gốc"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$V3" --ra "$KQ/p12_qwen3_8b_tinh_chinh_v3.jsonl" $P || echo "LỖI A v3"
caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --ra "$KQ/p12_llama31_8b_goc.jsonl" $P || echo "LỖI A llama gốc"
[ -f "$HOME/Documents/vbhc-ketqua/adapter/adapters.safetensors" ] && caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --adapter "$HOME/Documents/vbhc-ketqua/adapter" --ra "$KQ/p12_llama31_8b_tinh_chinh.jsonl" $P || echo "LỖI A llama tinh chỉnh"
echo "=== PHẦN A XONG"
# B. tinh chỉnh v4
AD="$KQ/adapter_v4"
if ! grep -q "=== V4 HUẤN LUYỆN XONG" "$KQ/nhat_ky.txt"; then
  echo "=== V4 HUẤN LUYỆN BẮT ĐẦU"
  caffeinate -i mlx_lm.lora --model "$QW" --train --data m6b -c m6b/qlora_qwen3_v4.yaml --resume-adapter-file "$V3/adapters.safetensors" \
    --iters 2100 --batch-size 1 --num-layers 16 --max-seq-length 3072 --grad-checkpoint --mask-prompt \
    --steps-per-report 50 --steps-per-eval 300 --val-batches 60 --save-every 300 --adapter-path "$AD" \
  || { echo "LỖI khi tinh chỉnh v4"; exit 1; }
  echo "=== V4 HUẤN LUYỆN XONG"
fi
python3 - "$KQ" "$V3/adapters.safetensors" <<'PY'
import re, sys, shutil, os, json, math
kq, v3 = sys.argv[1], sys.argv[2]; ad = f'{kq}/adapter_v4'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== V4 HUẤN LUYỆN BẮT ĐẦU'):]
if re.search(r'longer than 3072', log): print('CẢNH BÁO: còn ví dụ quá 3.072 token')
v = {int(i): float(x) for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', log, re.M)}
tep = {i: (v3 if i == 1 else f'{ad}/{i:07d}_adapters.safetensors') for i in v}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(tep[i])}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat_v4', exist_ok=True)
shutil.copy(tep[best], f'{kq}/tot_nhat_v4/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat_v4/adapter_config.json')
json.dump({'val_loss_v4_60vd': v, 'chon_vong': best, 'ghi_chu': 'vòng 1 = bản v3 đo trên tập thẩm định v4'}, open(f'{kq}/chon_checkpoint_v4.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best)
PY
[ -f "$KQ/tot_nhat_v4/adapters.safetensors" ] || exit 1
# C. chấm v4
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v4" --ra "$KQ/qwen3_8b_tinh_chinh_v4.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v4.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v4_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v4_tong.txt"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v4" --ra "$KQ/p12_qwen3_8b_tinh_chinh_v4.jsonl" $P
echo "=== M6b XONG $(date '+%F %T')"
