import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "models", "best_carbon_footprint_model.joblib"))


def predict_all_sources(model, energy_kwh, month, state, usage_type, season):
    sources = ['hidrelétrica', 'nuclear', 'solar', 'térmica', 'eólica']
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
    fuels = {
        "ethanol":  {"efficiency": 0.27, "emission_factor": 0.20},
        "gasoline": {"efficiency": 0.30, "emission_factor": 0.64},
        "diesel":   {"efficiency": 0.38, "emission_factor": 0.73}
    }
    results = {}
    for fuel, data in fuels.items():
        energy_input = energy_kwh / data["efficiency"]
        co2 = energy_input * data["emission_factor"]
        results[fuel] = round(co2, 2)

    return dict(sorted(results.items(), key=lambda x: x[1]))


def compare_energy_sources(energy_kwh, month, state, usage_type, season):
    electricity = predict_all_sources(model, energy_kwh, month, state, usage_type, season)
    fuels = liquid_fuel_emissions(energy_kwh)
    combined = {**electricity, **fuels}
    ranking = dict(sorted(combined.items(), key=lambda x: x[1]))
    base = ranking["hidrelétrica"]
    result = {}
    for source, value in ranking.items():
        percent = ((value - base) / base) * 100
        result[source] = {"co2": round(value, 2), "vs_hydro_%": round(percent, 2)}
    return result
