import json
import os

repo_root = '.'
search_str = 'read_excel'

for root, dirs, files in os.walk(repo_root):
    for filename in files:
        if filename.endswith('.ipynb'):
            path = os.path.join(root, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    nb = json.load(f)
                    for i, cell in enumerate(nb.get('cells', [])):
                        source = cell.get('source', [])
                        source_str = "".join(source) if isinstance(source, list) else source
                        if search_str in source_str:
                            print(f"Found '{search_str}' in {path} at cell index {i}")
                            print(f"Source snippet: {source_str[:100]}...")
            except Exception as e:
                pass # Silently skip errors
