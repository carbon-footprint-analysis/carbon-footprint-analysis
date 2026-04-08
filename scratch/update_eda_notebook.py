import json
import os

notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\02_eda_analysis.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Define the source code for the cells we want to update
# Cell 3 (Loading data)
loading_source = [
    "import pandas as pd\n",
    "\n",
    "# 1. Definir o caminho para o dataset sintético gerado\n",
    "caminho_dados = '../data/processed/synthetic_energy_emissions_dataset.csv'\n",
    "\n",
    "# 2. Carregar o dataset usando o pandas\n",
    "# O dataset sintético possui um índice na primeira coluna que podemos ignorar\n",
    "df = pd.read_csv(caminho_dados).drop(columns=['Unnamed: 0'], errors='ignore')\n",
    "\n",
    "# 3. Inspeção Visual\n",
    "print(\"✅ Dataset carregado com sucesso!\")\n",
    "print(f\"O arquivo contém {df.shape[0]} linhas e {df.shape[1]} colunas.\\n\")\n",
    "\n",
    "print(\"--- Primeiras 5 linhas do Dataset ---\")\n",
    "display(df.head())\n",
    "\n",
    "print(\"\\n--- Resumo Técnico (Tipos de Dados e Nulos) ---\")\n",
    "df.info()\n",
    "\n",
    "print(\"\\n--- Estatísticas Descritivas Básicas ---\")\n",
    "display(df.describe())"
]

# Cell 4 (Conversion)
conversion_source = [
    "# 1. Converter a coluna de data para o formato correto de data\n",
    "df['data'] = pd.to_datetime(df['data'])\n",
    "\n",
    "# 2. Converter colunas numéricas\n",
    "cols_numericas = ['consumo_kwh', 'emissao_co2']\n",
    "\n",
    "for col in cols_numericas:\n",
    "    if df[col].dtype == 'object':\n",
    "        df[col] = df[col].astype(str).str.replace(',', '.')\n",
    "    df[col] = pd.to_numeric(df[col], errors='coerce')\n",
    "\n",
    "# 3. Verificar se a conversão deu certo\n",
    "print(\"✅ Conversão concluída!\")\n",
    "print(\"\\n--- Novos Tipos de Dados ---\")\n",
    "print(df.dtypes)\n",
    "\n",
    "print(\"\\n--- Estatísticas Atualizadas ---\")\n",
    "display(df.describe())"
]

