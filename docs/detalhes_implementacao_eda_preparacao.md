# Relatório de Implementação: Finalização do EDA e Início da Preparação do Modelo

Este documento detalha as atividades realizadas na etapa atual do projeto de Análise de Pegada de Carbono, cobrindo a conclusão da Análise Exploratória de Dados (EDA) e a configuração inicial do pipeline de preparação para Machine Learning.

---

## 1. Conclusão da Análise Exploratória de Dados (EDA)

O notebook `notebooks/02_eda_analysis.ipynb` foi atualizado com análises críticas para garantir a robustez do futuro modelo preditivo.

### 1.1. Análise de Tendência Temporal
A visualização do tempo é fundamental para entender a **sazonalidade** do consumo energético.
- **Implementação**: Geramos um gráfico de linha das emissões totais de CO2 agregadas por mês.
- **Insights**: Permite identificar se há picos de emissão em meses específicos (ex: verão ou inverno), o que informa ao modelo sobre variações cíclicas.
- **Visualização Auxiliar**: Criamos um boxplot de emissões agrupado por estação do ano (`season`) para entender a variabilidade estatística em cada período.

### 1.2. Correlação Estatística
Entender como as variáveis se relacionam ajuda na seleção de atributos (**Feature Selection**).
- **Implementação**: Geramos um **Heatmap de Correlação** entre as variáveis numéricas: `energy_kwh` (consumo), `carbon_intensity` (fator de emissão da fonte) e `co2_emission` (target).
- **Justificativa**: Confirmar que o consumo de energia e a intensidade de carbono são os principais drivers das emissões totais.

### 1.3. Detecção de Outliers (Anomalias)
Dados discrepantes podem prejudicar o treinamento de modelos lineares.
- **Implementação**: Utilizamos o método do **Intervalo Interquartil (IQR)** na coluna `energy_kwh`.
- **Resultado**: Calculamos os limites inferior e superior para identificar consumos de energia que fogem do padrão esperado, permitindo um tratamento posterior (remoção ou ajuste).

---

## 2. Início da Preparação do Modelo (Data Preparation)

Foi criado o notebook `notebooks/03_model_preparation.ipynb`, estabelecendo a base para o treinamento.

### 2.1. Divisão do Dataset
Para validar a performance do modelo de forma justa, os dados foram divididos:
- **Proporção**: 80% para treinamento e 20% para teste (validação final).
- **Reprodutibilidade**: Definimos um `random_state` fixo para garantir que os resultados sejam consistentes em execuções futuras.

### 2.2. Pipeline de Pré-processamento
Configuramos a estrutura básica de transformação usando `ColumnTransformer` e `Pipeline` do Scikit-Learn:
- **Escalonamento (Scaling)**: Variáveis como `energy_kwh` foram preparadas para o `StandardScaler`, garantindo que todas as features numéricas tenham a mesma escala.
- **Codificação Categórica (Encoding)**: Variáveis como `sector`, `state` e `energy_source` foram preparadas para o `OneHotEncoder`, transformando categorias em colunas binárias processáveis por algoritmos matemáticos.

---

## 3. Resumo Técnico

| Categoria | Implementação Realizada | Ferramenta Utilizada | Arquivo Impactado |
| :--- | :--- | :--- | :--- |
| **EDA** | Gráficos de Tendência e Boxplots | Matplotlib / Seaborn | `02_eda_analysis.ipynb` |
| **Estatística** | Heatmap de Correlação | Seaborn | `02_eda_analysis.ipynb` |
| **Qualidade** | Detecção de Outliers (IQR) | Pandas / Numpy | `02_eda_analysis.ipynb` |
| **ML Prep** | Split Treino/Teste (80/20) | Scikit-Learn | `03_model_preparation.ipynb` |
| **ML Prep** | Pipeline de Scaling/Encoding | Scikit-Learn | `03_model_preparation.ipynb` |

---

## Próximos Passos
1. **Seleção de Modelos**: Testar Baseline de Regressão Linear.
2. **Treinamento**: Avaliar modelos de árvore (Random Forest) para capturar relações não lineares detectadas no EDA.
3. **Avaliação**: Validar métricas de erro (MAE/RMSE) no conjunto de teste.
