# 🌿 Carbon Footprint Analysis — Estimativa de Emissões de CO₂

![Status: Concluído](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen)
![Methodology: CRISP-DM](https://img.shields.io/badge/Methodology-CRISP--DM-blue)
![Tech: Python & Scikit-Learn](https://img.shields.io/badge/Tech-Python%20%26%20Scikit--Learn-orange)
![Dashboard: Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Explainability: SHAP](https://img.shields.io/badge/Explainability-SHAP-purple)

---

## 📌 Visão Geral

O **Carbon Footprint Analysis** é um projeto de Ciência de Dados que estima emissões de CO₂ associadas ao consumo energético de empresas brasileiras. O objetivo é transformar dados simples de consumo em estimativas claras e interpretáveis de pegada de carbono, apoiando decisões de sustentabilidade e relatórios ESG.

O projeto seguiu rigorosamente a metodologia **CRISP-DM** em 6 fases, desde a construção do dataset até a entrega de um dashboard interativo com explicabilidade de modelo.

### 🏆 Principais Resultados

| Métrica | Valor |
|---|---|
| Melhor modelo | Random Forest Regressor |
| R² no conjunto de teste | **0.9948** |
| MAE (com 5% de ruído) | 233 kg CO₂ |
| Queda de R² no stress test | < 0.35% |
| Tamanho do dataset | 100.000 registros sintéticos |
| Features utilizadas | 6 (consumo, fonte, estado, setor, mês, estação) |

---

## 🏗️ Ciclo de Desenvolvimento (CRISP-DM)

### 1. Business Understanding
Empresas e organizações precisam quantificar e monitorar emissões de carbono para:
- Cumprir metas ESG e reportar pelo **Protocolo GHG (Escopos 1, 2 e 3)**
- Apoiar decisões de transição energética (ex: trocar fonte térmica por hidrelétrica)
- Atender a crescentes exigências regulatórias e de investidores

### 2. Data Understanding — `01_build_dataset_generation_config.ipynb`
O dataset foi construído de forma sintética, mas **calibrado com dados reais** de duas fontes oficiais:
- **EPE** (Empresa de Pesquisa Energética): perfis de consumo industrial por estado
- **ANEEL** (Agência Nacional de Energia Elétrica): distribuição de fontes energéticas

Os fatores de emissão por fonte foram extraídos da literatura técnica:

| Fonte | Fator de Emissão (kg CO₂/kWh) |
|---|---|
| Hidrelétrica | 0.004 |
| Eólica | 0.011 |
| Nuclear | 0.012 |
| Solar | 0.045 |
| Térmica | 0.820 |

### 3. Data Understanding (EDA) — `02_eda_analysis.ipynb`
- Análise exploratória completa: distribuições, correlações e detecção de outliers
- Análise de sazonalidade por estação do ano
- Comparação de emissões por setor, estado e fonte de energia
- Criação da variável `impacto_ambiental` por percentis para classificação de risco
- Treinamento de uma Árvore de Decisão classificadora como análise exploratória, revelando que `consumo_kwh` e `fonte_energia` são os principais separadores de impacto — motivando diretamente a escolha do modelo de regressão final

### 4. Data Preparation — `03_model_preparation.ipynb`
Pipeline de pré-processamento com `sklearn.Pipeline`:
- **Variáveis numéricas** (`consumo_kwh`, `mes`): normalização com `StandardScaler`
- **Variáveis categóricas** (`estado`, `setor`, `fonte_energia`, `season`): codificação com `OneHotEncoder(handle_unknown='ignore')`
- Divisão 80/20 (treino/teste) com `random_state=42` para reprodutibilidade

### 5. Modeling — `04_model_training.ipynb`
Três modelos foram treinados e comparados:

| Modelo | R² | MAE |
|---|---|---|
| Regressão Linear | ~0.85 | alto |
| **Random Forest** | **0.9948** | **~220 kg** |
| Gradient Boosting | ~0.99 | similar |

O **Random Forest** foi selecionado como modelo campeão por seu equilíbrio entre performance, velocidade de inferência e interpretabilidade via feature importances. O modelo completo (pré-processador + regressor) foi exportado como um único `Pipeline` do scikit-learn.

**Top features por importância:**
1. `consumo_kwh` — 75.8%
2. `fonte_energia_térmica` — 24.0%
3. `fonte_energia_solar` — 0.07%
4. `mes` — 0.04%

### 6. Evaluation — `04_model_training.ipynb`
- Métricas avaliadas: R², MAE, RMSE
- **Stress Test**: adição de 5% de ruído gaussiano no consumo manteve R² > 0.99 — modelo é robusto a erros de medição
- **SHAP** (`06_shap_explainability.ipynb`): análise de explicabilidade com `TreeExplainer`, confirmando que a `fonte_energia_térmica` é o principal driver qualitativo de emissão

### 7. Deployment — `05_model_deployment.ipynb` + `app.py`
- Função `estimate_co2()` para predição pontual
- Comparação entre todas as fontes elétricas e combustíveis líquidos (`wrapper.py`)
- **Dashboard Streamlit** com 5 abas interativas

---

## 📊 Dashboard Interativo (`app.py`)

Execute com:
```bash
streamlit run app.py
```

| Aba | Funcionalidade |
|---|---|
| 📊 Visão Geral | KPIs, ranking de fontes, variação mensal, comparação vs hidrelétrica |
| ⚖️ Simulador de Cenários | Comparação lado a lado de dois perfis com radar chart |
| 🎯 Meta de Redução | Busca das combinações fonte × mês que atingem uma meta de % de redução + heatmap |
| 📂 Análise em Lote | Upload de CSV com múltiplos registros, relatório agregado e download dos resultados |
| 🔍 Explicabilidade (SHAP) | Waterfall plot + tabela de contribuições por variável para qualquer predição |

---

## 🗂️ Dicionário de Variáveis

| Variável | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `id_empresa` | string | Identificador único da empresa | `C907106` |
| `data` | date | Data do registro | `2025-01-09` |
| `estado` | categórica | Unidade federativa brasileira (27 UFs) | `SP` |
| `setor` | categórica | Setor de atividade da empresa | `industrial` |
| `porte` | categórica | Porte da empresa | `large`, `small`, `medium` |
| `tipo_combustivel` | categórica | Tipo de combustível utilizado | `electric` |
| `consumo_kwh` | numérica | Consumo energético do período (kWh) | `38495.24` |
| `fonte_energia` | categórica | Fonte geradora da energia | `eólica`, `térmica`, `hidrelétrica`, `solar`, `nuclear` |
| `emissao_co2` | numérica | **Variável alvo** — emissão estimada de CO₂ (kg) | `408.59` |
| `mes` | numérica | Mês do registro (1–12), derivado de `data` | `1` |
| `season` | categórica | Estação do ano (Brasil), derivada de `mes` | `Verao`, `Outono`, `Inverno`, `Primavera` |

**Setores disponíveis:** `industrial`, `comercial`, `residencial`, `rural`, `outros`  
**Fontes de energia disponíveis:** `hidrelétrica`, `eólica`, `solar`, `nuclear`, `térmica`

---

## 📂 Estrutura do Repositório

```
carbon-footprint-analysis/
│
├── data/
│   ├── raw/                          # Dados oficiais EPE e ANEEL
│   └── processed/
│       ├── synthetic_energy_emissions_dataset.csv
│       └── v2_energy_source_emission_factors.csv
│
├── models/
│   └── best_carbon_footprint_model.joblib   # Pipeline treinado (pré-proc + RF)
│
├── notebooks/
│   ├── 01_build_dataset_generation_config.ipynb  # Geração do dataset sintético
│   ├── 02_eda_analysis.ipynb                     # Análise exploratória
│   ├── 03_model_preparation.ipynb               # Pré-processamento e pipeline
│   ├── 04_model_training.ipynb                  # Treinamento e avaliação
│   ├── 05_model_deployment.ipynb                # Predição e exemplos de uso
│   └── 06_shap_explainability.ipynb             # Explicabilidade com SHAP
│
├── app.py          # Dashboard Streamlit (5 abas)
├── wrapper.py      # Funções de predição e comparação entre fontes
└── README.md
```

---

## 🚀 Como Executar

### Requisitos
```bash
pip install pandas numpy scikit-learn joblib streamlit plotly matplotlib shap
```

### Ordem de execução dos notebooks
```
01 → 02 → 03 → 04 → 05 → 06
```
> O notebook 04 gera o arquivo `best_carbon_footprint_model.joblib` necessário para os notebooks 05, 06 e para o `app.py`.

### Dashboard
```bash
streamlit run app.py
```

### Predição via Python
```python
from wrapper import compare_energy_sources

resultado = compare_energy_sources(
    energy_kwh=5000,
    month=6,
    state="SP",
    usage_type="industrial",
    season="Inverno"
)
print(resultado)
```

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Bibliotecas |
|---|---|
| Linguagem | Python 3.13 |
| Análise de dados | Pandas, NumPy |
| Machine Learning | Scikit-Learn 1.8 |
| Explicabilidade | SHAP |
| Visualização | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Persistência | Joblib |

---

## 🔭 Extensibilidade

O modelo foi desenhado para ser facilmente expandido:

- **Mobilidade corporativa**: adicionar `modal_transporte` (carro, ônibus, avião) com seus respectivos fatores de emissão por km
- **Escopo 3 do GHG Protocol**: incorporar emissões de cadeia de fornecimento via variáveis de logística
- **Série temporal**: com dados históricos reais, evoluir para modelos de forecasting de emissões

---

*Desenvolvido seguindo a metodologia CRISP-DM durante ciclo de aceleração em Ciência de Dados.*
