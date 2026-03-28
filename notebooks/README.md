# 🌍 CarbonFootprintAnalysis - Documentação Técnica (Fase 1 & 2)

Este projeto tem como objetivo analisar e estimar a pegada de carbono associada ao consumo energético em diferentes setores e regiões do Brasil. Abaixo estão detalhadas as etapas de estruturação, extração e limpeza de dados realizadas.

## 📁 1. Estrutura do Projeto
Para garantir a organização e reprodutibilidade, o projeto foi estruturado seguindo as melhores práticas de Ciência de Dados:

* **`Analise_Pegada_Carbono/`** (Raiz)
    * **`dados/`**
        * `brutos/`: Armazena o dataset original (`consumo_energia_emissoes_br.csv`).
        * `processados/`: Armazena o dado limpo e com novas variáveis (`dados_energia_limpos.csv`).
    * **`notebooks/`**: Contém os scripts de execução e análise.
    * **`docs/`**: Documentação e relatórios visuais.
    * **`scripts/`**: Funções auxiliares em Python.

---

## 🛠️ 2. Extração e Carregamento de Dados
O conjunto de dados utilizado é de natureza **sintética**, porém construído sobre regras estatísticas reais derivadas da **EPE (Empresa de Pesquisa Energética)** e **ANEEL**.

* **Volume de Dados:** 100.000 registros.
* **Atributos Originais:** ID da empresa, Data, Estado, Tipo de Uso (Setor), Porte, Tipo de Combustível, Consumo (kWh), Fonte de Energia e Emissão de CO₂.

---

## 🧹 3. Processamento e Limpeza (Data Cleaning)
Nesta etapa, transformamos os dados brutos em informação útil para cálculos estatísticos:

1.  **Tipagem de Dados:** Conversão da coluna `date` para o formato *datetime*.
2.  **Padronização Numérica:** As colunas `energy_kwh` e `co2_emission` foram convertidas de texto para *float64*, com tratamento de separadores decimais.
3.  **Validação de Nulos:** Confirmamos que o dataset não possui valores ausentes, garantindo a integridade da análise.

---

## 📊 4. Engenharia de Atributos e Insights Iniciais
Criamos novas métricas para facilitar a interpretação do impacto ambiental:

* **Intensidade de Carbono:** Calculada pela razão $CO₂ / kWh$.
    * *Insight:* A fonte **Térmica** apresentou intensidade de **0.60 kg CO₂/kWh**, enquanto fontes renováveis (Solar/Eólica) mantiveram-se em **0.01 kg CO₂/kWh**.
* **Categorização de Impacto:** Criamos a variável `impacto_ambiental` dividida em três faixas baseadas em quartis:
    * **Baixo Impacto:** 33.0% dos dados.
    * **Médio Impacto:** 33.0% dos dados.
    * **Alto Impacto:** 34.0% dos dados.

---

## 🤖 5. Modelo Preditivo (MVP)
Foi implementado um modelo de **Árvore de Decisão** para classificar o impacto ambiental com base no consumo e setor.
* **Acurácia:** ~80%.
* **Destaque:** O modelo demonstrou alta precisão (0.90) na identificação de registros de "Alto Impacto", sendo uma ferramenta eficaz para triagem ambiental.

---

### **Como Executar**
1. Os dados originais devem ser colocados em `dados/brutos/`.
2. O script de limpeza gera automaticamente o arquivo em `dados/processados/`.
3. O modelo pode ser treinado utilizando o arquivo processado para garantir maior performance.