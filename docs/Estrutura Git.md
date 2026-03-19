carbon-footprint-analysis/
│
├── docs/                         # documentação conceitual e técnica do projeto

│   ├── press\_release.md          # visão do projeto como produto (problema, solução e impacto)

│   ├── faq.md                    # perguntas críticas (decisões, riscos, limitações)

│   ├── crisp\_framework.md        # planejamento seguindo CRISP-DM

│   ├── architecture.md           # arquitetura do sistema (pipeline, fluxo, componentes)

│   ├── dataset\_schema.md         # definição estrutural do dataset (colunas, unidades, regras)

│   └── data\_generation\_methodology.md  # metodologia de geração dos dados (simulação, lógica, variabilidade)

│
├── data/          # datasets utilizados no projeto
│   ├── raw/       # dados originais sem modificação (fonte de verdade)
│   ├── processed/ # dados limpos e transformados prontos para modelagem (cache para evitar reprocessamento)
│   └── external/  # dados externos (APIs, datasets públicos, integrações com terceiros)
│
├── notebooks/     # notebooks usados para exploração de dados, EDA e experimentação
│                  # notebooks devem apenas orquestrar o pipeline, não conter lógica de produção
│
├── src/           # código principal reutilizável do projeto de Data Science
│   ├── init.py
│
│   ├── data/      # preparação de dados (ingestão e limpeza)
│   │   ├── init.py
│   │   ├── ingest.py        # funções para carregar dados de arquivos, APIs ou banco de dados
│   │   └── clean.py         # limpeza de dados, tratamento de nulos, normalização etc.
│
│   ├── features/  # criação de variáveis usadas pelo modelo (feature engineering)
│   │   ├── init.py
│   │   ├── build\_features.py        # pipeline principal de criação de features
│   │   └── aggregation\_features.py  # features derivadas de agregações ou transformações
│
│   ├── models/    # lógica de modelos de machine learning
│   │   ├── init.py
│   │   ├── train.py    # treinamento do modelo
│   │   └── predict.py  # função de previsão usando modelo treinado
│
│   └── pipeline/  # definição dos pipelines oficiais do projeto
│       ├── init.py
│       └── training\_pipeline.py  # pipeline completo de treinamento (data → features → modelo)
│
├── wrapper/       # camada de aplicação que conecta o modelo ao servidor/API
│   ├── init.py
│   ├── app.py     # inicialização da aplicação FastAPI
│   ├── routes.py  # definição das rotas/endpoints da API
│   ├── inference.py # carregamento do modelo treinado e execução de previsões
│   └── settings.py  # configurações da aplicação (paths, parâmetros, variáveis de ambiente)
│
├── frontend/      # interface web da aplicação
│   ├── static/    # arquivos estáticos servidos pelo servidor web
│   │   ├── css/   # folhas de estilo da interface
│   │   │   └── style.css
│   │   ├── js/    # scripts de interação da interface
│   │   │   └── app.js
│   │   └── images/ # imagens usadas pela interface
│   │
│   └── templates/ # templates HTML renderizados pelo backend (ex: Jinja2)
│       └── index.html
│
├── models/        # artefatos de modelos treinados
│   ├── artifacts/ # arquivos serializados do modelo (.pkl, .joblib etc.)
│   └── metadata.json # metadados do modelo (features usadas, data de treino, versão do modelo)
│
├── scripts/       # scripts executáveis para automação de tarefas
│                  # ex: preprocessamento de dados, treinamento batch, atualização de dataset
│
├── deploy/        # configuração de deploy e infraestrutura
│                  # ex: nginx.conf, serviço uvicorn/systemd, scripts de inicialização
│
├── reports/       # relatórios finais do projeto (análises, gráficos e conclusões)
│                  # normalmente gerados a partir de notebooks ou scripts
│
├── logs/          # logs da aplicação e pipeline de ML
│                  # usados para debug, monitoramento e auditoria de execução
│
├── requirements.txt # dependências Python necessárias para rodar o projeto
│
├── .env             # variáveis de ambiente (tokens, caminhos, configs sensíveis)
│                    # não deve ser versionado no Git
│
├── README.md        # documentação principal do projeto (visão geral, arquitetura e instruções de uso)
│
├── PROJECT\_GUIDE.md   # guia rápido explicando como o sistema funciona (dados → modelo → API)
│
├── CONTRIBUTING.md    # regras para colaboração (branches, commits, estrutura de código)
│
└── .gitignore       # lista de arquivos e pastas ignoradas pelo Git

