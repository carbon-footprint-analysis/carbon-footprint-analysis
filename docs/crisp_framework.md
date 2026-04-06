# CRISP-DM Framework: Projeto de Pegada de Carbono

Este documento mapeia o ciclo de vida do projeto seguindo a metodologia CRISP-DM, apontando para as implementações e resultados de cada etapa.

---

## 🟢 1. Business Understanding (Entendimento do Negócio) [CONCLUÍDO]

- **Problema**: Dificuldade em quantificar o impacto ambiental (CO₂) de atividades energéticas corporativas.
- **Objetivo**: Desenvolver um modelo para estimar emissões com base no consumo e contexto.
- **KPI**: Minimizar o erro de estimativa (MAE/RMSE).
- **Referência**: [README.md](../README.md)

---

## 🟢 2. Data Understanding (Entendimento dos Dados) [CONCLUÍDO]

- **Fonte**: Dataset sintético com 100.000 registros, baseado em parâmetros IPCC e EPE.
- **Análises**: EDA temporal, sazonalidade, correlações e qualidade dos dados.
- **Referência**: [02_eda_analysis.ipynb](../notebooks/02_eda_analysis.ipynb) | [Detalhes do EDA](./detalhes_implementacao_eda_preparacao.md)

---

## 🟢 3. Data Preparation (Preparação dos Dados) [CONCLUÍDO]

- **Processamento**: Limpeza de outliers (IQR) e criação de features temporais (mês/estação).
- **Pipeline**: Escalonamento numérico (`StandardScaler`) e codificação categórica (`OneHotEncoder`).
- **Referência**: [03_model_preparation.ipynb](../notebooks/03_model_preparation.ipynb)

---

## 🟢 4. Modeling (Modelagem) [CONCLUÍDO]

- **Algoritmos**: Comparação entre Regressão Linear (Baseline) e Random Forest Regressor.
- **Seleção**: O Random Forest foi selecionado por capturar melhor as relações não-lineares.
- **Referência**: [04_model_training.ipynb](../notebooks/04_model_training.ipynb) | [Relatório de Modelagem](./relatorio_final_modelagem.md)

---

## 🟢 5. Evaluation (Avaliação) [CONCLUÍDO]

- **Métricas**: R² de **0,9942** no conjunto de teste.
- **Robustez**: Stress Test com 5% de ruído demonstrou estabilidade (queda de apenas 0,37% no R²).
- **Referência**: Seção 4 e 5 do [Relatório de Modelagem](./relatorio_final_modelagem.md)

---

## 🟢 6. Deployment (Implantação) [CONCLUÍDO]

- **Persistência**: Modelo salvo em `models/carbon_footprint_rf_v1.joblib`.
- **Interfaces**:
    - **Visual**: [05_model_deployment.ipynb](../notebooks/05_model_deployment.ipynb)
    - **Técnica (CLI)**: [predict_co2.py](../scripts/predict_co2.py)
- **Documentação de Uso**: [Relatório de Implantação](./relatorio_implantacao_modelo.md)

---

## Conclusão Final
O projeto completou com sucesso todas as fases do ciclo CRISP-DM, entregando uma solução robusta, documentada e pronta para integração em sistemas de monitoramento ambiental (ESG).