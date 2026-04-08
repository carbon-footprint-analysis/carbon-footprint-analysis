import json
import os
import re

def thorough_fix(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple string-based check first to avoid JSON overhead if not needed
        target_patterns = [
            'consumo_energia_emissoes_br.xlsx',
            'pd.read_excel',
            '../data/raw/consumo_energia'
        ]
        
        if not any(p in content for p in target_patterns):
            print(f"SKIPPING: {path} (No target patterns found)")
            return

        nb = json.loads(content)
        changed = False
        
        github_url = "https://raw.githubusercontent.com/carbon-footprint-analysis/carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv"
        
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = cell.get('source')
                if isinstance(source, list):
                    source_str = "".join(source)
                else:
                    source_str = source
                
                new_source = source_str
                
                # Replace local legacy paths with GitHub URL and use read_csv
                # Pattern 1: Any path to consumo_energia_emissoes_br.xlsx
                pattern = r"['\"][^'\"]*consumo_energia_emissoes_br\.xlsx['\"]"
                if re.search(pattern, new_source):
                    new_source = re.sub(pattern, f"'{github_url}'", new_source)
                    new_source = new_source.replace('read_excel', 'read_csv')
                    print(f"  REPLACED Excel path in {path}")
                    changed = True
                
                # Pattern 2: Fixing the os.path.join mess (already caught by previous script but being thorough)
                if "os.path.join" in new_source and "https://raw.githubusercontent.com" in new_source:
                    new_source = re.sub(r"data_path\s*=\s*os\.path\.join\([^)]*'(https://[^']*)'[^)]*\)", r"data_path = '\1'", new_source)
                    print(f"  FIXED os.path.join in {path}")
                    changed = True

                # Pattern 3: If read_csv is used but still pointing to raw local xlsx (unlikely but possible)
                if "../data/raw/consumo_energia_emissoes_br" in new_source:
                    new_source = new_source.replace("../data/raw/consumo_energia_emissoes_br.csv", github_url)
                    new_source = new_source.replace("../data/raw/consumo_energia_emissoes_br.xlsx", github_url)
                    new_source = new_source.replace('read_excel', 'read_csv')
                    print(f"  NORMALIZED legacy path in {path}")
                    changed = True

                if changed:
                    # Update cell source
                    if isinstance(source, list):
                        cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in new_source.splitlines()]
                    else:
                        cell['source'] = new_source

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
            print(f"SAVED: {path}")
        else:
            print(f"NO CHANGES APPLIED: {path}")

    except Exception as e:
        print(f"ERROR processing {path}: {str(e)}")

notebooks_dir = 'notebooks'
for f in os.listdir(notebooks_dir):
    if f.endswith('.ipynb'):
        thorough_fix(os.path.join(notebooks_dir, f))
