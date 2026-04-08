"""
Fix 03_model_preparation.ipynb:
1. Replace local file path with GitHub raw URL
2. Fix column names from English stubs to Portuguese names used in the actual dataset
3. Derive mes/estacao from the 'data' column
"""
import json

nb_path = r'notebooks/03_model_preparation.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# --- Cell 3 (index 3): Data loading ---
new_loading_cell = [
    "# URL do dataset sintético no repositório GitHub\n",
    "DATASET_URL = (\n",
    "    'https://raw.githubusercontent.com/carbon-footprint-analysis/'\n",
    "    'carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv'\n",
    ")\n",
    "\n",
    "# Carregar o dataset\n",
    "df = pd.read_csv(DATASET_URL).drop(columns=['Unnamed: 0'], errors='ignore')\n",
    "\n",
    "# Derivar colunas de mês e estação a partir da coluna 'data'\n",
    "df['data'] = pd.to_datetime(df['data'])\n",
    "df['mes'] = df['data'].dt.month\n",
    "\n",
    "def get_estacao(mes):\n",
    "    if mes in [12, 1, 2]: return 'verao'\n",
    "    elif mes in [3, 4, 5]: return 'outono'\n",
    "    elif mes in [6, 7, 8]: return 'inverno'\n",
    "    else: return 'primavera'\n",
    "\n",
    "df['estacao'] = df['mes'].apply(get_estacao)\n",
    "\n",
    "print(f'[OK] Dataset carregado com sucesso!')\n",
    "print(f'   Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas')\n",
    "df.head()"
]

# --- Cell 5 (index 5): Feature selection ---
new_features_cell = [
    "# Variáveis alvo e atributos\n",
    "target = 'emissao_co2'\n",
    "features = ['consumo_kwh', 'setor', 'estado', 'fonte_energia', 'mes', 'estacao']\n",
    "\n",
    "X = df[features]\n",
    "y = df[target]\n",
    "\n",
    "print(f'Variável alvo: {target}')\n",
    "print(f'Atributos ({len(features)}): {features}')"
]

# --- Cell 9 (index 9): Pipeline numeric/categorical features ---
new_pipeline_cell = [
    "# Identificar colunas numéricas e categóricas\n",
    "numeric_features = ['consumo_kwh', 'mes']\n",
    "categorical_features = ['setor', 'estado', 'fonte_energia', 'estacao']\n",
    "\n",
    "# Definir transformadores\n",
    "numeric_transformer = Pipeline(steps=[\n",
    "    ('scaler', StandardScaler())\n",
    "])\n",
    "\n",
    "categorical_transformer = Pipeline(steps=[\n",
    "    ('onehot', OneHotEncoder(handle_unknown='ignore'))\n",
    "])\n",
    "\n",
    "# Combinar transformadores\n",
    "preprocessor = ColumnTransformer(\n",
    "    transformers=[\n",
    "        ('num', numeric_transformer, numeric_features),\n",
    "        ('cat', categorical_transformer, categorical_features)\n",
    "    ]\n",
    ")\n",
    "\n",
    "print('Pipeline de pré-processamento configurado.')"
]

# Map cell indices to their new sources
fixes = {
    3: new_loading_cell,
    5: new_features_cell,
    9: new_pipeline_cell,
}

for idx, new_source in fixes.items():
    nb['cells'][idx]['source'] = new_source
    nb['cells'][idx]['outputs'] = []
    nb['cells'][idx]['execution_count'] = None
    print(f'[OK] Cell {idx} updated.')

# Also remove 'import os' from imports cell since it's no longer needed
imports_cell = nb['cells'][1]
imports_cell['source'] = [
    line for line in imports_cell['source']
    if 'import os' not in line
]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('[OK] Notebook saved successfully.')
