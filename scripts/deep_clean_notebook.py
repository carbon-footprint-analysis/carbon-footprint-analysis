import json
import os
import re

NB_PATH = 'notebooks/01_build_dataset_generation_config.ipynb'

# Labels to replace (including variations with quotes)
REPLACEMENTS = {
    r"(['\"])agriculture(['\"])": r"\1rural\2",
    r"(['\"])commercial(['\"])": r"\1comercial\2",
    r"(['\"])other(['\"])": r"\1outros\2",
    r"(['\"])residential(['\"])": r"\1residencial\2",
    r"(['\"])hydro(['\"])": r"\1hidrelétrica\2",
    r"(['\"])thermal(['\"])": r"\1térmica\2",
    r"(['\"])wind(['\"])": r"\1eólica\2",
}

# Specific mappings that need inversion or correction
# map_usage was mapping 'Industrial': 'industrial' (correct) but 'Comercial': 'commercial' (wrong now)
USAGE_MAP_REPLACEMENT = """map_usage = {
    'Industrial': 'industrial',
    'Comercial':  'comercial',
    'Residencial': 'residencial',
    'Rural':      'rural',
    'Outros':     'outros'
}"""

def deep_clean():
    if not os.path.exists(NB_PATH):
        print(f"Error: {NB_PATH} not found.")
        return

    with open(NB_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    clean_count = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            
            # Convert list of lines to single string for regex replacement
            if isinstance(source, list):
                source_str = "".join(source)
            else:
                source_str = source

            original = source_str
            
            # 1. Apply general label replacements
            for pattern, repl in REPLACEMENTS.items():
                source_str = re.sub(pattern, repl, source_str)

            # 2. Fix specific map_usage definition if found
            if "map_usage = {" in source_str and "'Industrial': 'industrial'" in source_str:
                source_str = re.sub(r"map_usage = \{.*?\n\}", USAGE_MAP_REPLACEMENT, source_str, flags=re.DOTALL)

            if source_str != original:
                # Convert back to list of lines if it was a list
                if isinstance(source, list):
                    # Keep same line break structure if possible, but simplest is to split by \n
                    cell['source'] = [line + "\n" for line in source_str.splitlines()]
                    # Remove the extra \n from the last line if it didn't have one
                    if not source_str.endswith("\n") and cell['source']:
                        cell['source'][-1] = cell['source'][-1].rstrip("\n")
                else:
                    cell['source'] = source_str
                clean_count += 1

    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"✓ Deep clean complete. {clean_count} cells updated in {NB_PATH}")

if __name__ == "__main__":
    deep_clean()
