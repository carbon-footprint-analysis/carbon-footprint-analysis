\# ⚙️ Metodologia de Geração de Dados – Carbon Footprint Analysis



Este documento descreve o processo de geração do dataset sintético, incluindo lógica de simulação, variabilidade e regras para garantir realismo nos dados.



\---



\## 🎯 Objetivo



Gerar um dataset sintético, porém realista, que:



\- simule padrões reais de consumo energético

\- represente diferentes contextos de uso

\- incorpore variabilidade e incerteza

\- permita análises robustas e treinamento de modelos



\---



\##

&#x20;📌 Unidade de Observação



Cada linha do dataset representa:



👉 um evento de consumo de energia associado a um contexto específico em um determinado momento no tempo.



Exemplos:



\- consumo de combustível em transporte

\- uso de energia elétrica em residências ou indústrias

\- consumo energético em processos produtivos



\---



\## 🧩 Estrutura Conceitual



As variáveis do dataset podem ser interpretadas em blocos:



\- Fonte de energia → fuel\_type, energy\_source

\- Consumo → fuel\_amount, energy\_kwh

\- Emissão → co2\_emission

\- Contexto → usage\_type

\- Eficiência → efficiency\_factor

\- Tempo → date



\---



\## ⚙️ Pipeline de Geração



O dataset é gerado seguindo as etapas abaixo:



1\. Selecionar tipo de combustível (fuel\_type)

2\. Definir contexto de uso (usage\_type)

3\. Gerar data (date)

4\. Gerar consumo base (fuel\_amount)

5\. Ajustar consumo por sazonalidade

6\. Converter para energia (energy\_kwh)

7\. Aplicar fator de eficiência (efficiency\_factor)

8\. Calcular emissão de CO₂

9\. Adicionar ruído estatístico

10\. Registrar a observação



\---



\## 📅 Modelagem Temporal (date)



A variável temporal permite simular padrões realistas:



Formato sugerido:

YYYY-MM-DD



\### 🔹 Sazonalidade



O consumo varia ao longo do tempo:



\- meses quentes (dez–mar)

&#x20; → maior consumo elétrico (ar-condicionado)



\- meses frios (jun–ago)

&#x20; → menor consumo elétrico no Brasil



\---



\## ⚡ Variação da Matriz Energética



Para energia elétrica, a fonte de geração varia ao longo do ano:



\- períodos secos (ago–out)

&#x20; → maior uso de termelétricas

&#x20; → aumento nas emissões



\- períodos chuvosos

&#x20; → maior uso de hidrelétricas

&#x20; → redução nas emissões



👉 Isso permite que o mesmo consumo gere emissões diferentes dependendo do período.



\---



\## ⚙️ Modelagem de Consumo (fuel\_amount)



O consumo deve respeitar o contexto:



\- transport\_road → consumo médio

\- transport\_naval → consumo alto

\- agriculture → consumo médio

\- industry → consumo alto

\- residential → consumo baixo

\- commercial → consumo médio



👉 O objetivo é evitar valores irreais.



\---



\## ⚙️ Eficiência Energética (efficiency\_factor)



Representa variações reais de eficiência:



\- 0.8 → baixa eficiência

\- 1.0 → padrão

\- 1.2 → alta eficiência



👉 Impacta diretamente as emissões finais.



\---



\## 🌍 Modelagem de Emissões (CO₂)



A emissão não é totalmente determinística.



Modelo utilizado:



CO₂ = energy\_kwh × emission\_base × efficiency\_factor + ruído



👉 O termo de ruído adiciona variabilidade realista.



\---



\## 🎲 Ruído Estatístico



Para evitar dados artificiais:



\- adicionar pequena variação aleatória

\- manter coerência com o contexto

\- evitar padrões perfeitamente lineares



👉 Isso melhora a qualidade para machine learning.



\---



\## 📊 Tamanho do Dataset



Recomendações:



\- mínimo: 1000 registros

\- ideal: \~2000 registros

\- máximo: conforme necessidade do projeto



\---



\## 🔗 Relações Importantes



\- consumo ↑ → energia ↑ → CO₂ ↑

\- tipo de combustível → impacto diferente

\- fonte elétrica → grande variação de emissão

\- eficiência → altera emissão

\- tempo → influencia consumo e matriz



\---



\## 🎯 Princípios de Design



O processo foi projetado para ser:



\- realista

\- não determinístico

\- interpretável

\- consistente com fundamentos físicos



\---



\## 💡 Insight Principal



A emissão de CO₂ não depende apenas do consumo, mas também da eficiência, do contexto e do período do ano.

