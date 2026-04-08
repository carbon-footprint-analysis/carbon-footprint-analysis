import json
import os
import re

NB_PATH = 'notebooks/01_build_dataset_generation_config.ipynb'

# Case-sensitive mapping for targets that should be lowercase
TARGET_FIXES = {
    r":\s*['\"]Industrial['\"]": ": 'industrial'",
    r":\s*['\"]Comercial['\"]":  ": 'comercial'",
    r":\s*['\"]Outros['\"]":     ": 'outros'",
    r":\s*['\"]Residencial['\"]": ": 'residencial'",
    r":\s*['\"]Rural['\"]":       ": 'rural'",
}

# Any remaining English to Portuguese mapping
ENGLISH_TO_PT = {
    r"(['\"])agriculture(['\"])": r"\1rural\2",
    r"(['\"])commercial(['\"])": r"\1comercial\2",
    r"(['\"])other(['\"])": r"\1outros\2",
    r"(['\"])residential(['\"])": r"\1residencial\2",
}

def fix_generation_logic():
    if not os.path.exists(NB_PATH):
        print(f"Error: {NB_PATH} not found.")
        return

    with open(NB_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    clean_count = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                source_str = "".join(source)
            else:
                source_str = source

            original = source_str
            
            # 1. Fix capitalized targets in mappings
            for pattern, repl in TARGET_FIXES.items():
                source_str = re.sub(pattern, repl, source_str)
            
            # 2. Convert any remaining English labels to Portuguese
            for pattern, repl in ENGLISH_TO_PT.items():
                source_str = re.sub(pattern, repl, source_str)

            # 3. Handle capitalized source keys if they are the ONLY key (e.g. 'Industrial': 'industrial')
            # This is safer than a global swap
            source_str = source_str.replace("'Industrial': 'industrial'", "'industrial': 'industrial'")
            source_str = source_str.replace("'Comercial':  'comercial'", "'comercial': 'comercial'")
            source_str = source_str.replace("'Residencial':'residencial'", "'residencial': 'residencial'")

            if source_str != original:
                if isinstance(source, list):
                    cell['source'] = [line + "\n" for line in source_str.splitlines()]
                    if not source_str.endswith("\n") and cell['source']:
                        cell['source'][-1] = cell['source'][-1].rstrip("\n")
                else:
                    cell['source'] = source_str
                clean_count += 1

    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"✓ Generation logic fixed. {clean_count} cells updated in {NB_PATH}")

if __name__ == "__main__":
    fix_generation_logic()
