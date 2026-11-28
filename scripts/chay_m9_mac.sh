#!/bin/bash
# M9: huấn luyện v7 trên tập v7c rồi chấm. Dán vào Terminal:
#   curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m9_mac.sh | bash
# Chạy lại cùng lệnh sẽ tiếp tục từ chỗ dừng. Cắm sạc, mở nắp, tắt ứng dụng nặng.
#   A. Thử bộ nhớ: 20 vòng ở khung 6.144 token. Cổng: đỉnh dưới 28 GB, không thì dừng   ~10 phút
#   B. Tinh chỉnh v7 từ v6, 1.500 vòng (in ước tính thời gian sau bước A)
#   C. Chấm: v7 giao thức 2.0 khối bộ máy cũ (so thẳng với v6 đã công bố), v7 và v6 với khối bộ máy v1.1,
#      rồi v7 và v6 trên 20 văn bản mới nhất chưa từng huấn luyện                          ~2,5 giờ
set -u
GOC="$HOME/Documents/vbhc-benchmark"; R="$HOME/Documents/vbhc-ketqua"; KQ="$R/m9"; mkdir -p "$KQ"
exec > >(tee -a "$KQ/nhat_ky.txt") 2>&1
echo "=== M9 bắt đầu $(date '+%F %T')"
git -C "$GOC" pull -q --ff-only || { echo "LỖI: git pull"; exit 1; }
cd "$GOC" || exit 1; source .venv/bin/activate
[ -f m8c_6000/train.jsonl ] || xz -dkf m8c_6000/train.jsonl.xz
python3 -c "n=sum(1 for _ in open('m8c_6000/train.jsonl'));print('tệp huấn luyện v7c:',n,'ví dụ')"
QW="mlx-community/Qwen3-8B-4bit"; V6="$R/m7b/tot_nhat_v6"
[ -f "$V6/adapters.safetensors" ] || { echo "LỖI: thiếu adapter v6 ở $V6"; exit 1; }
CHUNG="--batch-size 1 --num-layers 16 --max-seq-length 6144 --grad-checkpoint --mask-prompt"
# A. thử bộ nhớ
if ! grep -q "=== BỘ NHỚ ĐẠT" "$KQ/nhat_ky.txt"; then
  echo "=== THỬ BỘ NHỚ BẮT ĐẦU"; rm -rf "$KQ/thu_bo_nho"; echo "swap trước: $(sysctl -n vm.swapusage)"
  caffeinate -i python3 scripts/m9_lora.py --model "$QW" --train --data m8c_6000 -c m8c_6000/qlora_qwen3_v7.yaml --resume-adapter-file "$V6/adapters.safetensors" \
    --iters 20 $CHUNG --steps-per-report 5 --steps-per-eval 1000 --val-batches 1 --save-every 1000 --adapter-path "$KQ/thu_bo_nho" \
  || { echo "LỖI khi thử bộ nhớ (có thể thiếu bộ nhớ). Gửi tệp $KQ/nhat_ky.txt"; exit 1; }
  echo "swap sau: $(sysctl -n vm.swapusage)"
  python3 - "$KQ/nhat_ky.txt" <<'PY' || exit 1
