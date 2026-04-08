import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

nb = json.load(open('notebooks/02_eda_analysis.ipynb', encoding='utf-8'))

for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    print(f"=== CELL idx={i} type={c['cell_type']} ===")
    print(src)
    print()
