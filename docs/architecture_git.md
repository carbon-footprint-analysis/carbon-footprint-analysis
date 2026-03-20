carbon-footprint-analysis/

│

├── LICENSE                      # licença do projeto (define uso, distribuição e direitos)

├── README.md                   # porta de entrada do projeto (visão geral + instruções rápidas)

│

├── data/                       # camada de dados (separada por estágio no pipeline)

│

│   ├── raw/                    # dados brutos (NUNCA modificar — fonte de verdade)

│   │   ├── ANEEL empreendimento-operacao-historico.csv   # dados reais de geração de energia no Brasil

│   │   ├── EPE - CONSUMO E NUMCONSUMO POR REGIAO...      # consumo energético por região

│   │   ├── EPE - CONSUMO SETOR INDUSTRIAL POR UF.csv     # consumo industrial detalhado

│   │   └── EPE - Consumo-Mensal-Dicionario-de-Dados.pdf  # dicionário oficial dos dados (referência)

│   │

│   ├── external/               # parâmetros e regras usadas na geração do dataset sintético

│   │

│   │   ├── consumption\_profiles.csv

│   │   │   # define faixas de consumo por tipo de uso (base da geração de valores)

│   │

│   │   ├── efficiency\_profiles.csv

│   │   │   # define variação de eficiência por contexto (introduz realismo e evita dataset trivial)

│   │

│   │   ├── fuel\_parameters.csv

│   │   │   # fatores físicos (energia por unidade e emissão de CO₂ por combustível)

│   │

│   │   ├── fuel\_distribution.csv

│   │   │   # probabilidade de cada combustível por tipo de uso (realismo contextual)

│   │

│   │   ├── usage\_distribution.csv

│   │   │   # distribuição global dos tipos de uso (define composição do dataset)

│   │

│   │   ├── company\_profiles.csv

│   │   │   # perfis base de empresas (impacto no consumo e comportamento)

│   │

│   │   ├── company\_size\_distribution\_by\_usage.csv

│   │   │   # distribuição de tamanho das empresas por tipo de uso (mais realismo estrutural)

│   │

│   │   ├── energy\_source\_distribution.csv

│   │   │   # distribuição de fontes elétricas (hidro, solar, eólica, etc.)

│   │   │   # usado quando fuel\_type = electric

│   │

│   │   ├── noise\_parameters.csv

│   │   │   # parâmetros de ruído (aleatoriedade controlada para evitar dataset determinístico)

│   │   │   # essencial para qualidade de ML (evita R² artificial)

│   │

│   ├── processed/              # dados finais gerados pelo pipeline

│       # aqui será salvo o dataset sintético final pronto para análise/modelagem

│

├── docs/                       # documentação conceitual e técnica (guia obrigatório da equipe)

│

│   ├── press\_release.md

│   │   # descrição do projeto como produto (problema, solução e impacto)

│

│   ├── faq.md

│   │   # perguntas críticas (decisões, limitações, riscos e justificativas técnicas)

│

│   ├── crisp\_framework.md

│   │   # planejamento estruturado (CRISP-DM: negócio → dados → modelo → deploy)

│

│   ├── architecture\_git.md

│   │   # organização do repositório e explicação da estrutura de pastas

│

│   ├── dataset\_schema.md

│   │   # definição das colunas do dataset final (contrato de dados)

│

│   └── data\_generation\_methodology.md

│       # lógica de geração do dataset (como os dados são criados e combinados)

│

├── notebooks/                  # análise exploratória (EDA) e testes

│   # NÃO usar para lógica de produção (apenas experimentação)

│

├── src/                        # código principal reutilizável (lógica de produção)

│

│   ├── \_\_init\_\_.py             # inicializa o pacote Python

│

│   ├── data/                   # ingestão e preparação de dados

│   │   ├── \_\_init\_\_.py

│   │   # ingest.py (futuro): leitura padronizada dos CSVs

│   │   # clean.py  (futuro): limpeza e normalização

│

│   ├── features/               # criação de features

│   │   ├── \_\_init\_\_.py

│   │   # transformação de dados em variáveis úteis para o modelo

│

│   ├── models/                 # lógica de machine learning

│   │   ├── \_\_init\_\_.py

│   │   # treinamento, avaliação e inferência

│

│   └── pipeline/               # pipelines oficiais do projeto

│       ├── \_\_init\_\_.py

│       # pipeline completo (geração → features → modelo)

│

├── scripts/                    # scripts executáveis (automação)

│   # generate\_dataset.py será criado aqui (coração do projeto)

│

├── wrapper/                    # camada de aplicação (API)

│   └── \_\_init\_\_.py

│   # integração do modelo com endpoints (FastAPI)

│

├── frontend/                   # interface do usuário

│   ├── static/                 # css, js e imagens

│   └── templates/              # HTML renderizado

│

├── models/                     # modelos treinados

│   └── artifacts/              # arquivos do modelo (.pkl, .joblib)

│

├── reports/                    # relatórios finais (insights, gráficos)

├── logs/                       # logs do sistema (debug e auditoria)

├── deploy/                     # configuração de deploy (infraestrutura)

