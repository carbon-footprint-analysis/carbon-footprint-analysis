import json
nb = json.load(open('notebooks/01_build_dataset_generation_config.ipynb', encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'capitalize' in src:
        cell_id = cell.get('metadata', {}).get('id', '')
        print(f'=== Cell {i} (id={cell_id}) ===')
        print(src)
        print()
print("DONE")
