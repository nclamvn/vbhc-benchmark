# Chạy M4–M5 trên máy Mac (M1 Max, 32 GB)

Các lệnh dưới đây chưa được chạy thử trên máy thật. Bước 2 là phép thử 5 phút để biết sớm có lỗi gì.

## 1. Chuẩn bị (một lần)

    git clone https://github.com/nclamvn/vbhc-benchmark && cd vbhc-benchmark
    python3 -m venv .venv && source .venv/bin/activate
    pip install -U "mlx-lm[train]"
    xz -dk m3/train.jsonl.xz

## 2. Thử nhanh 15 mục (khoảng 5 phút, tải mô hình lần đầu lâu hơn)

    python3 scripts/chay_mlx.py --model mlx-community/Qwen3-8B-4bit --ra ket_qua/thu.jsonl --gioi-han 5
    python3 scripts/cham_diem.py ket_qua/thu.jsonl

Nếu tên mô hình không tồn tại, tìm bản 4-bit tương ứng trên trang mlx-community của Hugging Face rồi thay tên. Gửi lại cho Claude: dòng lỗi (nếu có) và số "giây mỗi mục".

## 3. Ba mốc không tinh chỉnh (285 mục mỗi mô hình)

    python3 scripts/chay_mlx.py --model <mô hình 1> --ra ket_qua/m1.jsonl
    python3 scripts/chay_mlx.py --model <mô hình 2> --ra ket_qua/m2.jsonl
    python3 scripts/chay_mlx.py --model <mô hình 3> --ra ket_qua/m3.jsonl
    for f in ket_qua/m?.jsonl; do python3 scripts/cham_diem.py $f; done

Lệnh bị ngắt thì chạy lại y nguyên, kịch bản tự làm tiếp từ mục còn thiếu.

## 4. Tinh chỉnh QLoRA trên mô hình tốt nhất (chạy qua đêm)

    mlx_lm.lora --model <mô hình tốt nhất> --train --data m3 --iters 600 --batch-size 1 --num-layers 8 --max-seq-length 3072 --grad-checkpoint --adapter-path adapters/vbhc
    python3 scripts/chay_mlx.py --model <mô hình tốt nhất> --adapter adapters/vbhc --ra ket_qua/tinh_chinh.jsonl
    python3 scripts/cham_diem.py ket_qua/tinh_chinh.jsonl

Nếu máy báo hết bộ nhớ: giảm --max-seq-length xuống 2048. Nếu sau 1 giờ chưa qua 60 vòng lặp: dừng và báo lại, theo QĐ-10 một lượt không được quá 12 giờ.

## 5. Gửi lại

Thư mục ket_qua/ (các tệp .jsonl và _diem.json). Điểm phần nội dung của T1 cần người chấm; các tệp _diem.json chỉ có phần máy chấm được.
