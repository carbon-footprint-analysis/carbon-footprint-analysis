# Relatório Final: Modelagem de Pegada de Carbono

Este documento consolida os resultados da fase de modelagem do projeto de Análise de Pegada de Carbono, comparando o desempenho de diferentes algoritmos e fornecendo insights sobre os principais direcionadores de emissões de CO2.

---

## 1. Resumo da Abordagem

Seguindo o framework CRISP-DM, avançamos da preparação de dados para o treinamento e avaliação de modelos preditivos. O objetivo foi estimar a variável `co2_emission` com base no consumo energético e contexto operacional.

- **Baseline**: Regressão Linear Simples.
- **Modelo Avançado**: Random Forest Regressor (Ensemble).
- **Métricas de Avaliação**: R² (Coeficiente de Determinação), MAE (Erro Médio Absoluto) e RMSE (Raiz do Erro Quadrático Médio).

---

## 2. Comparativo de Performance

Os resultados demonstraram uma superioridade clara do modelo de Random Forest em capturar a complexidade do dataset.

| Métrica | Regressão Linear (Baseline) | Random Forest Regressor | Evolução |
| :--- | :--- | :--- | :--- |
| **R²** | 0,4438 | **0,9942** | +124% |
| **MAE** | 4.212,13 | **Extremamente Baixo** | Melhoria Drástica |

### Análise:
- **Regressão Linear**: Atuou como um baseline honesto, capturando a tendência linear global, mas falhando em mapear interações específicas entre tipos de combustível e eficiência.
- **Random Forest**: Ao utilizar árvores de decisão, o modelo conseguiu isolar perfeitamente o impacto de variáveis categóricas (como `energy_source`) e lidar com as relações não-lineares do consumo energético.

---

## 3. Importância das Features (Insights)

Através do Random Forest, identificamos os fatores que mais influenciam o cálculo da pegada de carbono:

1.  **energy_kwh**: O volume total de energia consumida é, sem surpresa, o driver número 1.
2.  **energy_source**: A fonte de energia (Térmica vs. Renovável) tem um peso determinante devido ao fator de intensidade de carbono.
3.  **state / usage_type**: Variáveis de contexto que ajudam a refinar a estimativa baseada na infraestrutura regional.

---

## 4. Teste de Robustez (Stress Test)

Para validar a confiabilidade do modelo em cenários reais de coleta de dados imperfeitos, realizamos um teste de estresse injetando ruído sintético.

- **Cenário**: Injeção de 5% de ruído gaussiano na variável de entrada principal (`energy_kwh`), simulando falhas ou imprecisões de sensores.
- **Performance**: O R² reduziu minimamente, de **0,9942** para **0,9905** (uma queda relativa de apenas **0,37%**).
- **Conclusão**: O Random Forest demonstrou alta robustez, mantendo previsões consistentes mesmo com imprecisões significativas de entrada, indicando que o modelo aprendeu padrões sólidos em vez de apenas memorizar os dados brutos.

---

## 5. Conclusão e Próximos Passos

O modelo de **Random Forest** atingiu um nível de excelência (99,4% R²), sendo validado inclusive sob estresse.

### Recomendações:
- **Deploy**: O pipeline está pronto para uso em produção.
- **Monitoramento**: Recomenda-se a revalidação contínua com dados de sensores reais para ajustar possíveis derivas (data drift).

---

## Arquivos Relacionados
- [04_model_training.ipynb](../notebooks/04_model_training.ipynb) (Treinamento Detalhado)
- [detalhes_implementacao_eda_preparacao.md](./detalhes_implementacao_eda_preparacao.md) (Histórico de EDA)
