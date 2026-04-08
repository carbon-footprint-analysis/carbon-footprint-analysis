import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

nb = json.load(open('notebooks/02_eda_analysis.ipynb', encoding='utf-8'))

for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    ec = c.get('execution_count')
    print(f"=== CELL idx={i} execution_count={ec} ===")
    print(src[:500])
    print()
