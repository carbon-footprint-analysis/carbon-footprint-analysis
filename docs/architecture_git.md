# 🏗️ Arquitetura do Projeto — CarbonFootprint

---

## 📦 Visão Geral

Estrutura organizada seguindo princípios de **engenharia de dados e MLOps**, separando claramente:

- dados  
- pipeline analítico  
- modelos  
- API  
- interface  
- documentação  

---

## 📁 Estrutura do Repositório

CarbonFootprint/
│
├── .gitattributes              # Configurações de atributos do Git
├── .gitignore                  # Arquivos ignorados no versionamento
│
├── app.py                      # API principal (FastAPI) para inferência e cálculo de CO₂
├── app.py_v2                   # Versão alternativa/teste da API
├── wrapper.py                  # Wrapper auxiliar (integração scripts/notebooks)
│
├── Dockerfile                  # Containerização da aplicação
├── requirements.txt            # Dependências do projeto
├── LICENSE                     # Licença do projeto
│
├── README.md                   # Documentação principal (visão geral do projeto)
│
├── pegada_1.png                # Imagem explicativa (pegada de carbono)
├── pegada_shap.png             # Visualização SHAP
├── pegada_transporte.png       # Visualização temática
│
├── shap_tab_snippet.py         # Script auxiliar para visualização SHAP
├── tmp_cells.txt               # Dump temporário de células de notebook
│
├── data/                       # Camada de dados (raw → external → processed)
│   ├── raw/                    # Dados brutos (fontes reais)
│   ├── external/               # Configurações do gerador sintético (núcleo)
│   ├── processed/              # Dados tratados e dataset final
│   └── (pipeline de dados)
│       raw → external → geração → processed
│
├── docs/                       # Documentação técnica
│   └── reports/                # Relatórios e outputs
│
├── frontend/                   # Interface web (consome API)
├── models/                     # Modelos treinados (.joblib)
├── notebooks/                  # Pipeline analítico
├── scripts/                    # Automações
├── src/                        # Código modular
├── scratch/                    # Debug
├── tmp/                        # Temporários
└── _wrapper_/                  # Auxiliar

---

## 🔄 Fluxo do Sistema

data/raw
   ↓
data/external (regras probabilísticas)
   ↓
geração de dataset sintético
   ↓
data/processed
   ↓
notebooks (EDA + modelagem)
   ↓
models/
   ↓
app.py (API)
   ↓
frontend

---

## ⚙️ Lógica de Geração do Dataset

1. Seleção de `usage_type`  
2. Seleção de `fuel_type`  
3. Consumo base  
4. Aplicação de eficiência  
5. Conversão para energia (kWh)  
6. Cálculo de emissão de CO₂  
7. Aplicação de ruído  

---

## 🎯 Objetivos da Arquitetura

- Garantir realismo dos dados  
- Evitar determinismo  
- Permitir uso em Machine Learning  
- Facilitar manutenção e escalabilidade  
- Separar claramente dados, lógica e interface  