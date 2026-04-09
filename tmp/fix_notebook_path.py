import json

nb_path = r'notebooks\03_model_preparation.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell.get('cell_type') == 'code':
        src = cell.get('source', [])
        new_src = []
        changed = False
        for line in src:
            if 'carbon_footprint_data.csv' in line:
                old = "os.path.join('..', 'data', 'carbon_footprint_data.csv')"
                new = "os.path.join('..', 'data', 'processed', 'synthetic_energy_emissions_dataset.csv')"
                line = line.replace(old, new)
                changed = True
            new_src.append(line)
        if changed:
            cell['source'] = new_src
            cell['outputs'] = []
            cell['execution_count'] = None
            print('Fixed cell source and cleared outputs.')

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done.')
