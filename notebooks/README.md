# 🧪 Notebooks de Desenvolvimento (CRISP-DM)

Esta pasta contém o passo a passo técnico do projeto, organizado conforme as fases do **CRISP-DM**. Cada notebook representa uma etapa crucial na construção do modelo de estimativa de CO2.

## 📋 Lista de Notebooks

### 01. Geração e Configuração de Dados
- **Arquivo**: `01_build_dataset_generation_config.ipynb`
- **Fase**: Business & Data Understanding
- **Objetivo**: Definir as premissas estatísticas e os fatores de emissão (IPCC/EPE) para a criação do dataset sintético de 100k registros.

### 02. Análise Exploratória (EDA)
- **Arquivo**: `02_eda_analysis.ipynb`
- **Fase**: Data Understanding
- **Objetivo**: Identificar padrões de consumo, sazonalidade, outliers e correlações entre fontes de energia e emissões.

### 03. Preparação de Dados
- **Arquivo**: `03_model_preparation.ipynb`
- **Fase**: Data Preparation
- **Objetivo**: Construção de pipelines de pré-processamento (StandardScaler e OneHotEncoder) e engenharia de novas features (estação do ano).

### 04. Treinamento e Comparação de Modelos
- **Arquivo**: `04_model_training.ipynb`
- **Fase**: Modeling / Evaluation
- **Objetivo**: 
    - Comparação entre **Linear Regression**, **Random Forest** e **Gradient Boosting**.
    - Seleção automática do melhor modelo baseado em R².
    - Teste de Robustez (Stress Test).
    - Exportação do modelo campeão para `models/`.

### 05. Implantação e Predição
- **Arquivo**: `05_model_deployment.ipynb`
- **Fase**: Deployment
- **Objetivo**: Demonstração prática de uso do modelo treinado para novas interferências e integração com sistemas de terceiros.

---

## 🛠️ Como Utilizar
Para garantir a integridade dos resultados, recomenda-se a execução sequencial dos notebooks (01 a 05).

> [!TIP]
> O **Notebook 04** é o "cérebro" da modelagem. Nele você pode ajustar hiperparâmetros e visualizar a importância de cada variável nas emissões de CO2.