PROJETO: Synthetic Energy Dataset Generator (foco Brasil)



OBJETIVO:

Construir um gerador de dataset sintético para consumo de energia e emissões de CO₂ que seja:

\- realista

\- não determinístico

\- fisicamente consistente

\- adequado para Machine Learning (sem R² artificial)



\---



PRINCÍPIO CENTRAL:

Isso NÃO é um dataset aleatório.

Isso é um MOTOR DE SIMULAÇÃO probabilístico baseado em regras.



TODOS os valores devem vir de arquivos CSV (NENHUM valor fixo no código).



\---



ESTRUTURA DO DADO:



Cada linha representa um evento de consumo energético:



company\_id, date, usage\_type, fuel\_type, fuel\_amount, energy\_kwh, co2\_emission, energy\_source, efficiency\_factor



\---



FONTES DE DADOS (CSV):



Todos localizados em: data/external/



1\. consumption\_profiles.csv

&#x20;  - Consumo base condicionado por (usage\_type, fuel\_type)

&#x20;  - Contém: min, max, unit, distribution\_type

&#x20;  - Define a UNIDADE de fuel\_amount



2\. efficiency\_profiles.csv

&#x20;  - Define eficiência por usage\_type

&#x20;  - Contém: eff\_min, eff\_max, distribution\_type



3\. fuel\_parameters.csv

&#x20;  - Define:

&#x20;    - energy\_factor (kWh por unidade)

&#x20;    - co2\_factor (kg CO₂ por unidade)

&#x20;  - SOMENTE para combustíveis NÃO elétricos



4\. fuel\_distribution.csv

&#x20;  - Define P(fuel\_type | usage\_type)



5\. usage\_distribution.csv

&#x20;  - Define P(usage\_type)



6\. company\_profiles.csv

&#x20;  - Define multiplicadores de consumo por porte da empresa



7\. company\_size\_distribution\_by\_usage.csv

&#x20;  - Define P(company\_size | usage\_type)



8\. energy\_source\_distribution.csv

&#x20;  - Define P(energy\_source | fuel\_type = electric)



9\. energy\_source\_emission\_factors.csv

&#x20;  - Define emissão (kg CO₂/kWh) por fonte elétrica

&#x20;  - USADO APENAS quando fuel\_type = electric



10\. noise\_parameters.csv

&#x20;  - Define:

&#x20;    - distribution\_type

&#x20;    - noise\_std (desvio relativo)

&#x20;    - random\_seed



\---



PIPELINE DE GERAÇÃO (ORDEM OBRIGATÓRIA):



1\. usage\_type ← sample(usage\_distribution)



2\. fuel\_type ← sample(fuel\_distribution | usage\_type)



3\. company\_size ← sample(company\_size\_distribution\_by\_usage | usage\_type)



4\. company\_multiplier ← lookup(company\_profiles)



5\. base\_consumption ← sample(consumption\_profiles | usage\_type, fuel\_type)



6\. fuel\_amount = base\_consumption × company\_multiplier



7\. efficiency\_factor ← sample(efficiency\_profiles | usage\_type)



8\. Ajuste de eficiência:

&#x20;  fuel\_amount = fuel\_amount / efficiency\_factor



9\. Conversão energética:

&#x20;  energy\_kwh = fuel\_amount × energy\_factor



10\. Emissão base:



&#x20;  IF fuel\_type ≠ electric:

&#x20;      co2\_emission = fuel\_amount × co2\_factor



&#x20;  IF fuel\_type = electric:

&#x20;      energy\_source ← sample(energy\_source\_distribution)

&#x20;      co2\_emission = energy\_kwh × emission\_factor



11\. Aplicar ruído multiplicativo:

&#x20;  co2\_emission = co2\_emission × (1 + ε)

&#x20;  ε \~ distribuição definida em noise\_parameters



\---



REGRAS OBRIGATÓRIAS:



\- energy\_source = NULL se fuel\_type ≠ electric

\- NÃO pode existir comportamento determinístico

\- TODA aleatoriedade deve vir dos CSVs

\- Probabilidades devem somar 1

\- Chaves devem ser consistentes (usage\_type, fuel\_type)

\- Unidades devem ser respeitadas (L, kg, m³, kWh)

\- NÃO usar números mágicos



\---



PARÂMETROS DE GERAÇÃO:



\- n\_rows: número de registros (ex: 2000)

\- date\_range: intervalo de datas (ex: 2024-01-01 a 2025-12-31)

\- frequency: diária ou aleatória



EMPRESAS:

\- Gerar um conjunto fixo de empresas (ex: 100–500)

\- Cada empresa tem um company\_size fixo

\- Cada linha referencia uma empresa existente (NÃO gerar nova por linha)



\---



RUÍDO:



\- Tipo: multiplicativo

\- Fórmula:

&#x20; co2\_final = co2\_base × (1 + ε)

\- ε \~ distribuição com média 0 e desvio noise\_std

\- random\_seed garante reprodutibilidade



\---



OUTPUT:



Salvar em:

data/processed/carbon\_footprint\_dataset.csv



\---



NÃO FAZER:



\- NÃO simplificar lógica

\- NÃO remover etapas probabilísticas

\- NÃO introduzir constantes arbitrárias

\- NÃO misturar fuel com energy\_source



\---



ENTREGÁVEL:



Código Python modular contendo:

\- generator.py

\- funções de amostragem

\- controle de seed

\- separação clara de responsabilidades



\---



FORMATO DE RESPOSTA:



\- Análise

\- Problemas (se houver)

\- Sugestões (se houver)

\- Veredito

