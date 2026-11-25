#!/bin/bash
# Chạy thử mô hình cơ sở pilot trên Mac. Dán vào Terminal (giữ nguyên bash -c và dấu ngoặc):
#   bash -c "$(curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/thu_v4.sh)"
GOC="$HOME/Documents/vbhc-benchmark"
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" && source .venv/bin/activate && python3 scripts/thu_v4.py "$@"
