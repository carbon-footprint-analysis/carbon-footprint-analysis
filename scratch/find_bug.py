import json
import os

repo_root = '.'
target_string = 'consumo_energia_emissoes_br.xlsx'

for root, dirs, files in os.walk(repo_root):
    for filename in files:
        if filename.endswith('.ipynb'):
            path = os.path.join(root, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    nb = json.load(f)
                
                for i, cell in enumerate(nb.get('cells', [])):
                    if cell.get('cell_type') == 'code':
                        source = cell.get('source')
                        if isinstance(source, list):
                            source_str = "".join(source)
                        else:
                            source_str = source
                        
                        if target_string in source_str:
                            print(f"FOUND in {path}, Cell {i}")
                            print("Source snippet:")
                            print(source_str)
                            print("-" * 20)
            except Exception as e:
                pass
