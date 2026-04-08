import json
import os

repo_root = '.'
github_url = 'https://raw.githubusercontent.com/carbon-footprint-analysis/carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv'

# Paths that might be present in older versions
old_paths = [
    '../data/processed/synthetic_energy_emissions_dataset.csv',
    '../data/raw/consumo_energia_emissoes_br.xlsx',
    '../data/raw/consumo_energia_emissoes_br.csv'
]

for root, dirs, files in os.walk(repo_root):
    for filename in files:
        if filename.endswith('.ipynb'):
            path = os.path.join(root, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    nb = json.load(f)
                
                updated = False
                for cell in nb.get('cells', []):
                    if cell.get('cell_type') == 'code':
                        source = cell.get('source')
                        if isinstance(source, list):
                            source_str = "".join(source)
                        else:
                            source_str = source
                        
                        modified_source = source_str
                        for old_p in old_paths:
                            if old_p in modified_source:
                                modified_source = modified_source.replace(old_p, github_url)
                                # Also fix read_excel to read_csv if needed
                                if '.xlsx' in old_p and 'read_excel' in modified_source:
                                    modified_source = modified_source.replace('read_excel', 'read_csv')
                                    # Add .drop(columns=['Unnamed: 0'], errors='ignore') if updating from xlsx to csv
                                    # But let's keep it simple for now as the current CSV might not have that index issues in the same way
                                
                                updated = True
                        
                        if updated:
                            if isinstance(source, list):
                                cell['source'] = [line + ("\n" if not line.endswith("\n") else "") for line in modified_source.splitlines()]
                            else:
                                cell['source'] = modified_source
                
                if updated:
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(nb, f, ensure_ascii=False, indent=1)
                    print(f"Updated {path}")
            except Exception as e:
                print(f"Error processing {path}: {e}")
