import json
import os

notebook_path = r'notebooks/02_eda_analysis.ipynb'
github_url = 'https://raw.githubusercontent.com/carbon-footprint-analysis/carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv'

if not os.path.exists(notebook_path):
    print(f"Error: {notebook_path} not found.")
    exit(1)

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

old_path = '../data/processed/synthetic_energy_emissions_dataset.csv'

updated = False
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell.get('source')
        if isinstance(source, list):
            source_str = "".join(source)
        else:
            source_str = source
        
        if old_path in source_str:
            new_source = source_str.replace(old_path, github_url)
            if isinstance(source, list):
                # Ensure each line ends with \n for nbformat-like consistency
                lines = new_source.splitlines()
                # If the original was a list, it usually had \n at the end of each string
                cell['source'] = [line + "\n" for line in lines]
                # Fix the last line if it didn't have a newline originally
                if not source_str.endswith("\n") and cell['source']:
                    cell['source'][-1] = cell['source'][-1].rstrip("\n")
            else:
                cell['source'] = new_source
            updated = True
            print("OK: Updated caminho_dados in notebook.")

if updated:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Notebook saved successfully.")
else:
    print("No changes needed in notebook.")
