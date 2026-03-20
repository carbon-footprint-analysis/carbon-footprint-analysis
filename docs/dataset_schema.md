# 📊 Dataset Schema – Carbon Footprint Analysis

Este documento define a estrutura, variáveis e premissas fundamentais do dataset utilizado no projeto.

---

## 🎯 Objetivo

O dataset foi projetado para:

- estimar emissões de CO₂  
- permitir comparação justa entre diferentes fontes de energia  
- suportar análises de dados e modelos de machine learning  
- gerar insights interpretáveis para tomada de decisão  

---

## 🧠 Princípio Central do Modelo

O dataset é baseado em duas relações fundamentais:

Energia (kWh) = fuel_amount × energy_factor  
CO₂ = fuel_amount × emission_factor  

👉 Para garantir comparabilidade, todas as fontes são convertidas para uma unidade comum: **kWh**.

---

## 📦 Estrutura do Dataset

| Coluna            | Tipo        | Descrição |
|------------------|------------|------------|
| fuel_type        | categórica | Tipo de combustível |
| fuel_amount      | numérica   | Quantidade consumida |
| energy_kwh       | numérica   | Energia equivalente gerada |
| co2_emission     | numérica   | Emissão estimada de CO₂ |
| energy_factor    | numérica   | Fator de conversão para kWh |
| emission_factor  | numérica   | Fator de emissão por unidade |
| usage_type       | categórica | Contexto de uso |
| energy_source    | categórica | Fonte da energia elétrica |

---

## ⚙️ Definição das Variáveis

### 🔹 fuel_type

Tipo de fonte de energia:

- gasolina  
- diesel  
- etanol  
- gnv (gás natural)  
- glp (gás liquefeito de petróleo)  
- biogás  
- elétrico  

---

### 🔹 fuel_amount

Quantidade consumida:

- litros (L) → combustíveis líquidos  
- m³ → gases  
- kg → GLP  
- kWh → energia elétrica  

---

### 🔹 energy_kwh

Energia equivalente gerada:

energy_kwh = fuel_amount × energy_factor  

---

### 🔹 co2_emission

Emissão estimada de CO₂:

co2_emission = fuel_amount × emission_factor  

---

## ⚡ Fatores de Energia (energy_factor)

Valores médios de densidade energética:

| Combustível | Valor (kWh/unidade) |
|------------|---------------------|
| gasolina   | 8.9 kWh/L |
| diesel     | 10.7 kWh/L |
| etanol     | 6.1 kWh/L |
| gnv        | 10.5 kWh/m³ |
| glp        | 13.6 kWh/kg |
| biogás     | 6.0 kWh/m³ |
| elétrico   | 1.0 kWh/kWh |

---

## 🌍 Fatores de Emissão (emission_factor)

Valores médios de emissão de CO₂:

| Combustível | Valor |
|------------|------|
| gasolina   | 2.31 kg CO₂/L |
| diesel     | 2.68 kg CO₂/L |
| etanol     | 1.5 kg CO₂/L |
| gnv        | 2.75 kg CO₂/m³ |
| glp        | 3.0 kg CO₂/kg |
| biogás     | 1.5 kg CO₂/m³ |
| elétrico   | variável |

---

## ⚡ Emissão de Energia Elétrica

A energia elétrica não possui emissão direta. O impacto depende da fonte:

| Fonte        | Emissão (kg CO₂/kWh) |
|-------------|----------------------|
| hydro       | 0.024 |
| solar       | 0.045 |
| wind        | 0.012 |
| natural_gas | 0.400 |
| coal        | 0.820 |
| nuclear     | 0.012 |
| mixed       | 0.100 |

👉 A mesma quantidade de energia pode gerar emissões diferentes dependendo da fonte.

---

## 🏭 usage_type

Contexto de uso da energia:

- transport_road  
- transport_naval  
- agriculture  
- industry_metallurgy  
- industry_chemical  
- industry_manufacturing  
- energy_generation  
- residential  
- commercial  

---

## 🔌 energy_source

Indica como a energia elétrica foi gerada.

👉 Aplicável apenas quando:

fuel_type = electric  

👉 Caso contrário:

energy_source = null  

---

## 📚 Referências

Os valores utilizados são baseados em:

- IPCC  
- EPA  
- IEA  
- ANP (Brasil)  
- EPE / ONS (matriz energética brasileira)  

---

## 🎯 Princípios de Design

O dataset foi projetado para ser:

- simples  
- interpretável  
- comparável entre diferentes fontes de energia  

---

## 💡 Insight Principal

A mesma quantidade de energia pode gerar emissões de CO₂ muito diferentes dependendo do combustível e da fonte de energia utilizada.