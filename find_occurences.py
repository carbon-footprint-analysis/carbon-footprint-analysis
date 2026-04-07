import json

notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\01_build_dataset_generation_config.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'usage_distribution_by_state' in source:
            print(f"Cell {i} contains 'usage_distribution_by_state':")
            print(source)
            print("-" * 20)
        if 'pd.read_csv' in source and 'v2_consumption_profiles.csv' in source:
            print(f"Cell {i} re-loads profiles:")
            print(source)
            print("-" * 20)
