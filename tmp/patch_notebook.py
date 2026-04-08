import json

notebook_path = 'c:/Repositorio/carbon-footprint-analysis/notebooks/01_build_dataset_generation_config.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # Fix company size distribution export
        if '../data/processed/v2_company_size_distribution_by_usage.csv' in source and 'to_csv' in source:
            if "size_dist['Classe'] = size_dist['Classe'].str.lower()" not in source:
                cell['source'] = [
                    "# Garantir normalização total antes de salvar\n",
                    "size_dist['Classe'] = size_dist['Classe'].str.lower()\n",
                    "size_dist['company_size'] = size_dist['company_size'].map({'small':'pequena','medium':'média','large':'grande'}).fillna(size_dist['company_size'])\n",
                    "size_dist.to_csv('../data/processed/v2_company_size_distribution_by_usage.csv', index=False)\n"
                ]
            else:
                 # Check if the existing one is complete
                 if "mapping_porte" not in source and "pequena" not in source:
                      cell['source'].insert(0, "size_dist['company_size'] = size_dist['company_size'].map({'small':'pequena','medium':'média','large':'grande'}).fillna(size_dist['company_size'])\n")
        
        # Fix seasonality export
        if '../data/processed/v2_seasonality_state_class_month.csv' in source and 'to_csv' in source:
             if "monthly_stats['Classe'] = monthly_stats['Classe'].str.lower()" not in source:
                 cell['source'].insert(0, "monthly_stats['Classe'] = monthly_stats['Classe'].str.lower()\n")

        # Fix profiles export
        if '../data/processed/v2_consumption_profiles.csv' in source and 'to_csv' in source:
             if "df_export['usage_type'] = df_export['usage_type'].str.lower()" not in source:
                 cell['source'].insert(0, "df_export['usage_type'] = df_export['usage_type'].str.lower()\n")

        # Fix usage by state export
        if '../data/processed/v2_usage_distribution_by_state.csv' in source and 'to_csv' in source:
             if "usage_distribution_by_state.columns = usage_distribution_by_state.columns.str.lower()" not in source:
                 cell['source'].insert(0, "usage_distribution_by_state.columns = usage_distribution_by_state.columns.str.lower()\n")

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook patched successfully.")
