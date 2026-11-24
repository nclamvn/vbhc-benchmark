"""Chạy một mô hình (có thể kèm adapter LoRA) trên bộ kiểm tra VBHC-Bench, CPU, giải mã tham lam (không lấy mẫu).
Giới hạn token sinh: T1 1000, T2 48, T3 320 (giống nhau cho mọi mô hình trong lượt chạy CPU). Chạy lại sẽ tiếp tục.
Dùng: python3 chay_cpu.py <tệp ra> [thư mục adapter]"""
import json, os, sys, time, torch, gc
from transformers import AutoTokenizer, AutoModelForCausalLM
torch.set_num_threads(2); BASE = 'qwen25_05b'; ra = sys.argv[1]; ad = sys.argv[2] if len(sys.argv) > 2 else None
TOI_DA = {'T1': 1000, 'T2': 48, 'T3': 320}
D = [json.loads(l) for l in open('/home/claude/vbhc/m3/test_de.jsonl', encoding='utf-8')]
D.sort(key=lambda d: {'T2': 0, 'T3': 1, 'T1': 2}[d['nhiem_vu']])
xong = {json.loads(l)['id'] for l in open(ra, encoding='utf-8')} if os.path.exists(ra) else set()
tok = AutoTokenizer.from_pretrained(BASE); m = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32)
if ad:
    from peft import PeftModel
    m = PeftModel.from_pretrained(m, ad); m = m.merge_and_unload()
m.eval(); t0 = time.time(); n = 0
with open(ra, 'a', encoding='utf-8') as f:
    for d in D:
        if d['id'] in xong: continue
        p = tok.apply_chat_template([{'role': 'system', 'content': d['he_thong']}, {'role': 'user', 'content': d['de']}], add_generation_prompt=True, tokenize=False)
        ids = tok(p, return_tensors='pt', add_special_tokens=False)['input_ids']; t1 = time.time()
        with torch.no_grad(): out = m.generate(ids, max_new_tokens=TOI_DA[d['nhiem_vu']], do_sample=False, repetition_penalty=1.05)
        tl = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
        f.write(json.dumps({'id': d['id'], 'tra_loi': tl, 'giay': round(time.time() - t1, 1), 'token_vao': ids.shape[1], 'token_ra': out.shape[1] - ids.shape[1]}, ensure_ascii=False) + '\n'); f.flush(); n += 1
        del out, ids; gc.collect()
        if n % 10 == 0: print(f'{n + len(xong)}/{len(D)} | {(time.time() - t0) / n:.1f} giây/mục', flush=True)
print('xong', ra, flush=True)
