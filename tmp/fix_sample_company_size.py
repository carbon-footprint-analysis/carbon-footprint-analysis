import json

nb = json.load(open('notebooks/01_build_dataset_generation_config.ipynb', encoding='utf-8'))
cells = nb['cells']

new_func_lines = [
    'def sample_company_size(usage_type):\n',
    '    """\n',
    '    Sample a company size for the given usage_type.\n',
    '    Falls back to \'small\' if no matching category is found.\n',
    '    Defensive: uses .values arrays to avoid pandas/numpy Series issues.\n',
    '    """\n',
    '    subset = company_size_dist[company_size_dist[\'Classe\'] == usage_type].copy()\n',
    '\n',
    '    if subset.empty:\n',
    '        # No match found - normalization mismatch or missing category; default to \'small\'\n',
    '        return \'small\'\n',
    '\n',
    '    sizes = subset[\'company_size\'].values\n',
    '    probs = subset[\'probability\'].values.astype(float)\n',
    '\n',
    '    if len(sizes) == 0:\n',
    '        return \'small\'\n',
    '\n',
    '    # Re-normalize probabilities to guard against floating-point rounding\n',
    '    total = probs.sum()\n',
    '    if total <= 0:\n',
    '        return \'small\'\n',
    '    probs = probs / total\n',
    '\n',
    '    return np.random.choice(sizes, p=probs)\n',
]

updated = 0
for i, c in enumerate(cells):
    if c['cell_type'] == 'code' and 'def sample_company_size' in ''.join(c['source']):
        cells[i]['source'] = new_func_lines
        print(f'Updated cell {i}')
        updated += 1

if updated == 0:
    print('WARNING: sample_company_size cell not found!')
else:
    with open('notebooks/01_build_dataset_generation_config.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print('Notebook saved successfully')
