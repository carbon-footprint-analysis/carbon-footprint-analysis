# Relatório de Implantação: Fase 6 CRISP-DM

Este documento detalha o encerramento do ciclo CRISP-DM para o projeto de Pegada de Carbono, focando na transição do modelo treinado para uma ferramenta de uso prático e escalonável.

---

## 1. Persistência do Modelo (Serialization)

Para que o modelo possa ser utilizado sem a necessidade de reprocessar os dados de treinamento (100.000 linhas), realizamos a persistência do pipeline completo.

- **Artefato**: `models/carbon_footprint_rf_v1.joblib`
- **Conteúdo**: O arquivo contém tanto o **regressor (Random Forest)** quanto os **transformadores (StandardScaler e OneHotEncoder)**. Isso garante que a normalização e codificação dos novos dados de entrada sejam idênticas às usadas no treino.

---

## 2. Interface de Predição (Deployment Interfaces)

Implementamos duas formas de interação com o modelo de inteligência:

### 2.1. Notebook de Demonstração (`05_model_deployment.ipynb`)
Destinado a analistas de dados e interessados em simulações visuais:
- Carregamento transparente do modelo.
- Função de inferência pronta para uso.
- Exemplos de cenários de sustentabilidade.

### 2.2. Ferramenta CLI (`scripts/predict_co2.py`)
Destinada a integração técnica e automação:
- **Uso**: `python scripts/predict_co2.py --kwh [valor] --state [sigla] --type [tipo] --source [fonte] --month [mes]`
- **Saída**: Relatório formatado com a estimativa da pegada de carbono em kg CO2.

---

## 3. Validação de Integridade

O modelo implantado foi validado contra o modelo original em memória:
- **R² Original**: 0,9942
- **R² Recarregado**: 0,9942
- **Consistência**: Confirmamos que não houve perda de precisão ou erro de desserialização (unpickling errors).

---

## 4. Conclusão do Ciclo

Com a entrega desta fase, o projeto cumpre todas as etapas do framework CRISP-DM:
1. **Business Understanding**: Objetivo de estimar emissões definido.
2. **Data Understanding**: EDA profunda e insights temporais.
3. **Data Preparation**: Pipeline de pré-processamento estruturado.
4. **Modeling**: Comparação entre Regressão Linear e Random Forest.
5. **Evaluation**: Validação de métricas e teste de robustez (stress test).
6. **Deployment**: Modelo persistido e ferramentas de predição entregues.

---

## Arquivos Relacionados
- [05_model_deployment.ipynb](../notebooks/05_model_deployment.ipynb) (Guia de Uso)
- [predict_co2.py](../scripts/predict_co2.py) (Ferramenta Terminal)
- [relatorio_final_modelagem.md](./relatorio_final_modelagem.md) (Histórico de Resultados)
