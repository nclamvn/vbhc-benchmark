#!/bin/bash
# M7 (QĐ-15). Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m7_mac.sh | bash
# Năm phần, chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Tổng khoảng 10–11 giờ, cắm sạc, mở nắp, tắt ứng dụng nặng.
#   A. Giao thức 1.3 cho 5 hệ 8B (nếu chưa chạy chay_p13_mac.sh)                    ~1 giờ 15 phút
#   B. Dò quy mô: Qwen3-14B và Qwen3-30B-A3B bản gốc, T1 giao thức 1.3 (tải ~8 GB + ~17 GB)   ~1 giờ 30 phút
#   C. Giao thức 2.0 (có tư liệu tra cứu): Qwen3-8B gốc, v4, Qwen3-14B gốc             ~1 giờ
#   D. Tinh chỉnh v5 từ v4 trên tập m7                                               ~5–6 giờ
#   E. Chấm v5: đủ bộ theo giao thức 1.1, T1 theo giao thức 2.0                        ~1 giờ
set -u
GOC="$HOME/Documents/vbhc-benchmark"; R="$HOME/Documents/vbhc-ketqua"; KQ="$R/m7"; P13="$R/p13"; mkdir -p "$KQ" "$P13"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M7 bắt đầu $(date '+%F %T')"
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" || exit 1; source .venv/bin/activate
xz -dkf m7/train.jsonl.xz
python3 -c "n=sum(1 for _ in open('m7/train.jsonl'));print('tệp huấn luyện v5:',n,'ví dụ')"
echo "Dung lượng trống: $(df -h "$HOME" | awk 'NR==2{print $4}') (cần khoảng 30 GB cho hai mô hình dò quy mô)"
QW="mlx-community/Qwen3-8B-4bit"; LL="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"
Q14="mlx-community/Qwen3-14B-4bit"; Q30="mlx-community/Qwen3-30B-A3B-4bit"; V4="$R/m6b/tot_nhat_v4"
[ -f "$V4/adapters.safetensors" ] || { echo "LỖI: thiếu adapter v4"; exit 1; }
P="--nhiem-vu T1 --phat-lap 1.1 --cua-so-lap 64 --chan-lap-khoi"
# A. giao thức 1.3 (mỗi lệnh tự bỏ qua các đề đã có)
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$V4" --ra "$P13/p13_qwen3_8b_tinh_chinh_v4.jsonl" $P || echo "LỖI A v4"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --ra "$P13/p13_qwen3_8b_goc.jsonl" $P || echo "LỖI A qwen3 gốc"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$R/m6/tot_nhat_v3" --ra "$P13/p13_qwen3_8b_tinh_chinh_v3.jsonl" $P || echo "LỖI A v3"
caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --ra "$P13/p13_llama31_8b_goc.jsonl" $P || echo "LỖI A llama gốc"
[ -f "$R/adapter/adapters.safetensors" ] && { caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --adapter "$R/adapter" --ra "$P13/p13_llama31_8b_tinh_chinh.jsonl" $P || echo "LỖI A llama tinh chỉnh"; }
echo "=== PHẦN A XONG"
# B. dò quy mô
caffeinate -i python3 scripts/chay_mlx.py --model "$Q14" --ra "$KQ/p13_qwen3_14b_goc.jsonl" $P || echo "LỖI B 14B"
caffeinate -i python3 scripts/chay_mlx.py --model "$Q30" --ra "$KQ/p13_qwen3_30b_a3b_goc.jsonl" $P || echo "LỖI B 30B-A3B"
echo "=== PHẦN B XONG"
# C. giao thức 2.0
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --ra "$KQ/p20_qwen3_8b_goc.jsonl" $P --tra-cuu || echo "LỖI C qwen3 gốc"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$V4" --ra "$KQ/p20_qwen3_8b_tinh_chinh_v4.jsonl" $P --tra-cuu || echo "LỖI C v4"
caffeinate -i python3 scripts/chay_mlx.py --model "$Q14" --ra "$KQ/p20_qwen3_14b_goc.jsonl" $P --tra-cuu || echo "LỖI C 14B"
echo "=== PHẦN C XONG"
# D. tinh chỉnh v5
AD="$KQ/adapter_v5"
if ! grep -q "=== V5 HUẤN LUYỆN XONG" "$KQ/nhat_ky.txt"; then
  echo "=== V5 HUẤN LUYỆN BẮT ĐẦU"
  caffeinate -i mlx_lm.lora --model "$QW" --train --data m7 -c m7/qlora_qwen3_v5.yaml --resume-adapter-file "$V4/adapters.safetensors" \
    --iters 2000 --batch-size 1 --num-layers 16 --max-seq-length 3072 --grad-checkpoint --mask-prompt \
    --steps-per-report 50 --steps-per-eval 250 --val-batches 60 --save-every 250 --adapter-path "$AD" \
  || { echo "LỖI khi tinh chỉnh v5"; exit 1; }
  echo "=== V5 HUẤN LUYỆN XONG"
fi
python3 - "$KQ" "$V4/adapters.safetensors" <<'PY'
import re, sys, shutil, os, json, math
kq, v4 = sys.argv[1], sys.argv[2]; ad = f'{kq}/adapter_v5'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== V5 HUẤN LUYỆN BẮT ĐẦU'):]
if re.search(r'longer than 3072', log): print('CẢNH BÁO: còn ví dụ quá 3.072 token')
v = {int(i): float(x) for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', log, re.M)}
tep = {i: (v4 if i == 1 else f'{ad}/{i:07d}_adapters.safetensors') for i in v}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(tep[i])}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat_v5', exist_ok=True)
shutil.copy(tep[best], f'{kq}/tot_nhat_v5/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat_v5/adapter_config.json')
json.dump({'val_loss_v5_60vd': v, 'chon_vong': best, 'ghi_chu': 'vòng 1 = bản v4 đo trên tập thẩm định v5'}, open(f'{kq}/chon_checkpoint_v5.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best)
PY
[ -f "$KQ/tot_nhat_v5/adapters.safetensors" ] || exit 1
# E. chấm v5
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v5" --ra "$KQ/qwen3_8b_tinh_chinh_v5.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v5.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v5_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v5_tong.txt"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v5" --ra "$KQ/p20_qwen3_8b_tinh_chinh_v5.jsonl" $P --tra-cuu
echo "=== M7 XONG $(date '+%F %T')"
