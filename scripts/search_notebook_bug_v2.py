import json
import os

notebooks_dir = 'notebooks'
search_str = 'consumo_energia_emissoes_br.xlsx'

for filename in os.listdir(notebooks_dir):
    if filename.endswith('.ipynb'):
        path = os.path.join(notebooks_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                nb = json.load(f)
                for i, cell in enumerate(nb.get('cells', [])):
                    source = cell.get('source', [])
                    source_str = "".join(source) if isinstance(source, list) else source
                    if search_str in source_str:
                        print(f"Found '{search_str}' in {filename} at cell index {i}")
                        print(f"Source snippet: {source_str[:100]}...")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
