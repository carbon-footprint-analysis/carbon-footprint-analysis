"""
Smoke test: simula a execução do notebook para verificar
se generate_dataset(100) funciona e retorna as colunas corretas.
"""
import pandas as pd
import numpy as np

# ── Carga de dados ──────────────────────────────────────────────────────────
profiles         = pd.read_csv('data/processed/v2_consumption_profiles.csv')
energy_dist      = pd.read_csv('data/processed/v2_energy_source_distribution.csv')
emission_df      = pd.read_csv('data/processed/v2_energy_source_emission_factors.csv')
usage_distribution_by_state = pd.read_csv(
    'data/processed/v2_usage_distribution_by_state.csv', index_col=0
)
company_size_dist = pd.read_csv('data/processed/v2_company_size_distribution_by_usage.csv')
seasonality       = pd.read_csv('data/processed/v2_seasonality_state_class_month.csv')
state_dist        = pd.read_csv('data/processed/v2_state_distribution.csv')

states        = state_dist['UF'].values
state_weights = state_dist['Consumo'].values / state_dist['Consumo'].sum()

# ── Funções ─────────────────────────────────────────────────────────────────

def generate_consumption(profile_row):
    if profile_row['distribution_type'] == 'lognormal':
        mu, sigma = profile_row['param_1'], profile_row['param_2']
        value = np.random.lognormal(mu, sigma)
        return min(value, 10 * np.exp(mu))
    raise ValueError("Distribuição não suportada")

def sample_energy_source(dist_df):
    return dist_df.sample(1, weights=dist_df['probability']).iloc[0]['energy_source']

def calculate_emission(energy_kwh, energy_source, emission_df):
    row = emission_df.loc[emission_df['energy_source'] == energy_source]
    if row.empty:
        raise ValueError(f"Fonte não encontrada: {energy_source}")
    return energy_kwh * row['emission_factor'].values[0]

def sample_company_size(setor):
    subset = company_size_dist[company_size_dist['Classe'] == setor].copy()
    if subset.empty:
        return 'pequena'
    portes = subset['company_size'].values
    probs  = subset['probability'].values.astype(float)
    total  = probs.sum()
    if total <= 0:
        return 'pequena'
    return np.random.choice(portes, p=probs / total)

def apply_seasonality(consumo, estado, setor, mes):
    subset = seasonality[
        (seasonality['UF']     == estado) &
        (seasonality['Classe'] == setor)  &
        (seasonality['month']  == mes)
    ]
    if subset.empty:
        return consumo
    return consumo * subset['seasonal_factor'].values[0]

def generate_event(profiles):
    estado = np.random.choice(states, p=state_weights)
    mes    = np.random.randint(1, 13)

    probs_estado = usage_distribution_by_state.loc[estado].values.astype(float)
    probs_estado = probs_estado / probs_estado.sum()
    setores      = usage_distribution_by_state.columns.tolist()
    setor        = np.random.choice(setores, p=probs_estado)

    profiles_subset = profiles[profiles['usage_type'] == setor]
    if profiles_subset.empty:
        raise ValueError(f"Nenhum perfil para setor: {setor!r}")
    row = profiles_subset.sample(1).iloc[0]

    consumo = generate_consumption(row)
    consumo = apply_seasonality(consumo, estado, setor, mes)
    consumo = consumo * np.random.normal(1, 0.08)

    porte = sample_company_size(setor)
    fonte = sample_energy_source(energy_dist)
    co2   = calculate_emission(consumo, fonte, emission_df)
    co2   = co2 * np.random.normal(1, 0.06)
    co2   = co2 * np.random.normal(1, 0.03)

    data = (
        pd.Timestamp('2025-01-01')
        + pd.DateOffset(months=mes - 1)
        + pd.to_timedelta(np.random.randint(0, 28), unit='D')
    )

    return {
        'id_empresa':       f"C{np.random.randint(100000, 999999)}",
        'data':             data,
        'estado':           estado,
        'setor':            setor,
        'porte':            porte,
        'tipo_combustivel': row['fuel_type'],
        'consumo_kwh':      consumo,
        'fonte_energia':    fonte,
        'emissao_co2':      co2,
    }

def generate_dataset(n):
    return pd.DataFrame([generate_event(profiles) for _ in range(n)])

# ── Teste ────────────────────────────────────────────────────────────────────
print("Gerando 500 eventos...")
df = generate_dataset(500)

with open('tmp/smoke_test_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== COLUNAS GERADAS ===\n")
    f.write(str(df.dtypes) + "\n\n")

    f.write("=== df.head() ===\n")
    f.write(df.head().to_string() + "\n\n")

    f.write("=== Valores únicos por coluna categórica ===\n")
    for col in ['estado', 'setor', 'porte', 'tipo_combustivel', 'fonte_energia']:
        f.write(f"  {col}: {sorted(df[col].unique())}\n")

    f.write("\n=== Estatísticas numéricas ===\n")
    f.write(df[['consumo_kwh', 'emissao_co2']].describe().to_string() + "\n")

print("✓ Smoke test ok — veja tmp/smoke_test_result.txt")
