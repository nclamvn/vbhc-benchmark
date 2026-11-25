"""Chạy một mô hình trên bộ kiểm tra VBHC-Bench bằng MLX (máy Mac Apple Silicon).
CHƯA CHẠY THỬ trên máy thật: viết theo giao diện mlx_lm đã công bố (load, generate). Nếu báo lỗi tham số, gửi lại dòng lỗi.
Dùng:  python3 scripts/chay_mlx.py --model <tên hoặc đường dẫn mô hình MLX> --ra ket_qua/<ten>.jsonl [--adapter adapters/vbhc] [--gioi-han 20]
       [--nhiem-vu T1] [--phat-lap 1.1]   (giao thức 1.2: phạt lặp khi giải mã, xem QĐ-13; mặc định giải mã tham lam như 1.1)
Chạy lại cùng lệnh sẽ tiếp tục từ mục còn thiếu."""
import argparse, json, os, sys, time
from mlx_lm import load, generate
ap = argparse.ArgumentParser(); ap.add_argument('--model', required=True); ap.add_argument('--ra', required=True)
ap.add_argument('--adapter'); ap.add_argument('--de', default='m3/test_de.jsonl'); ap.add_argument('--gioi-han', type=int, default=0)
ap.add_argument('--nhiem-vu', default=''); ap.add_argument('--phat-lap', type=float, default=0); ap.add_argument('--cua-so-lap', type=int, default=64); ap.add_argument('--chan-lap-khoi', action='store_true')
ap.add_argument('--tra-cuu', action='store_true', help='giao thức 2.0: T1 kèm tư liệu tra cứu (scripts/tra_cuu.py)')
a = ap.parse_args(); os.makedirs(os.path.dirname(a.ra) or '.', exist_ok=True)
D = [json.loads(l) for l in open(a.de, encoding='utf-8')]
if a.gioi_han:  # lấy đều ba nhiệm vụ để thử nhanh
    D = [x for nv in ['T1', 'T2', 'T3'] for x in [d for d in D if d['nhiem_vu'] == nv][:a.gioi_han]]
if a.nhiem_vu: D = [d for d in D if d['nhiem_vu'] in a.nhiem_vu.split(',')]
if a.tra_cuu:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tra_cuu; TC = tra_cuu.TraCuu()
    for d in D:
        if d['nhiem_vu'] == 'T1': d['de'] = tra_cuu.lam_giau_de(d['de'], TC, 8)
xong = {json.loads(l)['id'] for l in open(a.ra, encoding='utf-8')} if os.path.exists(a.ra) else set()
model, tok = load(a.model, adapter_path=a.adapter) if a.adapter else load(a.model)
TOI_DA = {'T1': 1800, 'T2': 48, 'T3': 320}; t0 = time.time(); n = 0
THEM = {}
if a.phat_lap:
    from mlx_lm.sample_utils import make_logits_processors
    THEM['logits_processors'] = make_logits_processors(repetition_penalty=a.phat_lap, repetition_context_size=a.cua_so_lap)
with open(a.ra, 'a', encoding='utf-8') as f:
    for d in D:
        if d['id'] in xong: continue
        m = [{'role': 'system', 'content': d['he_thong']}, {'role': 'user', 'content': d['de']}]
        p = None
        for mm in (m, [{'role': 'user', 'content': d['he_thong'] + '\n\n' + d['de']}]):   # mẫu không nhận vai system (một số bản Gemma): gộp vào lời người dùng
            try: p = tok.apply_chat_template(mm, add_generation_prompt=True, tokenize=False, enable_thinking=False); break   # tắt chế độ suy nghĩ ở mô hình có hỗ trợ
            except TypeError:
                try: p = tok.apply_chat_template(mm, add_generation_prompt=True, tokenize=False); break
                except Exception: continue
            except Exception: continue
        t1 = time.time()
        if a.chan_lap_khoi and d['nhiem_vu'] == 'T1':   # giao thức 1.3: dừng khi lặp nguyên đoạn (scripts/chan_lap.py)
            from mlx_lm import stream_generate
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from chan_lap import khoi_lap
            tl = ''
            for r in stream_generate(model, tok, p, max_tokens=TOI_DA[d['nhiem_vu']], **THEM):
                tl += r.text
                if '\n' in r.text:
                    c = khoi_lap(tl)
                    if c is not None: tl = tl[:c]; break
        else:
            tl = generate(model, tok, prompt=p, max_tokens=TOI_DA[d['nhiem_vu']], verbose=False, **THEM)
        f.write(json.dumps({'id': d['id'], 'tra_loi': tl, 'giay': round(time.time() - t1, 1)}, ensure_ascii=False) + '\n'); f.flush(); n += 1
        if n % 10 == 0: print(f'{n + len(xong)}/{len(D)} mục, {round((time.time() - t0) / n, 1)} giây mỗi mục', flush=True)
print('xong', a.ra)
