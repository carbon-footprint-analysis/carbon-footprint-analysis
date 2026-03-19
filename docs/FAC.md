# ❓ FAQ – Carbon Footprint Analysis


---


### Quem é o usuário do modelo?
- Analistas de dados e sustentabilidade  
- Empresas interessadas em monitorar emissões  
- Sistemas internos de apoio à decisão  


---


### Qual decisão será tomada com o modelo?
- Comparar o impacto ambiental entre diferentes fontes de energia  
- Identificar oportunidades de redução de emissões  
- Apoiar decisões operacionais com foco em eficiência energética  


---


### O que exatamente será previsto?
- Estimativa de emissão de CO₂ (`co2_emission`) com base em variáveis como:
  - tipo de combustível  
  - consumo energético  
  - contexto de uso  
  - eficiência  
  - período (tempo)  


---


### Como interpretar o resultado?
- Valores mais altos indicam maior impacto ambiental  
- Comparações entre cenários ajudam a identificar alternativas mais eficientes  
- O foco não é o valor absoluto isolado, mas sim a análise comparativa e de padrões  


---


### Com que frequência o modelo será usado?
- Batch (principal): geração de análises e relatórios periódicos  
- Sob demanda: simulação de cenários (ex: comparação entre combustíveis)  


---


### Quais dados estão disponíveis?
- Dataset sintético estruturado com:
  - consumo energético (`fuel_amount`)  
  - tipo de combustível (`fuel_type`)  
  - contexto de uso (`usage_type`)  
  - eficiência (`efficiency_factor`)  
  - fonte de energia elétrica (`energy_source`)  
  - variável temporal (`date`)  


👉 Baseado em parâmetros reais de instituições como IPCC, IEA, ANP e EPE/ONS.


---


### Exemplo de uso do modelo


Entrada:
- fuel_type: diesel  
- fuel_amount: 100 L  
- usage_type: transport_road  
- efficiency_factor: 1.0  
- date: 2024-09-15  


Saída:
- co2_emission ≈ valor estimado de CO₂  


👉 Esse resultado pode ser comparado com outros combustíveis ou períodos para análise.


---


### Quais riscos existem?
- Dependência de premissas do dataset sintético  
- Sensibilidade à calibração do ruído e da eficiência  
- Possível simplificação da realidade em cenários complexos  
- Risco de má interpretação dos resultados sem contexto adequado  


---