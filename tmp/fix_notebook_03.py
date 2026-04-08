import json

nb_path = r'notebooks/03_model_preparation.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Clear all outputs and execution counts
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

# Fix each code cell by source content
for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])

    # Cell: feature selection (uses English col names - fix to Portuguese)
    if 'co2_emission' in src or 'energy_kwh' in src:
        cell['source'] = [
            '# Variaveis alvo e atributos\n',
            'target = \'emissao_co2\'\n',
            'features = [\'consumo_kwh\', \'setor\', \'estado\', \'fonte_energia\', \'mes\', \'estacao\']\n',
            '\n',
            'X = df[features]\n',
            'y = df[target]\n',
            '\n',
            'print(f"Variavel alvo: {target}")\n',
            'print(f"Atributos ({len(features)}): {features}")\n',
        ]

    # Cell: numeric/categorical features (English names)
    if 'energy_kwh' in src and 'numeric_features' in src:
        cell['source'] = [
            '# Identificar colunas numericas e categoricas\n',
            'numeric_features = [\'consumo_kwh\', \'mes\']\n',
            'categorical_features = [\'setor\', \'estado\', \'fonte_energia\', \'estacao\']\n',
            '\n',
            '# Definir transformadores\n',
            'numeric_transformer = Pipeline(steps=[\n',
            '    (\'scaler\', StandardScaler())\n',
            '])\n',
            '\n',
            'categorical_transformer = Pipeline(steps=[\n',
            '    (\'onehot\', OneHotEncoder(handle_unknown=\'ignore\'))\n',
            '])\n',
            '\n',
            '# Combinar transformadores\n',
            'preprocessor = ColumnTransformer(\n',
            '    transformers=[\n',
            '        (\'num\', numeric_transformer, numeric_features),\n',
            '        (\'cat\', categorical_transformer, categorical_features)\n',
            '    ]\n',
            ')\n',
            '\n',
            'print(\'[OK] Pipeline de pre-processamento configurado.\')\n',
        ]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done! All cells fixed and outputs cleared.')
print('Please CLOSE and REOPEN the notebook in Jupyter, then Run All Cells.')
