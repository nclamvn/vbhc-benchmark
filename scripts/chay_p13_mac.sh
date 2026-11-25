#!/bin/bash
# Giao thức 1.3 (QĐ-14): chạy lại T1 với phạt lặp 1,1 + dừng khi lặp nguyên đoạn, cho 5 hệ 8B (~1 giờ 15 phút).
# Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_p13_mac.sh | bash
set -u
GOC="$HOME/Documents/vbhc-benchmark"; KQ="$HOME/Documents/vbhc-ketqua/p13"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" && source .venv/bin/activate
QW="mlx-community/Qwen3-8B-4bit"; LL="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"; R="$HOME/Documents/vbhc-ketqua"
P="--nhiem-vu T1 --phat-lap 1.1 --cua-so-lap 64 --chan-lap-khoi"
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$R/m6b/tot_nhat_v4" --ra "$KQ/p13_qwen3_8b_tinh_chinh_v4.jsonl" $P
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --ra "$KQ/p13_qwen3_8b_goc.jsonl" $P
caffeinate -i python3 scripts/chay_mlx.py --model "$QW" --adapter "$R/m6/tot_nhat_v3" --ra "$KQ/p13_qwen3_8b_tinh_chinh_v3.jsonl" $P
caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --ra "$KQ/p13_llama31_8b_goc.jsonl" $P
caffeinate -i python3 scripts/chay_mlx.py --model "$LL" --adapter "$R/adapter" --ra "$KQ/p13_llama31_8b_tinh_chinh.jsonl" $P
echo "=== GIAO THỨC 1.3 XONG $(date '+%F %T')"
