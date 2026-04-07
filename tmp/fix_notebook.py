import json
from pathlib import Path

notebook_path = Path('notebooks/01_build_dataset_generation_config.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell ID: Ixd5aQStdNlo - category_map and normalization
for cell in nb['cells']:
    if cell.get('metadata', {}).get('id') == 'Ixd5aQStdNlo':
        cell['source'] = [
            "category_map = {\n",
            "    'comercial': 'commercial',\n",
            "    'industrial': 'industrial',\n",
            "    'outros': 'other',\n",
            "    'residencial': 'residential',\n",
            "    'rural': 'agriculture'\n",
            "}\n",
            "\n",
            "def normalize_classe(df, col):\n",
            "    df[col] = df[col].astype(str).str.lower().replace(category_map)\n",
            "\n",
            "normalize_classe(profiles, 'usage_type')\n",
            "normalize_classe(company_size_dist, 'Classe')\n",
            "normalize_classe(seasonality, 'Classe')\n",
            "\n",
            "usage_distribution_by_state.columns = [category_map.get(c.lower(), c.lower()) for c in usage_distribution_by_state.columns]"
        ]
        print("Updated normalization cell.")

    # Cell ID: -B18U24GVCHv - sample_company_size
    if cell.get('metadata', {}).get('id') == '-B18U24GVCHv':
        cell['source'] = [
            "def sample_company_size(usage_type):\n",
            "\n",
            "    subset = company_size_dist[company_size_dist['Classe'] == usage_type]\n",
            "\n",
            "    if subset.empty:\n",
            "        return 'small'\n",
            "\n",
            "    if len(subset) == 1:\n",
            "        return subset['company_size'].iloc[0]\n",
            "\n",
            "    # Renormalize probabilities\n",
            "    probs = subset['probability']\n",
            "    probs = probs / probs.sum()\n",
            "\n",
            "    return np.random.choice(\n",
            "        subset['company_size'],\n",
            "        p=probs\n",
            "    )"
        ]
        print("Updated sample_company_size cell.")

    # Update path cell - v2_energy _source_distribution
    if any('energy _source' in line for line in cell['source']):
        cell['source'] = [line.replace('energy _source', 'energy_source') for line in cell['source']]
        print("Updated energy_source path typo.")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
