from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "best_carbon_footprint_model.joblib")

model = joblib.load(model_path)

app = FastAPI(
    title="Carbon Footprint API",
    description="API para comparar emissões de energia",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnergyInput(BaseModel):
    energy_kwh: float
    month: int
    state: str
    usage_type: str
    season: str


# fator médio de emissão da energia eólica
WIND_EMISSION_FACTOR = 0.012


def predict_all_sources(model, energy_kwh, month, state, usage_type, season):

    # removemos eólica do modelo
    sources = ['hidrelétrica', 'nuclear', 'solar', 'térmica']

    results = {}

    for source in sources:

        df = pd.DataFrame({
            "consumo_kwh": [energy_kwh],
            "estado": [state],
            "setor": [usage_type],
            "fonte_energia": [source],
            "mes": [month],
            "season": [season]
        })

        co2 = model.predict(df)[0]

        results[source] = round(float(co2), 2)

    return results


def liquid_fuel_emissions(energy_kwh):

    fuels = {
        "ethanol": {"efficiency": 0.27, "emission_factor": 0.20},
        "gasoline": {"efficiency": 0.30, "emission_factor": 0.64},
        "diesel": {"efficiency": 0.38, "emission_factor": 0.73}
    }

    results = {}

    for fuel, data in fuels.items():

        energy_input = energy_kwh / data["efficiency"]
        co2 = energy_input * data["emission_factor"]

        results[fuel] = round(co2, 2)

    return results


def wind_emission(energy_kwh):

    # cálculo manual da eólica
    co2 = energy_kwh * WIND_EMISSION_FACTOR

    return {"eólica": round(co2, 2)}


def compare_energy_sources(energy_kwh, month, state, usage_type, season):

    electricity = predict_all_sources(
        model,
        energy_kwh,
        month,
        state,
        usage_type,
        season
    )

    wind = wind_emission(energy_kwh)

    fuels = liquid_fuel_emissions(energy_kwh)

    combined = {**electricity, **wind, **fuels}

    ranking = dict(sorted(combined.items(), key=lambda x: x[1]))

    return ranking


@app.post("/compare")
def compare(data: EnergyInput):

    result = compare_energy_sources(
        data.energy_kwh,
        data.month,
        data.state,
        data.usage_type,
        data.season
    )

    return result