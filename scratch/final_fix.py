import json
import os

def fix_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    changed = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source')
            if isinstance(source, list):
                source_str = "".join(source)
            else:
                source_str = source
            
            new_source = source_str
            # Fix 1: os.path.join with URL
            if "os.path.join" in new_source and "https://raw.githubusercontent.com" in new_source:
                # Replace the whole data_path line or just the join
                import re
                new_source = re.sub(r"data_path\s*=\s*os\.path\.join\([^)]*'(https://[^']*)'[^)]*\)", r"data_path = '\1'", new_source)
                if new_source != source_str:
                    changed = True

            # Fix 2: Legend legacy Excel path
            old_excel_path = '../data/raw/consumo_energia_emissoes_br.xlsx'
            github_url = 'https://raw.githubusercontent.com/carbon-footprint-analysis/carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv'
            if old_excel_path in new_source:
                new_source = new_source.replace(old_excel_path, github_url)
                new_source = new_source.replace('read_excel', 'read_csv')
                # Add drop unnamed column if not present
                if 'drop(columns=[' not in new_source:
                    new_source = new_source.replace('pd.read_csv(caminho_dados)', "pd.read_csv(caminho_dados).drop(columns=['Unnamed: 0'], errors='ignore')")
                changed = True

            if changed:
                if isinstance(source, list):
                    cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in new_source.splitlines()]
                else:
                    cell['source'] = new_source

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"FIXED: {path}")
    else:
        print(f"NO CHANGES: {path}")

notebooks_dir = 'notebooks'
for f in os.listdir(notebooks_dir):
    if f.endswith('.ipynb'):
        fix_notebook(os.path.join(notebooks_dir, f))