# Cell 5 (EDA)
eda_source = [
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "\n",
    "# Silencia avisos genéricos\n",
    "warnings.filterwarnings('ignore', category=FutureWarning)\n",
    "\n",
    "# --- 1. PREPARAÇÃO DOS DADOS PARA O RELATÓRIO ---\n",
    "# Emissões por Setor\n",
    "setor_emissao = df.groupby('setor')['emissao_co2'].sum().sort_values(ascending=False).reset_index()\n",
    "\n",
    "# Emissões por Estado (Top 5 para o console)\n",
    "estado_emissao_full = df.groupby('estado')['emissao_co2'].sum().sort_values(ascending=False).reset_index()\n",
    "top_estados = estado_emissao_full.head(10)\n",
    "\n",
    "# Intensidade de Carbono\n",
    "resumo_fontes = df.groupby('fonte_energia')[['emissao_co2', 'consumo_kwh']].sum()\n",
    "intensidade = (resumo_fontes['emissao_co2'] / resumo_fontes['consumo_kwh']).sort_values(ascending=False)\n",
    "\n",
    "# --- 2. RELATÓRIO POR ESCRITO NO CONSOLE ---\n",
    "print(\"=\"*50)\n",
    "print(\"📊 RELATÓRIO EXECUTIVO DE EMISSÕES DE CO2\")\n",
    "print(\"=\"*50)\n",
    "\n",
    "print(\"\\n[1] EMISSÕES TOTAIS POR SETOR (kg CO2):\")\n",
    "for index, row in setor_emissao.iterrows():\n",
    "    print(f\" - {row['setor'].capitalize()}: {row['emissao_co2']:,.2f} kg\")\n",
    "\n",
    "print(\"\\n[2] TOP 5 ESTADOS COM MAIORES EMISSÕES:\")\n",
    "for index, row in estado_emissao_full.head(5).iterrows():\n",
    "    print(f\" - {row['estado']}: {row['emissao_co2']:,.2f} kg\")\n",
    "\n",
    "print(\"\\n[3] INTENSIDADE DE CARBONO POR FONTE (kg CO2/kWh):\")\n",
    "for fonte, valor in intensidade.items():\n",
    "    print(f\" - {fonte.capitalize()}: {valor:.4f} kg CO2/kWh\")\n",
    "\n",
    "print(\"\\n\" + \"=\"*50)\n",
    "\n",
    "# --- 3. PARTE VISUAL (GRÁFICOS) ---\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.figure(figsize=(15, 10))\n",
    "\n",
    "# Gráfico de Barras: Setor\n",
    "plt.subplot(2, 2, 1)\n",
    "sns.barplot(data=setor_emissao, x='setor', y='emissao_co2', hue='setor', palette='viridis', legend=False)\n",
    "plt.title('Total de Emissões por Setor (kg CO2)')\n",
    "plt.xticks(rotation=45)\n",
    "\n",
    "# Gráfico de Barras: Estado\n",
    "plt.subplot(2, 2, 2)\n",
    "sns.barplot(data=top_estados, x='estado', y='emissao_co2', hue='estado', palette='magma', legend=False)\n",
    "plt.title('Top 10 Estados com Maiores Emissões')\n",
    "\n",
    "# Boxplot: Fonte de Energia\n",
    "plt.subplot(2, 1, 2)\n",
    "sns.boxplot(data=df, x='fonte_energia', y='emissao_co2', hue='fonte_energia', palette='Set2', legend=False)\n",
    "plt.yscale('log')\n",
    "plt.title('Distribuição de Emissões por Fonte de Energia (Escala Log)')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Cell 6 (Classification)
classification_source = [
    "import numpy as np\n",
    "\n",
    "# 1. Criar a classificação baseada nos percentis das emissões\n",
    "# Vamos dividir em 3 grupos iguais (33% cada)\n",
    "limites = df['emissao_co2'].quantile([0.33, 0.66]).values\n",
    "\n",
    "def categorizar_impacto(valor):\n",
    "    if valor <= limites[0]:\n",
    "        return 'Baixo Impacto'\n",
    "    elif valor <= limites[1]:\n",
    "        return 'Médio Impacto'\n",
    "    else:\n",
    "        return 'Alto Impacto'\n",
    "\n",
    "# Aplicar a função\n",
    "df['impacto_ambiental'] = df['emissao_co2'].apply(categorizar_impacto)\n",
    "\n",
    "# 2. RELATÓRIO TEXTUAL DA NOVA COLUNA\n",
    "print(\"=\"*50)\n",
    "print(\"✅ NOVA VARIÁVEL: IMPACTO AMBIENTAL\")\n",
    "print(\"=\"*50)\n",
    "\n",
    "contagem = df['impacto_ambiental'].value_counts()\n",
    "porcentagem = df['impacto_ambiental'].value_counts(normalize=True) * 100\n",
    "\n",
    "for cat in ['Baixo Impacto', 'Médio Impacto', 'Alto Impacto']:\n",
    "    print(f\" - {cat}: {contagem[cat]} registros ({porcentagem[cat]:.1f}%)\")\n",
    "\n",
    "print(\"\\n\" + \"=\"*50)\n",
    "\n",
    "# 3. SALVAR O DATASET PROCESSADO\n",
    "caminho_processado = '../data/processed/dados_energia_limpos.csv'\n",
    "df.to_csv(caminho_processado, index=False)\n",
    "print(f\"💾 Arquivo salvo com sucesso em:\\n{caminho_processado}\")\n",
    "\n",
    "# 4. VISUALIZAÇÃO DA DISTRIBUIÇÃO\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.countplot(data=df, x='impacto_ambiental', order=['Baixo Impacto', 'Médio Impacto', 'Alto Impacto'],\n",
    "              hue='impacto_ambiental', palette='RdYlGn_r', legend=False)\n",
    "plt.title('Distribuição das Categorias de Impacto Ambiental')\n",
    "plt.ylabel('Quantidade de Registros')\n",
    "plt.show()"
]

# Cell 7 (Modeling)
modeling_source = [
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.tree import DecisionTreeClassifier, plot_tree\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "\n",
    "# 1. PREPARAÇÃO DOS DADOS\n",
    "# Vamos usar o consumo e o setor para prever o impacto ambiental\n",
    "# Precisamos transformar o texto (setor) em números para o modelo entender\n",
    "df_modelo = df.copy()\n",
    "df_modelo['setor_encoded'] = df_modelo['setor'].astype('category').cat.codes\n",
    "\n",
    "X = df_modelo[['consumo_kwh', 'setor_encoded']]\n",
    "y = df_modelo['impacto_ambiental']\n",
    "\n",
    "# Dividir em Treino (80%) e Teste (20%)\n",
    "X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "\n",
    "# 2. TREINAMENTO DO MODELO\n",
    "# Limitamos a profundidade (max_depth) para a árvore não ficar gigante e ser legível\n",
    "modelo = DecisionTreeClassifier(max_depth=3, random_state=42)\n",
    "modelo.fit(X_treino, y_treino)\n",
    "\n",
    "# 3. RELATÓRIO DE DESEMPENHO NO CONSOLE\n",
    "print(\"=\"*50)\n",
    "print(\"🤖 Relatório do Modelo Preditivo\")\n",
    "print(\"=\"*50)\n",
    "previsoes = modelo.predict(X_teste)\n",
    "print(classification_report(y_teste, previsoes))\n",
    "\n",
    "# 4. VISUALIZAÇÃO DA ÁRVORE (O \"MAPA\" DA DECISÃO)\n",
    "plt.figure(figsize=(20,10))\n",
    "plot_tree(modelo, feature_names=['Consumo (kWh)', 'Setor'],\n",
    "          class_names=modelo.classes_, filled=True, rounded=True, fontsize=12)\n",
    "plt.title(\"Árvore de Decisão: Classificação de Impacto Ambiental\")\n",
    "plt.show()"
]

# Update cells in the notebook
# The notebook structure:
# nb['cells'][0] -> Markdown header
# nb['cells'][1] -> Empty code cell
# nb['cells'][2] -> Folder creation (commented out)
# nb['cells'][3] -> Loading data (d8VSNeFBfNED)
# nb['cells'][4] -> Conversion (XE4wJuiOmpJR)
# nb['cells'][5] -> EDA (zfmggiwznWqU)
# nb['cells'][6] -> Classification (BfCJ5ikeo-dO)
# nb['cells'][7] -> Modeling (61KOqCL1qKGX)

cell_map = {
    'd8VSNeFBfNED': loading_source,
    'XE4wJuiOmpJR': conversion_source,
    'zfmggiwznWqU': eda_source,
    'BfCJ5ikeo-dO': classification_source,
    '61KOqCL1qKGX': modeling_source
}

for cell in nb['cells']:
    if cell.get('metadata', {}).get('id') in cell_map:
        cell['source'] = cell_map[cell['metadata']['id']]

# Remove redundant section starting from index 8 onwards (where Secton 2 starts)
# Section 2 starts with markdown id "w0r1obbk2Xhe"
redundant_index = -1
for i, cell in enumerate(nb['cells']):
    if cell.get('metadata', {}).get('id') == "w0r1obbk2Xhe":
        redundant_index = i
        break

if redundant_index != -1:
    nb['cells'] = nb['cells'][:redundant_index]

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully updated {notebook_path}")
