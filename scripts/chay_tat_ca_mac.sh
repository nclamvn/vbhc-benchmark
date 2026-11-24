#!/bin/bash
# Chạy trọn M4–M5 trên máy Mac Apple Silicon bằng MLX, không cần người can thiệp.
# Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_tat_ca_mac.sh | bash
# Kết quả và nhật ký ghi vào ~/Documents/vbhc-ketqua. Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng.
set -u
GOC="$HOME/Documents/vbhc-benchmark"; KQ="$HOME/Documents/vbhc-ketqua"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== bắt đầu $(date '+%F %T')"
if [ -d "$GOC/.git" ]; then git -C "$GOC" pull -q --ff-only || true; else git clone -q https://github.com/nclamvn/vbhc-benchmark "$GOC"; fi
cd "$GOC" || exit 1
[ -f m3/train.jsonl ] || xz -dk m3/train.jsonl.xz
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -U pip "mlx-lm[train]" || { echo "LỖI: cài mlx-lm thất bại"; exit 1; }
python3 -c "import mlx_lm, mlx.core as mx; print('mlx-lm', mlx_lm.__version__, 'thiết bị', mx.default_device())"
sysctl -n machdep.cpu.brand_string hw.memsize
MOHINH=("mlx-community/Qwen3-8B-4bit" "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit" "mlx-community/gemma-3-12b-it-4bit")
TEN=("qwen3_8b" "llama31_8b" "gemma3_12b")
# 1. thử nhanh 15 mục để biết tốc độ
caffeinate -i python3 scripts/chay_mlx.py --model "${MOHINH[0]}" --ra "$KQ/thu.jsonl" --gioi-han 5 && python3 scripts/cham_diem.py "$KQ/thu.jsonl" > "$KQ/thu_diem.txt"
# 2. ba mốc không tinh chỉnh
for i in 0 1 2; do
  echo "=== mốc ${TEN[$i]} $(date '+%F %T')"
  caffeinate -i python3 scripts/chay_mlx.py --model "${MOHINH[$i]}" --ra "$KQ/${TEN[$i]}.jsonl" || echo "LỖI khi chạy ${TEN[$i]}"
  python3 scripts/cham_diem.py "$KQ/${TEN[$i]}.jsonl" > "$KQ/${TEN[$i]}_tong.txt" || true
done
# 3. chọn mô hình tốt nhất theo điểm tổng hợp
TOT=$(python3 - "$KQ" <<'PY'
import json, sys, os
kq = sys.argv[1]; ten = ['qwen3_8b', 'llama31_8b', 'gemma3_12b']; mh = ['mlx-community/Qwen3-8B-4bit', 'mlx-community/Meta-Llama-3.1-8B-Instruct-4bit', 'mlx-community/gemma-3-12b-it-4bit']
d = {}
for t, m in zip(ten, mh):
    f = f'{kq}/{t}_diem.json'
    if os.path.exists(f): d[m] = json.load(open(f))['tong']['tong_hop']
print(max(d, key=d.get) if d else mh[0])
PY
)
echo "=== mô hình tốt nhất: $TOT  $(date '+%F %T')"; echo "$TOT" > "$KQ/mo_hinh_tot_nhat.txt"
# 4. tinh chỉnh QLoRA (bỏ qua nếu đã có adapter hoàn chỉnh)
if [ ! -f "$KQ/adapter/adapters.safetensors" ]; then
  caffeinate -i mlx_lm.lora --model "$TOT" --train --data m3 --iters 600 --batch-size 1 --num-layers 8 --max-seq-length 3072 --grad-checkpoint --mask-prompt --steps-per-eval 100 --save-every 100 --adapter-path "$KQ/adapter" \
  || caffeinate -i mlx_lm.lora --model "$TOT" --train --data m3 --iters 600 --batch-size 1 --num-layers 8 --max-seq-length 2048 --grad-checkpoint --steps-per-eval 100 --save-every 100 --adapter-path "$KQ/adapter" \
  || echo "LỖI khi tinh chỉnh"
fi
# 5. chấm mô hình đã tinh chỉnh
if [ -f "$KQ/adapter/adapters.safetensors" ]; then
  caffeinate -i python3 scripts/chay_mlx.py --model "$TOT" --adapter "$KQ/adapter" --ra "$KQ/tinh_chinh.jsonl"
  python3 scripts/cham_diem.py "$KQ/tinh_chinh.jsonl" > "$KQ/tinh_chinh_tong.txt" || true
fi
python3 scripts/bang_diem.py m3/moc_luat_diem.json "$KQ"/*_diem.json > "$KQ/bang_diem.md" 2>/dev/null || true
echo "=== XONG $(date '+%F %T')"
