import argparse
import pandas as pd
import joblib
import os
import sys

def get_season(month):
    if month in [12, 1, 2]: return 'Verao'
    if month in [3, 4, 5]: return 'Outono'
    if month in [6, 7, 8]: return 'Inverno'
    return 'Primavera'

def main():
    parser = argparse.ArgumentParser(description='Calculadora de Pegada de Carbono (CO2) - Modelo de Regressão')
    
    parser.add_argument('--kwh', type=float, required=True, help='Consumo de energia em kWh')
    parser.add_argument('--state', type=str, required=True, help='Sigla do estado (ex: SP, BA, RJ)')
    parser.add_argument('--type', type=str, required=True, choices=['industrial', 'comercial', 'residencial'], help='Tipo de uso')
    parser.add_argument('--source', type=str, required=True, choices=['hydro', 'thermal', 'solar', 'wind', 'nuclear'], help='Fonte de energia')
    parser.add_argument('--month', type=int, required=True, help='Mês da medição (1-12)')

    args = parser.parse_args()

    # Path to model
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, '..', 'models', 'carbon_footprint_rf_v1.joblib')

    if not os.path.exists(model_path):
        print(f"ERRO: Arquivo do modelo não encontrado em {model_path}")
        sys.exit(1)

    # Load model
    model = joblib.load(model_path)

    # Prepare input
    season = get_season(args.month)
    input_data = pd.DataFrame([{
        'energy_kwh': args.kwh,
        'state': args.state.upper(),
        'usage_type': args.type,
        'energy_source': args.source,
        'month': args.month,
        'season': season
    }])

    # Predict
    prediction = model.predict(input_data)[0]

    # Formatted Output
    print("\n" + "="*50)
    print("      RESULTADO DA ESTIMATIVA DE EMISSÕES CO2")
    print("="*50)
    print(f" Consumo:      {args.kwh:.2f} kWh")
    print(f" Estado:       {args.state.upper()}")
    print(f" Tipo:         {args.type.capitalize()}")
    print(f" Fonte:        {args.source.capitalize()}")
    print(f" Mês/Estação:  {args.month} ({season})")
    print("-" * 50)
    print(f" PEGADA DE CARBONO: {prediction:.2f} kg CO2")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