import re, sys
log = re.sub(r'\x1b\[[0-9;]*m', '', open(sys.argv[1], encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
log = log[log.rindex('=== THỬ BỘ NHỚ BẮT ĐẦU'):]
mem = [float(x) for x in re.findall(r'Peak mem ([\d.]+) GB', log)]
dong = [(int(a), float(b), float(c)) for a, b, c in re.findall(r'^\s*(\d+)\s+[\d.]+\s+\S+\s+([\d.]+)\s+([\d.]+)k\s*$', log, re.M)]   # vòng, tok/s, nghìn token đã học
if not mem: sys.exit('LỖI: không đọc được bộ nhớ đỉnh. Gửi nhật ký.')
dinh = max(mem); gio = None
if dong:
    tb_tok = dong[-1][2] * 1000 / dong[-1][0]; toc = sum(x[1] for x in dong) / len(dong); gio = 1500 * tb_tok / toc / 3600
    print(f'trung bình {tb_tok:.0f} token mỗi vòng, {toc:.0f} token/giây')
sw = re.findall(r'swap (trước|sau): total = [\d.]+M\s+used = ([\d.]+)M', log)
tang = float(sw[-1][1]) - float(sw[-2][1]) if len(sw) >= 2 else 0
print(f'bộ nhớ đỉnh {dinh:.1f} GB, swap tăng {tang:.0f} MB' + (f', ước tính 1.500 vòng khoảng {gio:.1f} giờ (chưa tính đánh giá)' if gio else ''))
if tang > 500: sys.exit('=== BỘ NHỚ KHÔNG ĐẠT (dùng swap). Dừng. Gửi nhật ký để dựng lại tập ở khung 4.500 token.')
if re.search(r'longer than 6144', log): print('CẢNH BÁO: có ví dụ dài hơn 6.144 token, sẽ bị cắt')
if dinh >= 28: sys.exit('=== BỘ NHỚ KHÔNG ĐẠT (≥ 28 GB). Dừng. Gửi nhật ký để dựng lại tập ở khung 4.500 token.')
print('=== BỘ NHỚ ĐẠT')
PY
fi
# B. tinh chỉnh v7 (tiếp từ checkpoint gần nhất nếu bị ngắt)
AD="$KQ/adapter_v7"
if ! grep -q "=== V7 HUẤN LUYỆN XONG" "$KQ/nhat_ky.txt"; then
  TIEP="$V6/adapters.safetensors"; CON=1500
  CUOI=$(ls "$AD"/0*_adapters.safetensors 2>/dev/null | sort | tail -1)
  if [ -n "$CUOI" ]; then DA=$(basename "$CUOI" | sed 's/_adapters.safetensors//;s/^0*//'); TIEP="$CUOI"; CON=$((1500 - DA)); echo "tiếp từ vòng $DA, còn $CON vòng"; fi
  echo "=== V7 HUẤN LUYỆN BẮT ĐẦU (đã xong ${DA:-0})"
  caffeinate -i python3 scripts/m9_lora.py --model "$QW" --train --data m8c_6000 -c m8c_6000/qlora_qwen3_v7.yaml --resume-adapter-file "$TIEP" \
    --iters "$CON" $CHUNG --steps-per-report 50 --steps-per-eval 300 --val-batches 60 --save-every 300 --adapter-path "$AD.phan_${DA:-0}" \
  || { echo "LỖI khi tinh chỉnh v7. Chạy lại cùng lệnh để tiếp."; exit 1; }
  mkdir -p "$AD"; cp "$AD.phan_${DA:-0}/adapter_config.json" "$AD/"
  for f in "$AD.phan_${DA:-0}"/0*_adapters.safetensors; do n=$(basename "$f" | sed 's/_adapters.safetensors//;s/^0*//'); cp "$f" "$AD/$(printf '%07d' $(( n + ${DA:-0} )))_adapters.safetensors"; done
  echo "=== V7 HUẤN LUYỆN XONG"
fi
python3 - "$KQ" "$V6/adapters.safetensors" <<'PY' || exit 1
import re, sys, shutil, os, json, math
kq, v6 = sys.argv[1], sys.argv[2]; ad = f'{kq}/adapter_v7'
log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{kq}/nhat_ky.txt', encoding='utf-8', errors='ignore').read().replace('\r', '\n'))
v = {}
for m in re.finditer(r'=== V7 HUẤN LUYỆN BẮT ĐẦU \(đã xong (\d+)\)', log):
    doan = log[m.end():]; doan = doan[:doan.find('=== V7 HUẤN LUYỆN BẮT ĐẦU') if '=== V7 HUẤN LUYỆN BẮT ĐẦU' in doan else len(doan)]
    for i, x in re.findall(r'^\s*(\d+)\s+val\s+([\d.]+|nan)', doan, re.M): v[int(i) + int(m[1]) if int(i) > 1 else int(m[1]) + 1] = float(x)
tep = {i: (v6 if i == 1 else f'{ad}/{i:07d}_adapters.safetensors') for i in v}
co = {i: x for i, x in v.items() if not math.isnan(x) and os.path.exists(tep[i])}
if not co: sys.exit('LỖI: không có checkpoint hữu hạn')
best = min(co, key=co.get); os.makedirs(f'{kq}/tot_nhat_v7', exist_ok=True)
shutil.copy(tep[best], f'{kq}/tot_nhat_v7/adapters.safetensors'); shutil.copy(f'{ad}/adapter_config.json', f'{kq}/tot_nhat_v7/adapter_config.json')
json.dump({'val_loss_v7c_60vd': v, 'chon_vong': best, 'ghi_chu': 'vòng 1 = bản v6 đo trên tập thẩm định v7c'}, open(f'{kq}/chon_checkpoint_v7.json', 'w'), indent=1)
print('val loss', v, '→ chọn vòng', best)
PY
# C. chấm (mỗi tệp chạy xong thì bỏ qua khi chạy lại)
P="--nhiem-vu T1 --phat-lap 1.1 --cua-so-lap 64 --chan-lap-khoi --tra-cuu"
chay() { [ -s "$KQ/$1" ] && [ "$(wc -l < "$KQ/$1")" -ge "$2" ] && { echo "đã có $1"; return; }; shift 2; caffeinate -i env "$@"; }
chay p20_v7_sot0.jsonl 41 python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v7" --ra "$KQ/p20_v7_sot0.jsonl" $P
chay p20_v7.jsonl 41 VBHC_SOT_BAN=v1.1 VBHC_DVD=m8/dong_vien_dan_c.json python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v7" --ra "$KQ/p20_v7.jsonl" $P
chay p20_v6_sot11.jsonl 41 VBHC_SOT_BAN=v1.1 VBHC_DVD=m8/dong_vien_dan_c.json python3 scripts/chay_mlx.py --model "$QW" --adapter "$V6" --ra "$KQ/p20_v6_sot11.jsonl" $P
chay moi_v7.jsonl 20 VBHC_SOT_BAN=v1.1 VBHC_DVD=m8/dong_vien_dan_c.json python3 scripts/chay_mlx.py --model "$QW" --adapter "$KQ/tot_nhat_v7" --de m9/de_moi.jsonl --ra "$KQ/moi_v7.jsonl" $P
chay moi_v6.jsonl 20 VBHC_SOT_BAN=v1.1 VBHC_DVD=m8/dong_vien_dan_c.json python3 scripts/chay_mlx.py --model "$QW" --adapter "$V6" --de m9/de_moi.jsonl --ra "$KQ/moi_v6.jsonl" $P
mkdir -p "$GOC/ket_qua/m9" && cp "$KQ"/p20_*.jsonl "$KQ"/moi_*.jsonl "$KQ/chon_checkpoint_v7.json" "$GOC/ket_qua/m9/"
echo "=== M9 XONG $(date '+%F %T'). Kết quả ở $KQ và đã chép vào ket_qua/m9 trong thư mục repo."
echo "Gửi lại cho Claude: thư mục ket_qua/m9 (nén:  cd $GOC && cp $KQ/nhat_ky.txt ket_qua/m9/ && tar czf ~/Desktop/m9.tgz ket_qua/m9)"
