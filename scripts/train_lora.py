"""M4 · Tinh chỉnh LoRA Qwen2.5-0.5B-Instruct trên tập huấn luyện VBHC (m3/train.jsonl), chạy CPU.
Mất mát chỉ tính trên phần trả lời của trợ lý. Văn bản dài bị cắt ở giữa để vừa MAX_LEN token.
Lưu điểm kiểm tra mỗi SAVE bước; chạy lại cùng lệnh sẽ tiếp tục từ điểm gần nhất.
Dùng: python3 train_lora.py <số bước> [chỉ đo: --do]"""
import json, random, sys, time, os, math, torch, gc
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, PeftModel
torch.manual_seed(0); torch.set_num_threads(2)
BASE = 'qwen25_05b'; MAX_LEN = 1024; LR = 2e-4; ACC = 4; SAVE = 20; OUT = 'adapter'
tok = AutoTokenizer.from_pretrained(BASE)
def ma_hoa(ex):
    m = ex['messages']; sys_, user, asst = m[0]['content'], m[1]['content'], m[2]['content']
    a_ids = tok(asst + '<|im_end|>\n', add_special_tokens=False)['input_ids'][:900]
    for _ in range(8):
        p = tok.apply_chat_template([{'role': 'system', 'content': sys_}, {'role': 'user', 'content': user}], add_generation_prompt=True, tokenize=False)
        p_ids = tok(p, add_special_tokens=False)['input_ids']
        if len(p_ids) + len(a_ids) <= MAX_LEN: break
        du = len(p_ids) + len(a_ids) - MAX_LEN; c = int(du * 3.2) + 200   # cắt ở giữa phần văn bản, giữ đầu và cuối
        if 'VĂN BẢN:\n' in user:
            h, t = user.split('VĂN BẢN:\n', 1); k = max(400, len(t) - c); user = h + 'VĂN BẢN:\n' + t[:int(k * .7)] + '\n[...]\n' + t[len(t) - int(k * .3):]
        else: user = user[:max(300, len(user) - c)]
    ids = (p_ids + a_ids)[:MAX_LEN]; lab = ([-100] * len(p_ids) + a_ids)[:MAX_LEN]
    return torch.tensor([ids]), torch.tensor([lab])
TR = [json.loads(l) for l in open('/home/claude/vbhc/m3/train.jsonl', encoding='utf-8')]
VA = [json.loads(l) for l in open('/home/claude/vbhc/m3/valid.jsonl', encoding='utf-8')]
# T1: chỉ giữ ví dụ mà cả yêu cầu lẫn văn bản trả lời vừa MAX_LEN, để mô hình học trọn văn bản kể cả phần kết, không học bản bị cắt cụt
def dai_tra_loi(ex): return len(tok(ex['messages'][1]['content'] + ex['messages'][2]['content'], add_special_tokens=False)['input_ids']) + 40 - MAX_LEN + 650
_n0 = len(TR); TR = [ex for ex in TR if not ex['messages'][1]['content'].startswith('Soạn hoàn chỉnh') or dai_tra_loi(ex) <= 650]
VA = [ex for ex in VA if not ex['messages'][1]['content'].startswith('Soạn hoàn chỉnh') or dai_tra_loi(ex) <= 650]
print('tap huan luyen sau loc', len(TR), '/', _n0, flush=True)
random.Random(0).shuffle(TR)
model = AutoModelForCausalLM.from_pretrained(BASE, dtype=torch.float32); model.config.use_cache = False
model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
if os.path.exists(f'{OUT}/trang_thai.json'):
    st = json.load(open(f'{OUT}/trang_thai.json')); model = PeftModel.from_pretrained(model, OUT, is_trainable=True)
else:
    st = {'buoc': 0, 'nhat_ky': []}
    model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'], task_type='CAUSAL_LM'))
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=LR, weight_decay=0.0)
if os.path.exists(f'{OUT}/opt.pt'): opt.load_state_dict(torch.load(f'{OUT}/opt.pt'))
BASEM = model.get_base_model()
def mat_mat(x, y):  # chỉ đưa vị trí trả lời qua lm_head: tiết kiệm bộ nhớ (từ vựng 151.936)
    h = BASEM.model(input_ids=x).last_hidden_state[0]; pos = (y[0, 1:] != -100).nonzero().squeeze(1)
    return torch.nn.functional.cross_entropy(BASEM.lm_head(h[pos]).float(), y[0, 1:][pos])
TONG = int(sys.argv[1]); chi_do = '--do' in sys.argv
def lr_at(b): return LR * min(1, (b + 1) / 10) * (0.5 * (1 + math.cos(math.pi * min(1, b / max(1, TONG)))) * 0.9 + 0.1)
def mat_mat_tham_dinh(n=20):
    model.eval(); L = []
    with torch.no_grad():
        for ex in VA[:n]:
            x, y = ma_hoa(ex); L.append(mat_mat(x, y).item())
    model.train(); return round(sum(L) / len(L), 4)
model.train(); t0 = time.time(); han = time.time() + float(os.environ.get('HAN_GIAY', '540'))
if st['buoc'] == 0 and not chi_do: st['nhat_ky'].append({'buoc': 0, 'val_loss': mat_mat_tham_dinh()}); print('val ban dau', st['nhat_ky'][-1], flush=True)
while st['buoc'] < TONG and time.time() < han:
    b = st['buoc']; tl = 0.0; nt = 0
    for g in opt.param_groups: g['lr'] = lr_at(b)
    for k in range(ACC):
        x, y = ma_hoa(TR[(b * ACC + k) % len(TR)]); loss = mat_mat(x, y) / ACC; loss.backward(); tl += loss.item(); nt += x.shape[1]; del loss; gc.collect()
    torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0); opt.step(); opt.zero_grad(); st['buoc'] += 1
    print(f"buoc {st['buoc']}/{TONG} loss {tl:.4f} lr {lr_at(b):.2e} token {nt} | {time.time() - t0:.0f}s", flush=True)
    st['nhat_ky'].append({'buoc': st['buoc'], 'loss': round(tl, 4)})
    if chi_do and st['buoc'] >= TONG: sys.exit(0)
    if st['buoc'] % SAVE == 0 or st['buoc'] == TONG:
        if st['buoc'] % 50 == 0 or st['buoc'] == TONG: st['nhat_ky'].append({'buoc': st['buoc'], 'val_loss': mat_mat_tham_dinh()}); print('val', st['nhat_ky'][-1], flush=True)
        model.save_pretrained(OUT); torch.save(opt.state_dict(), f'{OUT}/opt.pt'); json.dump(st, open(f'{OUT}/trang_thai.json', 'w'))
model.save_pretrained(OUT); torch.save(opt.state_dict(), f'{OUT}/opt.pt'); json.dump(st, open(f'{OUT}/trang_thai.json', 'w')); print('dung o buoc', st['buoc'])
