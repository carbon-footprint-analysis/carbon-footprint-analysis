carbon-footprint-analysis/

│

├── docs/                         # documentação conceitual e estratégica do projeto (leitura obrigatória antes de codar)

│   ├── press\_release.md          # visão do projeto como produto (problema, solução, impacto e proposta de valor)

│   ├── faq.md                    # perguntas críticas (decisões técnicas, riscos, limitações e trade-offs)

│   ├── crisp\_framework.md        # planejamento seguindo CRISP-DM (entendimento do problema até deploy)

│   ├── architecture.md           # arquitetura do sistema (fluxo de dados, componentes e integração)

│   ├── dataset\_schema.md         # definição das colunas e estrutura do dataset final (contrato de dados)

│   └── data\_generation\_methodology.md  # lógica de geração dos dados sintéticos (regras, variabilidade e realismo)

│

├── data/                         # camada de dados do projeto (organizada por estágio do dado)

│   ├── raw/                      # dados originais (NUNCA modificar — fonte de verdade)

│   │   ├── aneel\_generation.csv  # dados reais de geração de energia (base para matriz energética)

│   │   ├── epe\_consumption.csv   # dados reais de consumo energético por setor/região

│   │   └── ...                   # outros datasets brutos utilizados como referência

│   │

│   ├── external/                 # tabelas auxiliares usadas para gerar o dataset sintético (regras do sistema)

│   │   ├── consumption\_profiles.csv       # faixas de consumo por tipo de uso (base para geração de valores)

│   │   ├── efficiency\_profiles.csv        # variação de eficiência por uso (introduz realismo e variabilidade)

│   │   ├── fuel\_parameters.csv            # fatores físicos (energia e emissão por combustível)

│   │   ├── fuel\_distribution.csv          # probabilidade de uso de combustíveis por contexto

│   │   ├── usage\_distribution.csv         # distribuição global dos tipos de uso (define proporção do dataset)

│   │   ├── company\_profiles.csv           # perfis de empresas (impacto no consumo)

│   │   ├── company\_size\_distribution.csv  # distribuição de tamanho das empresas (small, medium, large)

│   │   └── energy\_source\_distribution.csv # distribuição das fontes elétricas (hidro, solar, etc.)

│   │

│   └── processed/                # dados finais prontos para análise e modelagem

│       └── synthetic\_energy\_dataset.csv  # dataset sintético gerado pelo pipeline (principal output do projeto)

│

├── notebooks/                   # notebooks para exploração (EDA) e testes (não usar para lógica final)

│                               # servem para análise, validação e visualização dos dados

│

├── src/                         # código principal reutilizável do projeto (lógica de produção)

│   ├── \_\_init\_\_.py              # inicializa o pacote Python do projeto

│

│   ├── data/                    # ingestão e tratamento de dados

│   │   ├── \_\_init\_\_.py

│   │   ├── ingest.py            # leitura padronizada dos CSVs (raw e external)

│   │   └── clean.py             # limpeza e padronização dos dados

│

│   ├── features/                # criação de variáveis (feature engineering)

│   │   ├── \_\_init\_\_.py

│   │   ├── build\_features.py        # criação das features principais do modelo

│   │   └── aggregation\_features.py  # features derivadas (agrupamentos, médias, etc.)

│

│   ├── models/                  # lógica de machine learning

│   │   ├── \_\_init\_\_.py

│   │   ├── train.py             # treinamento do modelo

│   │   └── predict.py           # inferência (previsões)

│

│   └── pipeline/                # pipelines oficiais do projeto

│       ├── \_\_init\_\_.py

│       └── training\_pipeline.py # fluxo completo: dados → features → modelo

│

├── wrapper/                     # camada de aplicação (API)

│   ├── \_\_init\_\_.py

│   ├── app.py                   # inicialização da aplicação (FastAPI)

│   ├── routes.py                # definição dos endpoints da API

│   ├── inference.py             # carregamento do modelo e execução de previsões

│   └── settings.py              # configurações gerais (paths, variáveis, ambiente)

│

├── frontend/                    # interface do usuário (camada visual)

│   ├── static/                  # arquivos estáticos

│   │   ├── css/style.css        # estilos da aplicação

│   │   ├── js/app.js            # lógica de interação do frontend

│   │   └── images/              # imagens utilizadas na interface

│   │

│   └── templates/

│       └── index.html           # página principal renderizada pelo backend

│

├── models/                      # artefatos de modelos treinados

│   ├── artifacts/               # arquivos do modelo (.pkl, .joblib)

│   └── metadata.json            # informações do modelo (features, versão, data)

│

├── scripts/                     # scripts executáveis (automação)

│   └── generate\_dataset.py      # script principal para geração do dataset sintético

│

├── deploy/                      # configuração de deploy (infraestrutura)

│                               # ex: nginx, uvicorn, scripts de inicialização

│

├── reports/                     # relatórios finais (gráficos, análises e insights)

│

├── logs/                        # logs do sistema (execução, erros, auditoria)

│

├── requirements.txt             # dependências Python do projeto

│

├── .env                         # variáveis sensíveis (não versionar)

│

├── README.md                    # visão geral do projeto (porta de entrada)

│

├── PROJECT\_GUIDE.md             # guia rápido de funcionamento (como usar o sistema)

│

├── CONTRIBUTING.md              # regras para contribuição (padrões, commits, organização)

│

└── .gitignore                   # arquivos ignorados pelo Git

