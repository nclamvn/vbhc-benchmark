"""Domain mẫu 300 thực thể (đủ cả claim toàn văn) để chạy bites nhanh; cùng engine, cùng gate."""
import json, os, shutil, random, sys
src, dst = sys.argv[1], sys.argv[2]
if os.path.exists(dst): shutil.rmtree(dst)
os.makedirs(os.path.join(dst, 'snapshots'))
claims = [json.loads(l) for l in open(os.path.join(src, 'claims.jsonl'), encoding='utf-8')]
withft = sorted({c['entity'] for c in claims if c['capture']['source'].startswith('datafiles')})
others = sorted({c['entity'] for c in claims} - set(withft))
rng = random.Random(7); pick = set(rng.sample(withft, min(150, len(withft))) + rng.sample(others, 150))
sub = [c for c in claims if c['entity'] in pick]
for s in {c['capture']['snapshot'] for c in sub}: shutil.copy(os.path.join(src, 'snapshots', s), os.path.join(dst, 'snapshots', s))
y = open(os.path.join(src, 'domain.yaml'), encoding='utf-8').read().replace('domain: vbhc_chinhphu', 'domain: vbhc_chinhphu_sample').replace('estimate: 20253', f'estimate: {len(pick)}').replace('basis: "', 'basis: "Mẫu 300 thực thể rút từ domain đầy đủ (seed 7); ')
open(os.path.join(dst, 'domain.yaml'), 'w', encoding='utf-8').write(y)
open(os.path.join(dst, 'claims.jsonl'), 'w', encoding='utf-8').write(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in sub))
print('sample entities', len(pick), 'claims', len(sub))
