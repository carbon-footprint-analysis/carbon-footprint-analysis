import json

with open('notebooks/03_model_preparation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Fix cell index 3: update data path and add mes/estacao derivation
new_source = (
    "# Carregar o dataset\n"
    "data_path = os.path.join('..', 'data', 'processed', 'synthetic_energy_emissions_dataset.csv')\n"
    "df = pd.read_csv(data_path)\n"
    "\n"
    "# Derivar colunas de mes e estacao a partir da coluna data\n"
    "df['data'] = pd.to_datetime(df['data'])\n"
    "df['mes'] = df['data'].dt.month\n"
    "\n"
    "def get_estacao(mes):\n"
    "    if mes in [12, 1, 2]: return 'verao'\n"
    "    elif mes in [3, 4, 5]: return 'outono'\n"
    "    elif mes in [6, 7, 8]: return 'inverno'\n"
    "    else: return 'primavera'\n"
    "\n"
    "df['estacao'] = df['mes'].apply(get_estacao)\n"
    "\n"
    "print(f'Formato do dataset: {df.shape}')\n"
    "df.head()\n"
)

nb['cells'][3]['source'] = new_source
nb['cells'][3]['outputs'] = []
nb['cells'][3]['execution_count'] = None

with open('notebooks/03_model_preparation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Notebook updated successfully.')
print('New cell 3 source:')
print(nb['cells'][3]['source'])
