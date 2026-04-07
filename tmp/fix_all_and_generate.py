"""
fix_all_and_generate.py
-----------------------
1. Normaliza o CSV de sazonalidade (Classe: Português -> Inglês)
2. Roda a geração do dataset sintético final com todas as correções
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA  = ROOT / 'data' / 'processed'

# ===========================================================
# PARTE 1 – Normalizar o CSV de sazonalidade
# ===========================================================
print("=== Normalizando seasonality CSV ===")

category_map = {
    'comercial':  'commercial',
    'industrial': 'industrial',
    'outros':     'other',
    'residencial':'residential',
    'rural':      'agriculture',
}

seasonality = pd.read_csv(DATA / 'v2_seasonality_state_class_month.csv')
print("Antes:", seasonality['Classe'].unique())

seasonality['Classe'] = (
    seasonality['Classe']
    .astype(str)
    .str.strip()
    .str.lower()
    .replace(category_map)
)

print("Depois:", seasonality['Classe'].unique())
seasonality.to_csv(DATA / 'v2_seasonality_state_class_month.csv', index=False)
print("✔ Salvo: v2_seasonality_state_class_month.csv\n")


# ===========================================================
# PARTE 2 – Carregar todos os arquivos de configuração
# ===========================================================
print("=== Carregando configurações ===")

profiles = pd.read_csv(DATA / 'v2_consumption_profiles.csv')
energy_dist = pd.read_csv(DATA / 'v2_energy_source_distribution.csv')
emission_df = pd.read_csv(DATA / 'v2_energy_source_emission_factors.csv')
usage_distribution_by_state = pd.read_csv(
    DATA / 'v2_usage_distribution_by_state.csv',
    index_col=0
)
company_size_dist = pd.read_csv(DATA / 'v2_company_size_distribution_by_usage.csv')
seasonality = pd.read_csv(DATA / 'v2_seasonality_state_class_month.csv')
state_dist = pd.read_csv(DATA / 'v2_state_distribution.csv')

# Normalizar categorias
def normalize_classe(df, col):
    df[col] = df[col].astype(str).str.strip().str.lower().replace(category_map)

normalize_classe(profiles, 'usage_type')
normalize_classe(company_size_dist, 'Classe')
normalize_classe(seasonality, 'Classe')
usage_distribution_by_state.columns = [
    category_map.get(c.lower(), c.lower())
    for c in usage_distribution_by_state.columns
]

states = state_dist['UF'].values
state_weights = state_dist['Consumo'].values
state_weights = state_weights / state_weights.sum()

print("profiles usage_type:  ", profiles['usage_type'].unique())
print("company_size Classe:  ", company_size_dist['Classe'].unique())
print("seasonality Classe:   ", seasonality['Classe'].unique())
print("usage_dist columns:   ", usage_distribution_by_state.columns.tolist())
print("energy_dist probabilidade total:", round(energy_dist['probability'].sum(), 4))
print()

# ===========================================================
# PARTE 3 – Funções de geração
# ===========================================================

def generate_consumption(profile_row):
    if profile_row['distribution_type'] == 'lognormal':
        mu    = profile_row['param_1']
        sigma = profile_row['param_2']
        value = np.random.lognormal(mu, sigma)
        max_v = 10 * np.exp(mu)
        return min(value, max_v)
    raise ValueError("Distribuição não suportada")


def sample_energy_source(dist_df):
    return dist_df.sample(1, weights=dist_df['probability']).iloc[0]['energy_source']


def calculate_emission(energy_kwh, energy_source, emission_df):
    row = emission_df.loc[emission_df['energy_source'] == energy_source]
    factor = row['emission_factor'].values[0]
    return energy_kwh * factor


def sample_company_size(usage_type):
    subset = company_size_dist[company_size_dist['Classe'] == usage_type]
    if subset.empty:
        return 'small'
    if len(subset) == 1:
        return subset['company_size'].iloc[0]
    probs = subset['probability'].values
    probs = probs / probs.sum()
    return np.random.choice(subset['company_size'].values, p=probs)


def apply_seasonality(consumption, state, usage_class, month):
    # usage_class já está em inglês (ex: 'industrial', 'residential')
    subset = seasonality[
        (seasonality['UF']     == state) &
        (seasonality['Classe'] == usage_class) &
        (seasonality['month']  == month)
    ]
    if subset.empty:
        return consumption
    factor = subset['seasonal_factor'].values[0]
    return consumption * factor


def generate_event(profiles):
    # 1) Estado
    state = np.random.choice(states, p=state_weights)

    # 2) Mês
    month = np.random.randint(1, 13)

    # 3) Setor econômico condicionado ao estado
    usage_probs_state = usage_distribution_by_state.loc[state].values.astype(float)
    usage_probs_state = usage_probs_state / usage_probs_state.sum()
    usage_types = usage_distribution_by_state.columns.tolist()
    usage_type = np.random.choice(usage_types, p=usage_probs_state)

    # 4) Perfil do setor
    profiles_subset = profiles[profiles['usage_type'] == usage_type]
    if profiles_subset.empty:
        raise ValueError(f"Nenhum profile encontrado para {usage_type}")
    row = profiles_subset.sample(1).iloc[0]

    # 5) Consumo base
    consumption = generate_consumption(row)

    # 6) Sazonalidade
    consumption = apply_seasonality(consumption, state, usage_type, month)

    # 7) Ruído operacional (~8%)
    consumption = consumption * np.random.normal(1, 0.08)

    # 8) Tamanho da empresa
    company_size = sample_company_size(usage_type)

    # 9) Fonte energética
    energy_source = sample_energy_source(energy_dist)

    # 10) Emissão + variação do fator (~6%)
    co2 = calculate_emission(consumption, energy_source, emission_df)
    co2 = co2 * np.random.normal(1, 0.06)

    # 11) Ruído de medição (~3%)
    co2 = co2 * np.random.normal(1, 0.03)

    # 12) Data dentro do mês
    date = (
        pd.Timestamp('2025-01-01')
        + pd.DateOffset(months=month - 1)
        + pd.to_timedelta(np.random.randint(0, 28), unit='D')
    )

    return {
        'company_id':   f"C{np.random.randint(100000, 999999)}",
        'date':         date,
        'state':        state,
        'usage_type':   usage_type,
        'company_size': company_size,
        'fuel_type':    row['fuel_type'],
        'energy_kwh':   consumption,
        'energy_source': energy_source,
        'co2_emission': co2,
    }


def generate_dataset(n):
    data = []
    for i in range(n):
        if i % 10000 == 0:
            print(f"  Gerando evento {i}/{n}...")
        data.append(generate_event(profiles))
    return pd.DataFrame(data)


# ===========================================================
# PARTE 4 – Gerar e salvar o dataset
# ===========================================================
print("=== Gerando dataset sintético (100.000 registros) ===")
np.random.seed(42)
df = generate_dataset(100_000)

print("\nDescrição do dataset:")
print(df.describe())
print("\nDistribuição por usage_type:")
print(df['usage_type'].value_counts())
print("\nDistribuição por company_size:")
print(df['company_size'].value_counts())

output_path = DATA / 'synthetic_energy_emissions_dataset.csv'
df.to_csv(output_path, index=False)
print(f"\n✔ Dataset salvo em: {output_path}")
print(f"  Shape: {df.shape}")
