import json
import os

notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\01_build_dataset_generation_config.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # 1. Fix map_usage and df_profiles index
        if "map_usage = {" in source and "df_profiles['usage_type']" in source:
            cell['source'] = [
                "df_profiles.index = df_profiles.index.str.lower()\n",
                "\n",
                "map_usage = {\n",
                "    'industrial': 'industrial',\n",
                "    'comercial': 'comercial',\n",
                "    'residencial': 'residencial',\n",
                "    'rural': 'rural',\n",
                "    'outros': 'outros'\n",
                "}\n",
                "\n",
                "df_profiles['usage_type'] = df_profiles.index.map(map_usage)"
            ]
            print("Fixed map_usage cell")

        # 2. Fix usage_distribution_by_state columns
        if "usage_distribution_by_state.columns = [category_map.get" in source:
            cell['source'] = [
                "usage_distribution_by_state = df_sector_state.pivot(\n",
                "    index='UF',\n",
                "    columns='Classe',\n",
                "    values='probability'\n",
                ")\n",
                "\n",
                "usage_distribution_by_state.columns = usage_distribution_by_state.columns.str.lower()"
            ]
            print("Fixed usage_distribution_by_state columns")

        # 3. Fix size_dist Classe lowercase
        if "size_dist =" in source and "value_counts(normalize=True)" in source and "size_dist.to_csv" not in source:
             # Check if it's the one creating size_dist
             if "reset_index(name='probability')" in source:
                 cell['source'].append("\nsize_dist['Classe'] = size_dist['Classe'].str.lower()")
                 print("Fixed size_dist lowercase")

        # 4. Fix monthly_stats Classe lowercase
        if "monthly_stats =" in source and ".agg(['mean','var'])" in source:
             cell['source'].append("\nmonthly_stats['Classe'] = monthly_stats['Classe'].str.lower()")
             print("Fixed monthly_stats lowercase")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
