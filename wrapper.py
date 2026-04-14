import joblib
import pandas as pd
import os

# Se o arquivo está na RAIZ, precisamos de apenas UM dirname para chegar à pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_carbon_footprint_model.joblib")

# Carregamento seguro do modelo
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print(f"⚠️ Aviso: Modelo não encontrado em {MODEL_PATH}")

def predict_all_sources(model, energy_kwh, month, state, usage_type, season):
    if model is None: return {}
    
    sources = ['Hidrelétrica', 'Nuclear', 'Solar', 'Térmica', 'Eólica']
    results = {}

    for source in sources:
        df = pd.DataFrame({
            "consumo_kwh": [energy_kwh],
            "mes": [month],
            "estado": [state],
            "setor": [usage_type],
            "fonte_energia": [source],
            "season": [season]
        })
        co2 = model.predict(df)[0]
        results[source] = round(float(co2), 2)

    return dict(sorted(results.items(), key=lambda x: x[1]))

def liquid_fuel_emissions(energy_kwh):
    # Cálculo baseado na eficiência energética (kWh equivalentes)
    fuels = {
        "Etanol":  {"efficiency": 0.27, "emission_factor": 0.20},
        "Gasolina": {"efficiency": 0.30, "emission_factor": 0.64},
        "Diesel":   {"efficiency": 0.38, "emission_factor": 0.73}
    }
    results = {}
    for fuel, data in fuels.items():
        energy_input = energy_kwh / data["efficiency"]
        co2 = energy_input * data["emission_factor"]
        results[fuel] = round(co2, 2)

    return dict(sorted(results.items(), key=lambda x: x[1]))

def compare_energy_sources(energy_kwh, month, state, usage_type, season):
    # Compara todas as fontes e calcula a variação percentual vs Hidrelétrica
    electricity = predict_all_sources(model, energy_kwh, month, state, usage_type, season)
    fuels = liquid_fuel_emissions(energy_kwh)
    combined = {**electricity, **fuels}
    
    ranking = dict(sorted(combined.items(), key=lambda x: x[1]))
    
    # Referência (Base): Hidrelétrica (geralmente a menor emissão na rede brasileira)
    base_val = electricity.get("Hidrelétrica", 1.0) 
    
    result = {}
    for source, value in ranking.items():
        # Cálculo da variação percentual: 
        # $$\Delta\% = \frac{V_{atual} - V_{base}}{V_{base}} \times 100$$
        percent = ((value - base_val) / base_val) * 100
        result[source] = {"co2": round(value, 2), "vs_hydro_pct": round(percent, 2)}
        
    return result