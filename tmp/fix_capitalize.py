import json

nb = json.load(open('notebooks/01_build_dataset_generation_config.ipynb', encoding='utf-8'))

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'capitalize' in src:
        cell_id = cell.get('metadata', {}).get('id', '')
        print(f'=== Cell {i} (id={cell_id}) ===')
        # Fix: remove .capitalize() — usage_class já está em inglês minúsculo
        new_src = src.replace('.capitalize()', '')
        cell['source'] = [new_src]
        print("FIXED:")
        print(new_src)
        print()

with open('notebooks/01_build_dataset_generation_config.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook salvo com correção do .capitalize()")
