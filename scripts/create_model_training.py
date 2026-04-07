import nbformat as nbf
import os

# Path to the new notebook
notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\04_model_training.ipynb'

# Create a new notebook
nb = nbf.v4.new_notebook()

# Define cells
cells = [
    nbf.v4.new_markdown_cell("# 04 - Treinamento e Avaliação do Modelo\n\nNeste notebook, treinamos e comparamos diferentes modelos de regressão para estimar a pegada de carbono. Começamos com um baseline linear e progredimos para modelos de conjunto (*ensemble*) como Random Forest."),
    nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\nimport os\n\n# Semente aleatória para reprodutibilidade\nnp.random.seed(42)"),
    nbf.v4.new_markdown_cell("## 1. Carregamento e Preparação dos Dados\n\nCarregamos o dataset e preparamos as features temporais baseadas nos insights do EDA."),
    nbf.v4.new_code_cell("# Carregar o dataset\ndata_path = os.path.join('..', 'data', 'processed', 'synthetic_energy_emissions_dataset.csv')\ndf = pd.read_csv(data_path)\n\n# Engenharia de features temporal\ndf['date'] = pd.to_datetime(df['date'])\ndf['month'] = df['date'].dt.month\n\ndef get_season(month):\n    if month in [12, 1, 2]: return 'Verao'\n    if month in [3, 4, 5]: return 'Outono'\n    if month in [6, 7, 8]: return 'Inverno'\n    return 'Primavera'\n\ndf['season'] = df['month'].apply(get_season)\n\n# Seleção de atributos e target\ntarget = 'co2_emission'\n# Removemos o target e colunas não-preditivas (IDs e Datas brutas)\nX = df.drop(columns=[target, 'company_id', 'date'])\ny = df[target]\n\n# Divisão Treino/Teste\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\nprint(f\"Treino: {X_train.shape}, Teste: {X_test.shape}\")"),
    nbf.v4.new_markdown_cell("## 2. Pipeline de Pré-processamento\n\nDefinimos o processamento comum para todos os modelos."),
    nbf.v4.new_code_cell("# Definição das colunas\nnumeric_features = ['energy_kwh', 'month']\ncategorical_features = ['state', 'usage_type', 'energy_source', 'season']\n\n# Transformers\npreprocessor = ColumnTransformer(\n    transformers=[\n        ('num', StandardScaler(), numeric_features),\n        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)\n    ]\n)"),
    nbf.v4.new_markdown_cell("## 3. Modelo Baseline: Regressão Linear\n\nTreinamos o modelo simples para referência."),
    nbf.v4.new_code_cell("# Pipeline Linear\nmodel_lr = Pipeline(steps=[\n    ('preprocessor', preprocessor),\n    ('regressor', LinearRegression())\n])\n\nmodel_lr.fit(X_train, y_train)\ny_pred_lr = model_lr.predict(X_test)\n\nprint(f\"Regressão Linear - R²: {r2_score(y_test, y_pred_lr):.4f}\")"),
    nbf.v4.new_markdown_cell("## 4. Modelo Avançado: Random Forest\n\nTestamos um modelo de árvore de decisão para capturar relações não-lineares."),
    nbf.v4.new_code_cell("# Pipeline Random Forest\nmodel_rf = Pipeline(steps=[\n    ('preprocessor', preprocessor),\n    ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))\n])\n\nmodel_rf.fit(X_train, y_train)\ny_pred_rf = model_rf.predict(X_test)\n\nr2_original = r2_score(y_test, y_pred_rf)\nprint(f\"Random Forest - R²: {r2_original:.4f}\")"),
    nbf.v4.new_markdown_cell("## 5. Comparação de Performance\n\nAnálise visual das métricas."),
    nbf.v4.new_code_cell("def get_metrics(y_true, y_pred, name):\n    return {\n        'Model': name,\n        'R2': r2_score(y_true, y_pred),\n        'MAE': mean_absolute_error(y_true, y_pred),\n        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred))\n    }\n\nresults = pd.DataFrame([\n    get_metrics(y_test, y_pred_lr, 'Linear Regression'),\n    get_metrics(y_test, y_pred_rf, 'Random Forest')\n])\n\ndisplay(results)\n\n# Plot comparativo\nplt.figure(figsize=(10, 5))\nsns.barplot(data=results, x='Model', y='R2', palette='coolwarm')\nplt.title('Comparação de Performance (R²)')\nplt.ylim(0, 1)\nplt.show()"),
    nbf.v4.new_markdown_cell("## 6. Importância das Features (Random Forest)\n\nIdentificamos quais variáveis mais influenciam o cálculo de CO2."),
    nbf.v4.new_code_cell("# Extração dos nomes das colunas após OneHotEncoding\nohe_feature_names = model_rf.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)\nfeature_names = numeric_features + list(ohe_feature_names)\n\n# Importâncias\nimportances = model_rf.named_steps['regressor'].feature_importances_\nfeature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values('importance', ascending=False)\n\nplt.figure(figsize=(10, 8))\nsns.barplot(data=feature_importance_df.head(10), x='importance', y='feature', palette='magma')\nplt.title('Top 10 Variáveis mais Importantes (Random Forest)')\nplt.show()"),
    nbf.v4.new_markdown_cell("## 7. Teste de Robustez (Stress Test)\n\nSimulamos imprevistos do mundo real ao adicionar ruído de 5% aos dados de consumo energético."),
    nbf.v4.new_code_cell("# Simulação de ruído (5% de desvio padrão do consumo)\nX_test_noisy = X_test.copy()\n\n# Calcula a escala do ruído (5% do consumo medido)\nnoise_scale = X_test_noisy['energy_kwh'] * 0.05\nnoise = np.random.normal(0, 1, size=len(X_test_noisy)) * noise_scale\n\nX_test_noisy['energy_kwh'] += noise\n\n# Predições no conjunto ruidoso\ny_pred_noisy = model_rf.predict(X_test_noisy)\n\n# Métricas ruidosas\nr2_noisy = r2_score(y_test, y_pred_noisy)\nmae_noisy = mean_absolute_error(y_test, y_pred_noisy)\n\nprint(f\"--- Teste de Robustez (5% Ruído) ---\")\nprint(f\"R² Original (Sem Ruído): {r2_original:.4f}\")\nprint(f\"R² Ruidoso (Com 5% de Ruído): {r2_noisy:.4f}\")\nprint(f\"Queda Relativa no R²: {((r2_original - r2_noisy) / r2_original) * 100:.2f}%\")\nprint(f\"Novo MAE: {mae_noisy:.2f} kg CO2\")")
]

nb.cells = cells

# Save the notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook {notebook_path} updated with Stress Test.")
