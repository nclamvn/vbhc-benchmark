"""Gọi mlx_lm.lora như lệnh gốc, khi kết thúc in bộ nhớ đỉnh do MLX đo ("Peak mem X GB").
Bản mlx_lm mới không còn in dòng này trong bảng huấn luyện. Dùng: python3 scripts/m9_lora.py <các tham số của mlx_lm.lora>"""
import atexit, runpy, sys
import mlx.core as mx
def in_dinh():
    f = getattr(mx, 'get_peak_memory', None) or mx.metal.get_peak_memory
    print(f'Peak mem {f() / 1e9:.2f} GB', flush=True)
atexit.register(in_dinh)
sys.argv = ['mlx_lm.lora'] + sys.argv[1:]
runpy.run_module('mlx_lm.lora', run_name='__main__')
