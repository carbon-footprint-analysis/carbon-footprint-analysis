import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}

def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }

cells = [
    # --- 0: Título ---
    md(
        "# 🔍 Análise Exploratória de Dados (EDA) e Modelagem\n\n"
        "Este notebook realiza a análise dos dados de consumo de energia e emissões de CO2, focando em:\n"
        "1. Carregamento e inspeção do dataset sintético.\n"
        "2. Limpeza e preparação dos dados.\n"
        "3. Visualização de tendências setoriais e regionais.\n"
        "4. Classificação de impacto ambiental.\n"
        "5. Treinamento de um modelo de Árvore de Decisão.\n\n"
        "---"
    ),

    # --- 1: Imports ---
    md("## 1. Importação de Bibliotecas"),
    code(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import warnings\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.tree import DecisionTreeClassifier, plot_tree\n"
        "from sklearn.metrics import classification_report\n\n"
        "warnings.filterwarnings('ignore')\n"
        "sns.set_theme(style='whitegrid')\n"
        "print('✅ Bibliotecas importadas com sucesso!')"
    ),

    # --- 2: Carregamento ---
    md("## 2. Carregamento do Dataset\n\nOs dados são carregados diretamente do repositório GitHub do projeto."),
    code(
        "# URL do dataset sintético no repositório GitHub\n"
        "DATASET_URL = (\n"
        "    'https://raw.githubusercontent.com/carbon-footprint-analysis/'\n"
        "    'carbon-footprint-analysis/main/data/processed/synthetic_energy_emissions_dataset.csv'\n"
        ")\n\n"
        "# Carregar com pd.read_csv — o dataset é um arquivo CSV\n"
        "df = pd.read_csv(DATASET_URL).drop(columns=['Unnamed: 0'], errors='ignore')\n\n"
        "print(f'✅ Dataset carregado com sucesso!')\n"
        "print(f'   Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas\\n')\n"
        "display(df.head())"
    ),

    # --- 3: Inspeção ---
    md("## 3. Inspeção e Limpeza dos Dados"),
    code(
        "# Tipos de dados e valores nulos\n"
        "print('--- Informações Gerais ---')\n"
        "df.info()\n\n"
        "print('\\n--- Estatísticas Descritivas ---')\n"
        "display(df.describe())\n\n"
        "print('\\n--- Valores Nulos por Coluna ---')\n"
        "print(df.isnull().sum())"
    ),

    # --- 4: Limpeza ---
    md("### 3.1 Conversão de Tipos"),
    code(
        "# Converter coluna de data\n"
        "df['data'] = pd.to_datetime(df['data'])\n\n"
        "# Garantir que colunas numéricas estejam no tipo correto\n"
        "for col in ['consumo_kwh', 'emissao_co2']:\n"
        "    if df[col].dtype == object:\n"
        "        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)\n"
        "    df[col] = pd.to_numeric(df[col], errors='coerce')\n\n"
        "print('✅ Conversão de tipos concluída!')\n"
        "print(df.dtypes)"
    ),

    # --- 5: EDA ---
    md("## 4. Análise Exploratória — Relatório Executivo"),
    code(
        "# Agregações\n"
        "setor_emissao   = df.groupby('setor')['emissao_co2'].sum().sort_values(ascending=False).reset_index()\n"
        "top_estados     = df.groupby('estado')['emissao_co2'].sum().sort_values(ascending=False).head(10).reset_index()\n"
        "resumo_fontes   = df.groupby('fonte_energia')[['emissao_co2', 'consumo_kwh']].sum()\n"
        "intensidade     = (resumo_fontes['emissao_co2'] / resumo_fontes['consumo_kwh']).sort_values(ascending=False)\n\n"
        "# Relatório no console\n"
        "print('=' * 50)\n"
        "print('📊 RELATÓRIO EXECUTIVO DE EMISSÕES DE CO2')\n"
        "print('=' * 50)\n\n"
        "print('\\n[1] EMISSÕES TOTAIS POR SETOR (kg CO2):')\n"
        "for _, row in setor_emissao.iterrows():\n"
        "    print(f\"  - {row['setor'].capitalize()}: {row['emissao_co2']:,.2f} kg\")\n\n"
        "print('\\n[2] TOP 5 ESTADOS COM MAIORES EMISSÕES:')\n"
        "for _, row in top_estados.head(5).iterrows():\n"
        "    print(f\"  - {row['estado']}: {row['emissao_co2']:,.2f} kg\")\n\n"
        "print('\\n[3] INTENSIDADE DE CARBONO POR FONTE (kg CO2/kWh):')\n"
        "for fonte, valor in intensidade.items():\n"
        "    print(f\"  - {fonte.capitalize()}: {valor:.4f} kg CO2/kWh\")\n"
        "print('=' * 50)"
    ),

    # --- 6: Visualizações ---
    md("### 4.1 Visualizações Gráficas"),
    code(
        "fig, axes = plt.subplots(2, 2, figsize=(16, 11))\n"
        "fig.suptitle('Análise de Emissões de CO2 — Visão Geral', fontsize=15, fontweight='bold')\n\n"
        "# Gráfico 1: Emissões por setor\n"
        "sns.barplot(ax=axes[0, 0], data=setor_emissao, x='setor', y='emissao_co2',\n"
        "            hue='setor', palette='viridis', legend=False)\n"
        "axes[0, 0].set_title('Emissões Totais por Setor (kg CO2)')\n"
        "axes[0, 0].set_xlabel('Setor')\n"
        "axes[0, 0].set_ylabel('Emissão Total (kg CO2)')\n"
        "axes[0, 0].tick_params(axis='x', rotation=45)\n\n"
        "# Gráfico 2: Top 10 estados\n"
        "sns.barplot(ax=axes[0, 1], data=top_estados, x='estado', y='emissao_co2',\n"
        "            hue='estado', palette='magma', legend=False)\n"
        "axes[0, 1].set_title('Top 10 Estados — Maiores Emissões')\n"
        "axes[0, 1].set_xlabel('Estado')\n"
        "axes[0, 1].set_ylabel('Emissão Total (kg CO2)')\n"
        "axes[0, 1].tick_params(axis='x', rotation=45)\n\n"
        "# Gráfico 3: Intensidade de carbono por fonte\n"
        "sns.barplot(ax=axes[1, 0], x=intensidade.index, y=intensidade.values,\n"
        "            palette='coolwarm', legend=False)\n"
        "axes[1, 0].set_title('Intensidade de Carbono por Fonte (kg CO2/kWh)')\n"
        "axes[1, 0].set_xlabel('Fonte de Energia')\n"
        "axes[1, 0].set_ylabel('kg CO2 / kWh')\n"
        "axes[1, 0].tick_params(axis='x', rotation=45)\n\n"
        "# Gráfico 4: Boxplot distribuição de emissões por fonte\n"
        "sns.boxplot(ax=axes[1, 1], data=df, x='fonte_energia', y='emissao_co2',\n"
        "            hue='fonte_energia', palette='Set2', legend=False)\n"
        "axes[1, 1].set_yscale('log')\n"
        "axes[1, 1].set_title('Distribuição de Emissões por Fonte (Escala Log)')\n"
        "axes[1, 1].set_xlabel('Fonte de Energia')\n"
        "axes[1, 1].set_ylabel('Emissão (kg CO2) — escala log')\n"
        "axes[1, 1].tick_params(axis='x', rotation=45)\n\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),

    # --- 7: Classificação ---
    md("## 5. Classificação de Impacto Ambiental\n\nCriamos uma nova coluna categórica com base nos percentis 33% e 66% das emissões."),
    code(
        "limites = df['emissao_co2'].quantile([0.33, 0.66]).values\n\n"
        "def categorizar_impacto(valor):\n"
        "    if valor <= limites[0]:\n"
        "        return 'Baixo Impacto'\n"
        "    elif valor <= limites[1]:\n"
        "        return 'Médio Impacto'\n"
        "    return 'Alto Impacto'\n\n"
        "df['impacto_ambiental'] = df['emissao_co2'].apply(categorizar_impacto)\n\n"
        "print('=' * 50)\n"
        "print('✅ NOVA VARIÁVEL: IMPACTO AMBIENTAL')\n"
        "print('=' * 50)\n"
        "contagem   = df['impacto_ambiental'].value_counts()\n"
        "porcentagem = df['impacto_ambiental'].value_counts(normalize=True) * 100\n"
        "for cat in ['Baixo Impacto', 'Médio Impacto', 'Alto Impacto']:\n"
        "    print(f\"  - {cat}: {contagem[cat]} registros ({porcentagem[cat]:.1f}%)\")\n\n"
        "# Visualização\n"
        "plt.figure(figsize=(8, 5))\n"
        "sns.countplot(data=df, x='impacto_ambiental',\n"
        "              order=['Baixo Impacto', 'Médio Impacto', 'Alto Impacto'],\n"
        "              hue='impacto_ambiental', palette='RdYlGn_r', legend=False)\n"
        "plt.title('Distribuição das Categorias de Impacto Ambiental')\n"
        "plt.xlabel('Categoria')\n"
        "plt.ylabel('Quantidade de Registros')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),

    # --- 8: Salvar processado ---
    md("### 5.1 Salvar Dataset Processado"),
    code(
        "import os\n\n"
        "caminho_processado = '../data/processed/dados_energia_limpos.csv'\n"
        "os.makedirs(os.path.dirname(caminho_processado), exist_ok=True)\n"
        "df.to_csv(caminho_processado, index=False)\n"
        "print(f'💾 Dataset processado salvo em: {caminho_processado}')\n"
        "print(f'   Dimensões finais: {df.shape[0]} linhas × {df.shape[1]} colunas')"
    ),

    # --- 9: Modelo ---
    md(
        "## 6. Modelagem — Árvore de Decisão\n\n"
        "Treinamos um modelo de classificação para prever o impacto ambiental "
        "com base no consumo (kWh) e no setor da empresa."
    ),
    code(
        "# Codificar variável categórica 'setor'\n"
        "df_modelo = df.copy()\n"
        "df_modelo['setor_encoded'] = df_modelo['setor'].astype('category').cat.codes\n\n"
        "X = df_modelo[['consumo_kwh', 'setor_encoded']]\n"
        "y = df_modelo['impacto_ambiental']\n\n"
        "# Divisão treino/teste\n"
        "X_treino, X_teste, y_treino, y_teste = train_test_split(\n"
        "    X, y, test_size=0.2, random_state=42\n"
        ")\n\n"
        "# Treinar o modelo\n"
        "modelo = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
        "modelo.fit(X_treino, y_treino)\n\n"
        "# Relatório de desempenho\n"
        "previsoes = modelo.predict(X_teste)\n"
        "print('=' * 50)\n"
        "print('🤖 RELATÓRIO DO MODELO PREDITIVO')\n"
        "print('=' * 50)\n"
        "print(classification_report(y_teste, previsoes))"
    ),

    # --- 10: Árvore visual ---
    md("### 6.1 Visualização da Árvore de Decisão"),
    code(
        "plt.figure(figsize=(22, 10))\n"
        "plot_tree(\n"
        "    modelo,\n"
        "    feature_names=['Consumo (kWh)', 'Setor (encoded)'],\n"
        "    class_names=modelo.classes_,\n"
        "    filled=True,\n"
        "    rounded=True,\n"
        "    fontsize=11\n"
        ")\n"
        "plt.title('Árvore de Decisão — Classificação de Impacto Ambiental', fontsize=14, fontweight='bold')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ),

    # --- 11: Conclusão ---
    md(
        "## 7. Conclusão\n\n"
        "Este notebook realizou com sucesso:\n"
        "- ✅ Carregamento e limpeza do dataset sintético de emissões.\n"
        "- ✅ Análise exploratória com relatório executivo e gráficos.\n"
        "- ✅ Criação da variável `impacto_ambiental` por percentis.\n"
        "- ✅ Treinamento e avaliação de um classificador de Árvore de Decisão.\n\n"
        "---\n"
        "_Próximo passo: `03_model_preparation.ipynb` — Pré-processamento avançado para ML._"
    ),
]

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.13.0"
        }
    },
    "cells": cells
}

with open('notebooks/02_eda_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print('✅ Notebook reescrito com sucesso em notebooks/02_eda_analysis.ipynb')
