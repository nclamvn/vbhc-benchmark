#!/bin/bash
# M7b (QĐ-16). Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m7b_mac.sh | bash
# Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Khoảng 5 giờ, cắm sạc, mở nắp, tắt ứng dụng nặng.
#   D. Tinh chỉnh v6 từ v5 trên tập m7b, 800 vòng                       ~3 giờ
#   E. Chấm v6: T1 theo giao thức 2.0 trước, rồi đủ bộ theo giao thức 1.1   ~2 giờ
set -u
GOC="$HOME/Documents/vbhc-benchmark"; R="$HOME/Documents/vbhc-ketqua"; KQ="$R/m7b"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M7b bắt đầu $(date '+%F %T')"
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" || exit 1; source .venv/bin/activate
xz -dkf m7b/train.jsonl.xz
python3 -c "n=sum(1 for _ in open('m7b/train.jsonl'));print('tệp huấn luyện v6:',n,'ví dụ')"
QW="mlx-community/Qwen3-8B-4bit"; V5="$R/m7/tot_nhat_v5"
[ -f "$V5/adapters.safetensors" ] || { echo "LỖI: thiếu adapter v5"; exit 1; }
P="--nhiem-vu T1 --phat-lap 1.1 --cua-so-lap 64 --chan-lap-khoi"
# D. tinh chỉnh v6
AD="$KQ/adapter_v6"
if ! grep -q "=== V6 HUẤN LUYỆN XONG" "$KQ/nhat_ky.txt"; then
  echo "=== V6 HUẤN LUYỆN BẮT ĐẦU"
  caffeinate -i mlx_lm.lora --model "$QW" --train --data m7b -c m7b/qlora_qwen3_v6.yaml --resume-adapter-file "$V5/adapters.safetensors" \
    --iters 800 --batch-size 1 --num-layers 16 --max-seq-length 3072 --grad-checkpoint --mask-prompt \
    --steps-per-report 50 --steps-per-eval 200 --val-batches 60 --save-every 200 --adapter-path "$AD" \
  || { echo "LỖI khi tinh chỉnh v6"; exit 1; }
  echo "=== V6 HUẤN LUYỆN XONG"
fi
python3 - "$KQ" "$V5/adapters.safetensors" <<'PY'
import re, sys, shutil, os, json, math
kq, v5 = sys.argv[1], sys.argv[2]; ad = f'{kq}/adapter_v6'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== V6 HUẤN LUYỆN BẮT ĐẦU'):]
if re.search(r'longer than 3072', log): print('CẢNH BÁO: còn ví dụ quá 3.072 token')
v = {int(i): float(x) for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', log, re.M)}
tep = {i: (v5 if i == 1 else f'{ad}/{i:07d}_adapters.safetensors') for i in v}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(tep[i])}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat_v6', exist_ok=True)
shutil.copy(tep[best], f'{kq}/tot_nhat_v6/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat_v6/adapter_config.json')
json.dump({'val_loss_v6_60vd': v, 'chon_vong': best, 'ghi_chu': 'vòng 1 = bản v5 đo trên tập thẩm định v6'}, open(f'{kq}/chon_checkpoint_v6.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best)
PY
[ -f "$KQ/tot_nhat_v6/adapters.safetensors" ] || exit 1
# E. chấm v6: giao thức 2.0 trước (quyết định), rồi đủ bộ 1.1
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v6" --ra "$KQ/p20_qwen3_8b_tinh_chinh_v6.jsonl" $P --tra-cuu
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v6" --ra "$KQ/qwen3_8b_tinh_chinh_v6.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v6.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v6_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v6_tong.txt"
echo "=== M7b XONG $(date '+%F %T')"
