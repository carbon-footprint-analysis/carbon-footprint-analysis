import json

notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\01_build_dataset_generation_config.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell and replace its source
found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        if "assert set(company_size_dist['Classe'].unique()) <= {'comercial'" in source:
            new_source = [
                "# Padronizar para minúsculo\n",
                "profiles['usage_type'] = profiles['usage_type'].str.strip().str.lower()\n",
                "company_size_dist['Classe'] = company_size_dist['Classe'].str.strip().str.lower()\n",
                "seasonality['Classe'] = seasonality['Classe'].str.strip().str.lower()\n",
                "\n",
                "# Verificação de consistência:\n",
                "\n",
                "assert set(profiles['usage_type'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\\n",
                "    f\"usage_type inesperado em profiles: {set(profiles['usage_type'].unique())}\"\n",
                "\n",
                "assert set(company_size_dist['Classe'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\\n",
                "    f\"Classe inesperada em company_size_dist: {set(company_size_dist['Classe'].unique())}\"\n",
                "\n",
                "assert set(seasonality['Classe'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\\n",
                "    f\"Classe inesperada em seasonality: {set(seasonality['Classe'].unique())}\"\n",
                "\n",
                "setores_state = set(usage_distribution_by_state.columns)\n",
                "setores_profiles = set(profiles['usage_type'].unique())\n",
                "assert setores_state == setores_profiles, \\\n",
                "    f\"Mismatch setores: state={setores_state} | profiles={setores_profiles}\"\n",
                "\n",
                "print(\"✓ Todas as categorias estão consistentes em PT-BR\")\n",
                "print(\"  Setores:\", sorted(setores_profiles))\n",
                "print(\"  Fontes:\", sorted(energy_dist['energy_source'].unique()))\n",
                "print(\"  Portes:\", sorted(company_size_dist['company_size'].unique()))\n"
            ]
            cell['source'] = new_source
            found = True
            break

if found:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook fixed.")
else:
    print("Cell not found.")
