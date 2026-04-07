# 🌿 Carbon Footprint Analysis: Estimativa de Emissões CO2

![Status: Concluído](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)
![Methodology: CRISP-DM](https://img.shields.io/badge/Methodology-CRISP--DM-blue)
![Tech: Python & SKLearn](https://img.shields.io/badge/Tech-Python%20%26%20SKLearn-orange)

## 📊 Visão Geral do Projeto

Este projeto utiliza Ciência de Dados e Machine Learning para quantificar o impacto ambiental (pegada de carbono) de atividades energéticas. Através de um dataset sintético baseado em parâmetros reais (IPCC, EPE), desenvolvemos um modelo capaz de estimar emissões de CO2 com extrema precisão, auxiliando na tomada de decisão para estratégias de sustentabilidade (ESG).

### 🏆 Resultados Principais
- **Performance do Modelo**: R² de **0,9948** (Gradient Boosting Regressor / Random Forest).
- **Competição de Modelos**: O pipeline agora compara Linear Regression, Random Forest e Gradient Boosting, selecionando automaticamente o melhor.
- **Robustez**: Stress Test com 5% de ruído manteve o R² acima de **0.99** no modelo campeão.
- **Insights**: Identificação do Consumo (kWh) e Fonte de Energia como os principais drivers de emissão.

---

## 🏗️ Ciclo de Desenvolvimento (CRISP-DM)

O projeto seguiu rigorosamente as 6 fases da metodologia CRISP-DM:

1.  **[Business Understanding](./docs/crisp_framework.md#1-business-understanding)**: Definição de objetivos e KPIs de sustentabilidade.
2.  **[Data Understanding](./notebooks/02_eda_analysis.ipynb)**: EDA profunda, análise de sazonalidade e detecção de outliers.
3.  **[Data Preparation](./notebooks/03_model_preparation.ipynb)**: Pipelines de Normalização e One-Hot Encoding.
4.  **[Modeling](./notebooks/04_model_training.ipynb)**: Comparação entre modelos lineares e de ensemble (**Random Forest** e **Gradient Boosting**).
5.  **[Evaluation](./docs/relatorio_final_modelagem.md)**: Validação métrica, análise de importância de atributos e testes de estresse.
6.  **[Deployment](./notebooks/05_model_deployment.ipynb)**: Exportação do melhor modelo para `best_carbon_footprint_model.joblib` e interface CLI.

---

## 🚀 Como Executar o Projeto

### 1. Requisitos
Certifique-se de ter o Python instalado e instale as dependências:
```bash
pip install -r requirements.txt
```

### 2. Calculadora de CO2 (CLI)
Você pode realizar predições rápidas diretamente pelo terminal:
```bash
python scripts/predict_co2.py --kwh 1500 --state SP --type industrial --source thermal --month 3
```

---

## 📂 Estrutura do Repositório
- `data/` → Conjuntos de dados brutos e processados.
- `docs/` → Relatórios detalhados de cada fase do projeto.
- `models/` → O **melhor modelo** treinado salvo como `best_carbon_footprint_model.joblib`.
- `notebooks/` → O passo a passo técnico do desenvolvimento (Fases 1-6).
- `scripts/` → Utilitários de treinamento, stress test e ferramentas de predição.

---

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.x
- **Análise**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn
- **Persistência**: Joblib

---

## 🚚 Extensibilidade: Frotas e Mobilidade

Embora o foco inicial deste MVP seja o consumo energético, o modelo foi desenhado para ser facilmente estendido para o setor de **Mobilidade Corporativa**:

- **Veículos Elétricos (EVs)**: O modelo atual já suporta a estimativa de EVs ao inserir o consumo médio em kWh da frota e a fonte de energia da rede de recarga.
- **Veículos a Combustão**: Pode ser adaptado convertendo o consumo de combustível (litros) para seu equivalente em kWh ou adicionando a feature `fuel_type` ao pipeline de treinamento.
- **Logística ESG**: Ideal para empresas que buscam relatórios de escopo 2 e 3 do Protocolo GHG.

---

**Contato**: Desenvolvido durante o ciclo de aceleração em Ciência de Dados.
