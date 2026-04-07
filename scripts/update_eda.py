import nbformat as nbf
import os

# Path to the notebook
notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\02_eda_analysis.ipynb'

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Remove the last empty cell if it exists
if len(nb.cells) > 0 and nb.cells[-1].cell_type == 'code' and not nb.cells[-1].source:
    nb.cells.pop()

# Define new cells
new_cells = [
    nbf.v4.new_markdown_cell("## 4. Análise de Tendência Temporal e Detecção de Anomalias\n\nNesta seção, exploramos como as emissões de CO2 variam ao longo do tempo (sazonalidade) e identificamos possíveis outliers no consumo de energia."),
    nbf.v4.new_code_cell("# 4.1 Tendência Temporal por Mês\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nplt.figure(figsize=(12, 6))\nsns.lineplot(data=raw, x='month', y='co2_emission', estimator='sum', errorbar=None, marker='o')\nplt.title('Emissões Totais de CO2 por Mês')\nplt.xlabel('Mês')\nplt.ylabel('Total CO2 (kg)')\nplt.grid(True, linestyle='--', alpha=0.7)\nplt.show()"),
    nbf.v4.new_code_cell("# 4.2 Distribuição por Estação\nplt.figure(figsize=(10, 6))\nsns.boxplot(data=raw, x='season', y='co2_emission', palette='viridis', hue='season', legend=False)\nplt.title('Distribuição de Emissões de CO2 por Estação')\nplt.xlabel('Estação')\nplt.ylabel('Emissões de CO2 (kg)')\nplt.show()"),
    nbf.v4.new_markdown_cell("## 5. Correlação Estatística\n\nAnalisamos a força da relação entre o consumo de energia, a intensidade de carbono da fonte e as emissões resultantes."),
    nbf.v4.new_code_cell("# Heatmap de Correlação\nplt.figure(figsize=(8, 6))\ncorrelation_matrix = raw[['energy_kwh', 'carbon_intensity', 'co2_emission']].corr()\nsns.heatmap(correlation_matrix, annot=True, cmap='RdYlGn', fmt=\".2f\")\nplt.title('Correlação entre Consumo, Intensidade e Emissões')\nplt.show()"),
    nbf.v4.new_markdown_cell("## 6. Detecção de Outliers\n\nUtilizamos o método do Intervalo Interquartil (IQR) para identificar consumos de energia atípicos."),
    nbf.v4.new_code_cell("# Cálculo de IQR para energy_kwh\nQ1 = raw['energy_kwh'].quantile(0.25)\nQ3 = raw['energy_kwh'].quantile(0.75)\nIQR = Q3 - Q1\nlower_bound = Q1 - 1.5 * IQR\nupper_bound = Q3 + 1.5 * IQR\n\noutliers_count = len(raw[(raw['energy_kwh'] < lower_bound) | (raw['energy_kwh'] > upper_bound)])\nprint(f\"Total de outliers detectados em 'energy_kwh': {outliers_count}\")\nprint(f\"Limites aceitáveis: {lower_bound:.2f} a {upper_bound:.2f}\")\n\n# Visualização Gráfica de Outliers\nplt.figure(figsize=(10, 4))\nsns.boxplot(x=raw['energy_kwh'], color='salmon')\nplt.title('Boxplot de Consumo de Energia (kWh) - Verificação de Outliers')\nplt.show()")
]

# Append new cells
nb.cells.extend(new_cells)

# Save the notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook updated successfully.")
