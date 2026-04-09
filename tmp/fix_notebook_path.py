import json

nb_path = r'notebooks\03_model_preparation.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

OLD = "carbon_footprint_data.csv"
NEW_PATH = "os.path.join('..', 'data', 'processed', 'synthetic_energy_emissions_dataset.csv')"

fixes = 0
for cell in nb['cells']:
    if cell.get('cell_type') != 'code':
        continue
    src = cell.get('source', [])
    new_src = []
    changed = False
    for line in src:
        if OLD in line:
            # Replace the whole os.path.join call
            import re
            line = re.sub(
                r"os\.path\.join\([^)]+carbon_footprint_data\.csv[^)]*\)",
                NEW_PATH,
                line
            )
            changed = True
            fixes += 1
        new_src.append(line)
    if changed:
        cell['source'] = new_src
        cell['outputs'] = []
        cell['execution_count'] = None
        print(f"  Fixed cell. New source snippet: {new_src}")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'Fixed {fixes} line(s). Done.')
