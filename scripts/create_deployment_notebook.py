import nbformat as nbf
import os

# Path to the new notebook
notebook_path = r'c:\Repositorio\carbon-footprint-analysis\notebooks\05_model_deployment.ipynb'

# Create a new notebook
nb = nbf.v4.new_notebook()

# Define cells
cells = [
    nbf.v4.new_markdown_cell("# 05 - Implantação e Predição (Deployment)\n\nNeste notebook, demonstramos como utilizar o modelo treinado de Pegada de Carbono para realizar predições em tempo real. O modelo foi salvo em formato `.joblib` e contém todo o pipeline de pré-processamento necessário."),
    nbf.v4.new_code_cell("import pandas as pd\nimport joblib\nimport os\n\n# Carregar o modelo\nmodel_path = os.path.join('..', 'models', 'carbon_footprint_rf_v1.joblib')\nmodel = joblib.load(model_path)\n\nprint(\"✅ Modelo carregado com sucesso!\")"),
    nbf.v4.new_markdown_cell("## 1. Função de Predição Customizada\n\nCriamos uma função auxiliar que recebe os dados de entrada, os formata conforme o esperado pelo modelo e retorna o valor da emissão de CO2."),
    nbf.v4.new_code_cell("def estimate_co2(energy_kwh, state, usage_type, energy_source, month):\n    # Determinar a estação com base no mês\n    def get_season(m):\n        if m in [12, 1, 2]: return 'Verao'\n        if m in [3, 4, 5]: return 'Outono'\n        if m in [6, 7, 8]: return 'Inverno'\n        return 'Primavera'\n    \n    season = get_season(month)\n    \n    # Criar DataFrame de entrada\n    input_df = pd.DataFrame([{\n        'energy_kwh': energy_kwh,\n        'state': state,\n        'usage_type': usage_type,\n        'energy_source': energy_source,\n        'month': month,\n        'season': season\n    }])\n    \n    # Realizar a predição\n    prediction = model.predict(input_df)[0]\n    return prediction\n\nprint(\"Função 'estimate_co2' pronta para uso.\")"),
    nbf.v4.new_markdown_cell("## 2. Exemplos de Uso\n\nVamos testar o modelo com alguns cenários hipotéticos."),
    nbf.v4.new_code_cell("# Cenário A: Indústria em SP usando fonte Térmica (Gasolina/Óleo) em Janeiro\nco2_a = estimate_co2(energy_kwh=1000, state='SP', usage_type='industrial', energy_source='thermal', month=1)\n\n# Cenário B: Residência na BA usando fonte Renovável (Solar/Eólica) em Agosto\nco2_b = estimate_co2(energy_kwh=1000, state='BA', usage_type='residencial', energy_source='solar', month=8)\n\nprint(f\"Cenário A: {co2_a:.2f} kg CO2\")\nprint(f\"Cenário B: {co2_b:.2f} kg CO2\")\nprint(f\"Diferença: {co2_a - co2_b:.2f} kg CO2\")"),
    nbf.v4.new_markdown_cell("## 3. Conclusão\n\nO modelo está pronto para ser integrado a sistemas de monitoramento ESG, permitindo o cálculo automatizado de emissões baseando-se apenas em dados de consumo e contexto geográfico.")
]

nb.cells = cells

# Save the notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook {notebook_path} created successfully.")
