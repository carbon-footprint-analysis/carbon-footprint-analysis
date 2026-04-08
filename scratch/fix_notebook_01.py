import json

nb_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\01_build_dataset_generation_config.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

old_line = "df.to_csv('https://raw.githubusercontent.com/carbon-footprint-analysis/carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv')"
new_line = "df.to_csv('../data/processed/synthetic_energy_emissions_dataset.csv')"

found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if isinstance(source, list):
            for i, line in enumerate(source):
                if old_line in line:
                    source[i] = line.replace(old_line, new_line)
                    found = True
        elif isinstance(source, str):
            if old_line in source:
                cell['source'] = source.replace(old_line, new_line)
                found = True

if found:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Notebook updated successfully.")
else:
    print("Target line not found.")
