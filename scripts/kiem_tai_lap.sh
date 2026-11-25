#!/bin/bash
# Kiểm tái lập pilot từ một bản clone sạch (M6 · đóng gói). Không cần GPU.
#   bash scripts/kiem_tai_lap.sh                  → bước 1–2 (chỉ cần Python 3)
#   VBHC_TOAN_VAN=<toan_van_v4.jsonl> bash scripts/kiem_tai_lap.sh   → thêm bước 3–4 (cần toàn văn tải từ Drive, và transformers cho bước 4)
set -u; LOI=0
echo "1. Chấm lại mọi tệp trả lời, so với điểm đã công bố"
cp ket_qua/bang_xep_hang.json /tmp/bxh_cong_bo.json
python3 scripts/bang_xep_hang.py > /dev/null && if cmp -s ket_qua/bang_xep_hang.json /tmp/bxh_cong_bo.json; then echo "   KHỚP: bảng xếp hạng tính lại trùng từng byte"; else echo "   LỆCH: xem git diff ket_qua/bang_xep_hang.json"; LOI=1; fi
echo "2. Bộ kiểm trung thực chạy trên văn bản thật (mức báo nhầm)"
python3 scripts/kiem_trung_thuc.py m3/chi_muc_kiem_trung_thuc.csv.xz m3/test_dap_an.jsonl --tham-chieu
if [ -n "${VBHC_TOAN_VAN:-}" ]; then
  echo "3. Dựng lại bộ đánh giá M3, so từng byte"
  for f in test_de.jsonl test_dap_an.jsonl valid.jsonl chia_tap.json; do cp m3/$f /tmp/goc_$f; done
  python3 scripts/m3_dung_bo.py > /dev/null
  for f in test_de.jsonl test_dap_an.jsonl valid.jsonl chia_tap.json; do cmp -s m3/$f /tmp/goc_$f && echo "   KHỚP m3/$f" || { echo "   LỆCH m3/$f"; LOI=1; }; done
  echo "4. Dựng lại tập huấn luyện v2 và v4, so từng byte"
  cp m6/valid.jsonl /tmp/goc_m6_valid.jsonl; cp m6b/valid.jsonl /tmp/goc_m6b_valid.jsonl; xz -dc m6/train.jsonl.xz > /tmp/goc_m6_train.jsonl; xz -dc m6b/train.jsonl.xz > /tmp/goc_m6b_train.jsonl
  python3 scripts/m6_du_lieu_v2.py > /dev/null && python3 scripts/m6_du_lieu_v4.py > /dev/null
  for p in m6/train m6/valid m6b/train m6b/valid; do cmp -s $p.jsonl /tmp/goc_${p%%/*}_${p##*/}.jsonl && echo "   KHỚP $p.jsonl" || { echo "   LỆCH $p.jsonl"; LOI=1; }; done
  echo "5. Dựng lại bảng đồng viện dẫn và tập v5 (M7), so từng byte"
  cp m7/dong_vien_dan.json /tmp/goc_m7_dvd.json; cp m7/valid.jsonl /tmp/goc_m7_valid.jsonl; xz -dc m7/train.jsonl.xz > /tmp/goc_m7_train.jsonl
  python3 scripts/tra_cuu.py --dung > /dev/null && python3 scripts/m7_du_lieu_v5.py > /dev/null
  cmp -s m7/dong_vien_dan.json /tmp/goc_m7_dvd.json && echo "   KHỚP m7/dong_vien_dan.json" || { echo "   LỆCH m7/dong_vien_dan.json"; LOI=1; }
  for p in train valid; do cmp -s m7/$p.jsonl /tmp/goc_m7_$p.jsonl && echo "   KHỚP m7/$p.jsonl" || { echo "   LỆCH m7/$p.jsonl"; LOI=1; }; done
fi
[ $LOI = 0 ] && echo "=== TÁI LẬP ĐẠT" || echo "=== CÓ BƯỚC LỆCH"
exit $LOI
