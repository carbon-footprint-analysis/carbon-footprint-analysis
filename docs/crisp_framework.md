CRISP-DM Framework


1. Business Understanding


Problema de negócio:
Empresas e organizações têm dificuldade em entender e quantificar o impacto ambiental de suas atividades energéticas, especialmente quando diferentes fontes de energia e combustíveis estão envolvidas.


Objetivo:
Desenvolver um modelo capaz de estimar emissões de CO₂ com base em padrões de consumo energético, considerando contexto de uso, eficiência e variações ao longo do tempo.


KPI principal:
Erro médio da estimativa de CO₂ (MAE ou RMSE)


Critério de sucesso:
- O modelo deve gerar estimativas coerentes e interpretáveis  
- Deve capturar variações relevantes (ex: sazonalidade e eficiência)  
- Deve permitir comparação clara entre diferentes fontes de energia  




2. Data Understanding


Fontes de dados:
- Dataset sintético gerado com base em parâmetros reais (IPCC, IEA, ANP, EPE/ONS)  
- Regras de negócio e simulação de consumo energético  


Variável target:
co2_emission


Período dos dados:
- Dados simulados com base em até 2 anos  
- Frequência diária  


Problemas conhecidos:
- Dataset sintético (não representa casos reais específicos)  
- Dependência de premissas para geração dos dados  
- Possível sensibilidade à calibração do ruído e eficiência  
















3. Data Preparation


Pipeline esperado:
ingest → limpeza → feature engineering → split


Etapas:
- Validação e ingestão dos dados sintéticos gerados  
- Validação de consistência (ex: consumo vs contexto)  
- Criação de features:
  - energy_kwh  
  - efficiency_factor  
  - extração de tempo (ex: mês a partir de date)  
- Tratamento de variáveis categóricas  
- Separação treino/teste  




4. Modeling


Baseline:
Regressão Linear simples


Modelos candidatos:
- Regressão Linear  
- Random Forest Regressor  
- Gradient Boosting (ex: XGBoost ou LightGBM)  




5. Evaluation


Métricas:
- MAE (Mean Absolute Error)  
- RMSE (Root Mean Squared Error)  
- R² (coeficiente de determinação)  




6. Deployment (visão inicial)


Tipo de inferência:
- batch → geração de relatórios e análises  
- API → estimativa em tempo real (ex: input de consumo no site)