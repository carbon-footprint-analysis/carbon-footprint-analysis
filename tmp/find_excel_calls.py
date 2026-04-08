import json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = r'c:\Repositorio\carbon-footprint-analysis\notebooks'

for fname in os.listdir(root):
    if not fname.endswith('.ipynb'):
        continue
    path = os.path.join(root, fname)
    nb = json.load(open(path, encoding='utf-8'))
    for i, c in enumerate(nb['cells']):
        src = ''.join(c['source'])
        if 'read_excel' in src or 'df_gerado_teste' in src or ('../notebooks' in src and 'csv' in src):
            print(f"FOUND in {fname} Cell idx={i}:")
            print(src[:500])
            print()
