#!/bin/bash
# M6 · Tinh chỉnh Qwen3-8B bằng QLoRA trên tập huấn luyện v2 (QĐ-12), chọn checkpoint theo val loss thấp nhất, chấm trên bộ kiểm tra.
# Dán vào Terminal:  curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m6_mac.sh | bash
# Kết quả ghi vào ~/Documents/vbhc-ketqua/m6. Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Lượt 3 dự kiến khoảng 5 giờ, nên cắm sạc.
set -u
GOC="$HOME/Documents/vbhc-benchmark"; KQ="$HOME/Documents/vbhc-ketqua/m6"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M6 bắt đầu $(date '+%F %T')"
if [ -d "$GOC/.git" ]; then git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }; else git clone -q https://github.com/nclamvn/vbhc-benchmark "$GOC"; fi
cd "$GOC" || exit 1
xz -dkf m6/train.jsonl.xz   # luôn giải nén lại: lượt 2 đã chạy nhầm bản cũ còn sót trên máy
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python3 -c "import mlx_lm" 2>/dev/null || pip install -q -U pip "mlx-lm[train]" || { echo "LỖI: cài mlx-lm"; exit 1; }
df -h "$HOME" | tail -1
MH="mlx-community/Qwen3-8B-4bit"
# 1. Lượt 1 và lượt 2 đều hỏng ở cùng vị trí dữ liệu (vòng 450–500): lượt 2 vẫn dùng tệp train.jsonl cũ chưa lọc còn sót trên máy,
#    nên ví dụ 3.570 token lại làm loss thành nan. Checkpoint tốt nhất hiện có là vòng 250 của lượt 2 (val 0,872 trên 60 ví dụ).
#    Lượt 3 tiếp từ checkpoint đó, trên dữ liệu đã lọc thật, thêm 1.500 vòng. Val ở vòng 1 của lượt 3 chính là của checkpoint xuất phát,
#    nên việc chọn checkpoint có tính cả trường hợp không huấn luyện thêm.
python3 -c "import json,sys;from collections import Counter;L=[sum(len(m['content']) for m in json.loads(l)['messages']) for l in open('m6/train.jsonl',encoding='utf-8')];print('tệp huấn luyện',len(L),'ví dụ')"
A2="$KQ/adapter_luot2/0000250_adapters.safetensors"; AD="$KQ/adapter_luot3"
[ -f "$A2" ] || { echo "LỖI: thiếu checkpoint vòng 250 lượt 2"; exit 1; }
if ! grep -q "=== LƯỢT 3 XONG" "$KQ/nhat_ky.txt"; then
  echo "=== LƯỢT 3 BẮT ĐẦU"
  caffeinate -i mlx_lm.lora --model "$MH" --train --data m6 -c m6/qlora_qwen3_luot3.yaml --resume-adapter-file "$A2" \
    --iters 1500 --batch-size 1 --num-layers 16 --max-seq-length 3072 --grad-checkpoint --mask-prompt \
    --steps-per-report 50 --steps-per-eval 250 --val-batches 60 --save-every 250 --adapter-path "$AD" \
  || { echo "LỖI khi tinh chỉnh lượt 3"; exit 1; }
  echo "=== LƯỢT 3 XONG"
fi
python3 - "$KQ" "$A2" <<'PY'
import re, sys, shutil, os, json, math
kq, a2 = sys.argv[1], sys.argv[2]; ad = f'{kq}/adapter_luot3'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== LƯỢT 3 BẮT ĐẦU'):]
if re.search(r'longer than 3072', log): print('CẢNH BÁO: vẫn còn ví dụ quá 3.072 token')
v = {int(i): float(x) for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', log, re.M)}
tep = {i: (a2 if i == 1 else f'{ad}/{i:07d}_adapters.safetensors') for i in v}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(tep[i])}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn nào')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat_v3', exist_ok=True)
shutil.copy(tep[best], f'{kq}/tot_nhat_v3/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat_v3/adapter_config.json')
json.dump({'val_loss_luot3_60vd': v, 'chon_vong_luot3': best, 'ghi_chu': 'vòng 1 = checkpoint vòng 250 lượt 2'}, open(f'{kq}/chon_checkpoint_v3.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best)
PY
[ -f "$KQ/tot_nhat_v3/adapters.safetensors" ] || exit 1
caffeinate -i python3 scripts/chay_mlx.py --model "$MH" --adapter "$KQ/tot_nhat_v3" --ra "$KQ/qwen3_8b_tinh_chinh_v3.jsonl"
python3 scripts/cham_diem.py "$KQ/qwen3_8b_tinh_chinh_v3.jsonl" > "$KQ/qwen3_8b_tinh_chinh_v3_tong.txt" || true
cat "$KQ/qwen3_8b_tinh_chinh_v3_tong.txt"
echo "=== M6 LƯỢT 3 XONG $(date '+%F %T')"
