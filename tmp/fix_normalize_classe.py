import json

nb = json.load(open('notebooks/01_build_dataset_generation_config.ipynb', encoding='utf-8'))
cells = nb['cells']

new_norm_lines = [
    'category_map = {\n',
    "    'comercial': 'commercial',\n",
    "    'industrial': 'industrial',\n",
    "    'outros': 'other',\n",
    "    'residencial': 'residential',\n",
    "    'rural': 'agriculture'\n",
    '}\n',
    '\n',
    'def normalize_classe(df, col):\n',
    '    """Normalize Portuguese category names to English lowercase. Uses map() for reliable replacement."""\n',
    "    df[col] = df[col].astype(str).str.lower().map(lambda x: category_map.get(x, x))\n",
    '\n',
    "normalize_classe(profiles, 'usage_type')\n",
    "normalize_classe(company_size_dist, 'Classe')\n",
    "normalize_classe(seasonality, 'Classe')\n",
    '\n',
    "usage_distribution_by_state.columns = [category_map.get(c.lower(), c.lower()) for c in usage_distribution_by_state.columns]\n",
]

updated = 0
for i, c in enumerate(cells):
    if c['cell_type'] == 'code' and 'def normalize_classe' in ''.join(c['source']):
        cells[i]['source'] = new_norm_lines
        print(f'Updated normalize_classe at cell {i}')
        updated += 1

if updated == 0:
    print('WARNING: normalize_classe cell not found!')
else:
    with open('notebooks/01_build_dataset_generation_config.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print('Notebook saved successfully')
