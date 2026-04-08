import json
import re

def enhance_config_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # 1. Update first markdown cell
    nb['cells'][0]['source'] = [
        "# 📊 Configuração da Geração de Dados Sintéticos\n",
        "\n",
        "Este notebook processa dados oficiais de energia provenientes de:\n",
        "\n",
        "- **EPE** (Empresa de Pesquisa Energética)\n",
        "- **ANEEL** (Agência Nacional de Energia Elétrica)\n",
        "\n",
        "O objetivo principal é gerar os arquivos de configuração probabilística utilizados pelo gerador de conjuntos de dados sintéticos.\n",
        "\n",
        "--- \n",
        "### 📤 Saídas Geradas:\n",
        "- `consumption_profiles.csv`\n",
        "- `energy_source_distribution.csv`\n",
        "- `company_size_distribution_by_usage.csv`\n",
        "- `usage_distribution_by_state.csv`\n",
        "- `seasonality_state_class_month.csv`"
    ]

    # 2. Iterate and translate comments/markdown
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if "Clona Projeto" in source:
                cell['source'] = ["### 🧬 Preparação do Ambiente\n", "Clonagem do repositório para facilitar o acesso aos dados."]
            elif "importa dados oficiais" in source:
                cell['source'] = ["### 📥 ETL: Consumo Industrial por Estado (EPE)\n", "Importação e limpeza dos dados de consumo industrial."]
            elif "Abertura do dados oficial" in source:
                cell['source'] = ["### 📥 ETL: Consumo Mensal por Categoria (EPE)\n", "Abertura dos dados oficiais de consumo mensal convertendo a escala de MW para kWh."]
        
        elif cell['cell_type'] == 'code':
            source_lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
            new_lines = []
            for line in source_lines:
                # Simple translations
                line = line.replace("# Mapping Portuguese categories to standardized English labels", "# Mapeamento de categorias para rótulos padronizados")
                line = line.replace("# Folder creation commented out", "# Criação de pastas comentada para preservar estrutura local")
                line = line.replace("# Define o nome da pasta principal", "# Nome do projeto")
                line = line.replace("# Define as subpastas", "# Subpastas do projeto")
                line = line.replace("# Create the directory", "# Cria o diretório")
                new_lines.append(line)
            cell['source'] = new_lines

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"✓ {nb_path} aprimorado.")

def enhance_eda_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Add Header and Table of Contents if missing
    if nb['cells'][0]['cell_type'] != 'markdown' or "Análise Exploratória" not in "".join(nb['cells'][0]['source']):
        header_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🔍 Análise Exploratória de Dados (EDA) e Modelagem\n",
                "\n",
                "Este notebook realiza a análise dos dados de consumo de energia e emissões de CO2, focando em:\n",
                "1. Limpeza e preparação dos dados.\n",
                "2. Visualização de tendências setoriais e regionais.\n",
                "3. Classificação de impacto ambiental.\n",
                "4. Treinamento de um modelo de Árvore de Decisão.\n",
                "\n",
                "---"
            ]
        }
        nb['cells'].insert(0, header_cell)

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if "EDA synthetic_energy_emissions_dataset.csv" in source:
                cell['source'] = ["## 🧪 Análise do Dataset Sintético Gerado\n", "Exploração dos dados gerados no passo anterior."]
            elif "Tipagem das colunas" in source:
                cell['source'] = ["### 📊 Definição de Tipos e Esquema\n", source]
            elif "ETL leve" in source:
                cell['source'] = ["## ⚙️ Processamento e Engenharia de Atributos (Feature Engineering)"]
            elif "add região" in source:
                cell['source'] = ["- Adição da coluna de **Região** baseada na UF."]
            elif "add mes" in source:
                cell['source'] = ["- Extração do **Mês**."]
            elif "add estação" in source:
                cell['source'] = ["- Mapeamento das **Estações do Ano**."]
            elif "Distribuições" in source:
                cell['source'] = ["### 📈 Distribuições Estatísticas"]
            elif "tipo de uso" in source:
                cell['source'] = ["#### Proporção por Tipo de Uso"]
            elif "fonte energia" in source:
                cell['source'] = ["#### Proporção por Fonte de Energia"]
        
        elif cell['cell_type'] == 'code':
            source_lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
            new_lines = []
            for line in source_lines:
                # Code translation in comments and plot labels
                line = line.replace("'Total de Emissões por Setor (kg CO2)'", "'Total de Emissões por Setor (kg CO2)'") # already ok
                line = line.replace("'Top 10 Estados com Maiores Emissões'", "'Top 10 Estados com Maiores Emissões'") # already ok
                line = line.replace("'Distribuição de Emissões por Fonte de Energia (Escala Log)'", "'Distribuição de Emissões por Fonte de Energia (Escala Log)'") # already ok
                line = line.replace('"Distribuiçao tipo de uso"', '"Distribuição por Tipo de Uso"')
                line = line.replace('"Proporção das Fontes de Energia"', '"Proporção por Fonte de Energia"')
                line = line.replace('"Fonte de energia"', '"Fonte de Energia"')
                line = line.replace('"Distribuição do consumo de energia por setor (escala log)"', '"Distribuição do Consumo de Energia por Setor (Escala Log)"')
                line = line.replace('"Setor"', '"Setor"')
                line = line.replace('"Energia (kWh)"', '"Energia (kWh)"')
                
                # Model related
                line = line.replace('"🤖 RELATÓRIO DO MODELO PREDITIVO"', '"🤖 Relatório do Modelo Preditivo"')
                line = line.replace('"Árvore de Decisão: Como o modelo classifica o Impacto Ambiental"', '"Árvore de Decisão: Classificação de Impacto Ambiental"')
                
                new_lines.append(line)
            cell['source'] = new_lines

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"✓ {nb_path} aprimorado.")

# Execute
enhance_config_notebook('notebooks/01_build_dataset_generation_config.ipynb')
enhance_eda_notebook('notebooks/02_eda_analysis.ipynb')
