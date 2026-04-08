import json
import os

notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\01_build_dataset_generation_config.ipynb'

if not os.path.exists(notebook_path):
    print(f"Error: {notebook_path} not found.")
    exit(1)

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

target_code_search = "profiles = pd.read_csv('../data/processed/v2_consumption_profiles.csv')"

found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if isinstance(source, list):
            source_str = "".join(source)
        else:
            source_str = source
        
        if target_code_search in source_str:
            new_source = [
                "import pandas as pd\n",
                "import numpy as np\n",
                "\n",
                "profiles = pd.read_csv('../data/processed/v2_consumption_profiles.csv')\n",
                "\n",
                "energy_dist = pd.read_csv('../data/processed/v2_energy_source_distribution.csv')\n",
                "\n",
                "emission_df = pd.read_csv('../data/processed/v2_energy_source_emission_factors.csv')\n",
                "\n",
                "usage_distribution_by_state = pd.read_csv(\n",
                "    '../data/processed/v2_usage_distribution_by_state.csv',\n",
                "    index_col=0\n",
                ")\n",
                "\n",
                "company_size_dist = pd.read_csv(\n",
                "    '../data/processed/v2_company_size_distribution_by_usage.csv'\n",
                ")\n",
                "\n",
                "seasonality = pd.read_csv(\n",
                "    '../data/processed/v2_seasonality_state_class_month.csv'\n",
                ")\n",
                "\n",
                "# Normalização de categorias para garantir consistência (PT-BR minúsculo)\n",
                "company_size_dist['Classe'] = company_size_dist['Classe'].str.lower()\n",
                "seasonality['Classe'] = seasonality['Classe'].str.lower()\n",
                "usage_distribution_by_state.columns = usage_distribution_by_state.columns.str.lower()\n",
                "\n",
                "state_dist = pd.read_csv('../data/processed/v2_state_distribution.csv')\n",
                "states = state_dist['UF'].values\n",
                "state_weights = state_dist['Consumo'].values / state_dist['Consumo'].sum()\n"
            ]
            cell['source'] = new_source
            found = True
            print("Successfully found and updated the loading cell.")
            break

if not found:
    print("Could not find the target cell.")
else:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook saved successfully.")
