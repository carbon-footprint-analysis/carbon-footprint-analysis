import json

nb_path = 'notebooks/03_model_preparation.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:100]
    print(f"  Cell {i} ({c['cell_type']}): {repr(src)}")

# Find the cell that has the wrong path
target_old = 'carbon_footprint_data.csv'
fixed = False
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    if target_old in src:
        print(f"\n[!] Found bad path in cell {i}. Fixing...")
        cell['source'] = (
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
        cell['outputs'] = []
        cell['execution_count'] = None
        fixed = True

if fixed:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("\n[OK] Notebook salvo com sucesso!")

    # Verify
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb2 = json.load(f)
    for i, c in enumerate(nb2['cells']):
        if 'data_path' in ''.join(c['source']):
            print(f"\n[Verificacao] Cell {i}:")
            print(''.join(c['source']))
else:
    print("\n[INFO] Nenhuma celula com o caminho antigo encontrada.")
    print("Caminho atual do dataset nas celulas:")
    for i, c in enumerate(nb['cells']):
        if 'data_path' in ''.join(c['source']):
            print(f"  Cell {i}: {''.join(c['source'])[:200]}")
