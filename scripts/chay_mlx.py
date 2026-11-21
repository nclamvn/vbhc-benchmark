"""Chạy một mô hình trên bộ kiểm tra VBHC-Bench bằng MLX (máy Mac Apple Silicon).
CHƯA CHẠY THỬ trên máy thật: viết theo giao diện mlx_lm đã công bố (load, generate). Nếu báo lỗi tham số, gửi lại dòng lỗi.
Dùng:  python3 scripts/chay_mlx.py --model <tên hoặc đường dẫn mô hình MLX> --ra ket_qua/<ten>.jsonl [--adapter adapters/vbhc] [--gioi-han 20]
Chạy lại cùng lệnh sẽ tiếp tục từ mục còn thiếu."""
import argparse, json, os, time
from mlx_lm import load, generate
ap = argparse.ArgumentParser(); ap.add_argument('--model', required=True); ap.add_argument('--ra', required=True)
ap.add_argument('--adapter'); ap.add_argument('--de', default='m3/test_de.jsonl'); ap.add_argument('--gioi-han', type=int, default=0)
a = ap.parse_args(); os.makedirs(os.path.dirname(a.ra) or '.', exist_ok=True)
D = [json.loads(l) for l in open(a.de, encoding='utf-8')]
if a.gioi_han:  # lấy đều ba nhiệm vụ để thử nhanh
    D = [x for nv in ['T1', 'T2', 'T3'] for x in [d for d in D if d['nhiem_vu'] == nv][:a.gioi_han]]
xong = {json.loads(l)['id'] for l in open(a.ra, encoding='utf-8')} if os.path.exists(a.ra) else set()
model, tok = load(a.model, adapter_path=a.adapter) if a.adapter else load(a.model)
TOI_DA = {'T1': 1800, 'T2': 48, 'T3': 320}; t0 = time.time(); n = 0
with open(a.ra, 'a', encoding='utf-8') as f:
    for d in D:
        if d['id'] in xong: continue
        m = [{'role': 'system', 'content': d['he_thong']}, {'role': 'user', 'content': d['de']}]
        try: p = tok.apply_chat_template(m, add_generation_prompt=True, tokenize=False, enable_thinking=False)   # tắt chế độ suy nghĩ ở các mô hình có hỗ trợ
        except TypeError: p = tok.apply_chat_template(m, add_generation_prompt=True, tokenize=False)
        t1 = time.time(); tl = generate(model, tok, prompt=p, max_tokens=TOI_DA[d['nhiem_vu']], verbose=False)
        f.write(json.dumps({'id': d['id'], 'tra_loi': tl, 'giay': round(time.time() - t1, 1)}, ensure_ascii=False) + '\n'); f.flush(); n += 1
        if n % 10 == 0: print(f'{n + len(xong)}/{len(D)} mục, {round((time.time() - t0) / n, 1)} giây mỗi mục', flush=True)
print('xong', a.ra)
