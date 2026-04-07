# ==> CELL 2
# Mapping Portuguese categories to standardized English labels
category_map = {
    'comercial': 'commercial',
    'industrial': 'industrial',
    'outros': 'other',
    'residencial': 'residential',
    'rural': 'agriculture',
    'Comercial': 'commercial',
    'Industrial': 'industrial',
    'Outros': 'other',
    'Residencial': 'residential',
    'Rural': 'agriculture'
}

# # !git clone https://github.com/carbon-footprint-analysis/carbon-footprint-analysis.git

# ==> CELL 4
import pandas as pd

epe = pd.read_csv('../data/raw/epe_industrial_consumption_by_state.csv',
                    encoding='latin-1',
                    sep=';',
                    decimal=',')

# ==> CELL 5
epe.head()

# ==> CELL 6
epe['DataExcel'] = pd.to_datetime(epe['DataExcel'], dayfirst=True)

# ==> CELL 7
epe.info()

# ==> CELL 8
epe['SetorIndustrial'].unique()

# ==> CELL 9
df = epe.copy()

# ==> CELL 10
df['year'] = df['DataExcel'].dt.year
df['month'] = df['DataExcel'].dt.month

# ==> CELL 11
df_2025 = df[df['year'] == 2025].copy()
df_2025.drop(columns=['DataVersao', 'DataExcel'], inplace=True)

# ==> CELL 12
df_2025.head(5)

# ==> CELL 13
df_grouped = df.groupby('SetorIndustrial')['Consumo'].mean().reset_index()

# ==> CELL 14
df_grouped = df_grouped.rename(columns={'Consumo':'Consumo_MWh'})

# ==> CELL 15
df_grouped.head()

# ==> CELL 16
df_grouped['Consumo_kWh'] = (df_grouped['Consumo_MWh']) * 1000

# ==> CELL 17
df_grouped.head()

# ==> CELL 18
df_grouped.to_csv('../data/processed/media_consumo_indutria_2025.csv')

# ==> CELL 20
import pandas as pd

epe_categoria = pd.read_csv('../data/raw/EPE - Dados_abertos_Consumo_Mensal.CSV',
                    encoding='latin-1',
                    sep=';',
                    decimal=',')

# ==> CELL 21
df_2025 = df[df['year'] == 2025].copy()
df_2025.drop(columns=['DataVersao', 'DataExcel'], inplace=True)

# ==> CELL 22
epe_categoria.info()

# ==> CELL 23
epe_categoria['DataExcel'] = pd.to_datetime(epe_categoria['DataExcel'], dayfirst=True)

# ==> CELL 24
df = epe_categoria.copy()

# ==> CELL 25
df['year'] = df['DataExcel'].dt.year
df['month'] = df['DataExcel'].dt.month

# ==> CELL 26
df_2025 = df[df['year'] == 2025]

# ==> CELL 27
df_2025['Consumo'] = (
    df_2025['Consumo']
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df_2025['Consumidores'] = (
    df_2025['Consumidores']
    .astype(str)
    .str.replace('.', '', regex=False)
    .astype(float)
)

# ==> CELL 28
df_2025.info()

# ==> CELL 29
df_2025.head()

# ==> CELL 30
df_2025.drop(columns=['Data', 'DataVersao'], inplace=True)

# ==> CELL 31
df_2025 = df_2025.rename(columns={'Consumo':'Consumo_MWh'})

# ==> CELL 32
df_simplificado = (
    df_2025
    .groupby('Classe')
    .agg({
        'Consumo_MWh': 'sum',
        'Consumidores': 'sum'
    })
)

df_simplificado['consumo_medio_MWh'] = df_simplificado['Consumo_MWh'] / df_simplificado['Consumidores']

df_simplificado = df_simplificado.sort_values('Consumo_MWh', ascending=False)

# ==> CELL 33
df_simplificado['Consumo_kWh'] = (df_simplificado['Consumo_MWh']) * 1000
df_simplificado['consumo_medio_KWh'] = (df_simplificado['consumo_medio_MWh']) * 1000

# ==> CELL 34
df_simplificado = df_simplificado[[
    'Consumidores',
    'Consumo_MWh',
    'Consumo_kWh',
    'consumo_medio_MWh',
    'consumo_medio_KWh'
]]

# ==> CELL 35
df_simplificado

# ==> CELL 36
df_simplificado.to_csv('../data/processed/consumo_medio_categoria_2025.csv')

# ==> CELL 38
df_grouped.head()

# ==> CELL 39
df_grouped.info()

# ==> CELL 40
df_simplificado.head()

# ==> CELL 41
df_simplificado.info()

# ==> CELL 43
df_profiles = df_simplificado.copy()

# ==> CELL 44
df_profiles.head()

# ==> CELL 45
def get_sigma(classe):
    if classe in ['Industrial', 'industrial']:
        return 0.6
    elif classe in ['Comercial', 'commercial']:
        return 0.4
    elif classe in ['Residencial', 'residential']:
        return 0.3
    else:
        return 0.35

df_profiles['sigma'] = df_profiles.index.map(get_sigma)

# ==> CELL 46
map_usage = {
    'Industrial': 'industrial',
    'Comercial': 'commercial',
    'Residencial': 'residential',
    'Rural': 'agriculture',
    'Outros': 'other'
}

df_profiles['usage_type'] = df_profiles.index.map(map_usage)

# ==> CELL 47
import numpy as np

df_profiles['mu'] = np.log(df_profiles['consumo_medio_KWh'])

# ==> CELL 48
df_final = df_profiles.copy()
df_final['fuel_type'] = 'electric'
df_final['distribution_type'] = 'lognormal'
df_final['param_1'] = df_profiles['mu']
df_final['param_2'] = df_profiles['sigma']
df_final['param_1_name'] = 'mu'
df_final['param_2_name'] = 'sigma'
df_final['unit'] = 'kWh'
df_final['is_energy_based'] = True

# ==> CELL 49
df_final.head()

# ==> CELL 50
df_export = df_final[[
    'usage_type',
    'fuel_type',
    'distribution_type',
    'param_1',
    'param_2',
    'param_1_name',
    'param_2_name',
    'unit',
    'is_energy_based'
]].copy()

# ==> CELL 51
df_export.head()

# ==> CELL 52
df_export.to_csv('../data/processed/v2_consumption_profiles.csv', index=False)

# ==> CELL 55
import pandas as pd
import numpy as np

profiles = pd.read_csv('../data/processed/v2_consumption_profiles.csv')

# ==> CELL 57
def generate_consumption(profile_row):

    if profile_row['distribution_type'] == 'lognormal':
        mu = profile_row['param_1']
        sigma = profile_row['param_2']

        value = np.random.lognormal(mu, sigma)

        # LIMITADOR
        max_value = 10 * np.exp(mu)
        value = min(value, max_value)

        return value

    else:
        raise ValueError("Distribuição não suportada")

# ==> CELL 59
usage_probs = {
    'residential': 0.6,
    'commercial': 0.2,
    'industrial': 0.1,
    'agriculture': 0.05,
    'other': 0.05
}

# ==> CELL 60
def generate_event(profiles):

    weights = profiles['usage_type'].map(usage_probs)

    row = profiles.sample(1, weights=weights).iloc[0]

    consumption = generate_consumption(row)

    return {
        'usage_type': row['usage_type'],
        'fuel_type': row['fuel_type'],
        'energy_kwh': consumption
    }

# ==> CELL 62
def generate_dataset(n, profiles):
    data = []

    for _ in range(n):
        event = generate_event(profiles)
        data.append(event)

    return pd.DataFrame(data)

# ==> CELL 64
df = generate_dataset(10000, profiles)

# ==> CELL 65
df.head()

# ==> CELL 66
df.to_csv('df_gerado_teste.csv')

# ==> CELL 67
df['usage_type'].value_counts(normalize=True)

# ==> CELL 68
df.groupby('usage_type')['energy_kwh'].describe()

# ==> CELL 69
df['energy_kwh'].max()

# ==> CELL 70
(df['energy_kwh'] < 0).sum()

# ==> CELL 71
import matplotlib.pyplot as plt

df[df['usage_type']=='industrial']['energy_kwh'].hist(bins=50)
plt.title('Industrial')
plt.show()

# ==> CELL 73
df_aneel = pd.read_csv('../data/raw/aneel_generation.csv',
                       encoding='latin-1',
                       sep=';',
                       decimal=',')

# ==> CELL 74
df_aneel.info()

# ==> CELL 75
df_aneel.head()

# ==> CELL 76
df_aneel['AnoReferencia'].unique()

# ==> CELL 77
df_aneel = df_aneel[df_aneel['AnoReferencia']==2025]

# ==> CELL 78
df_aneel['SigTipoGeracao'].unique()

# ==> CELL 79
df_grouped = df_aneel.groupby('SigTipoGeracao')['MdaPotenciaInstaladaKW'].sum()

# ==> CELL 80
df_grouped.head()

# ==> CELL 82
df_dist = df_grouped / df_grouped.sum()

# ==> CELL 84
df_dist.info()

# ==> CELL 85
df_grouped = df_aneel.groupby('SigTipoGeracao')['MdaPotenciaInstaladaKW'].sum().reset_index()

df_grouped.columns = ['energy_source', 'total_generation']

# ==> CELL 86
df_grouped['probability'] = df_grouped['total_generation'] / df_grouped['total_generation'].sum()

df_dist = df_grouped[['energy_source', 'probability']]
df_dist = df_dist.copy()

# ==> CELL 87
df_dist.head()

# ==> CELL 88
df_dist['probability'].sum()

# ==> CELL 89
map_sources = {
    'UHE': 'hydro',      # Hidrelétrica grande
    'PCH': 'hydro',      # Pequena central hidrelétrica
    'CGH': 'hydro',      # Central geradora hidráulica

    'EOL': 'wind',       # Eólica

    'UFV': 'solar',      # Solar fotovoltaica

    # se aparecer depois:
    'UTE': 'thermal',    # termoelétrica (genérico)
    'UTN': 'nuclear',    # nuclear
}
df_dist['energy_source'] = df_dist['energy_source'].map(map_sources)

# ==> CELL 90
df_dist = df_dist.groupby('energy_source')['probability'].sum().reset_index()

# ==> CELL 91
df_dist['probability'] = df_dist['probability'] / df_dist['probability'].sum()

# ==> CELL 92
df_dist = df_dist.sort_values('probability', ascending=False)

# ==> CELL 93
df_dist

# ==> CELL 94
df_dist.to_csv('../data/processed/v2_energy_source_distribution.csv')

# ==> CELL 96
emission_factors = pd.read_csv('../data/processed/v2_energy_source_emission_factors.csv')

# ==> CELL 97
def calculate_emission(energy_kwh, energy_source, emission_df):

    row = emission_df.loc[
        emission_df['energy_source'] == energy_source
    ]

    if row.empty:
        raise ValueError(f"Fonte não encontrada: {energy_source}")

    factor = row['emission_factor'].values[0]

    return energy_kwh * factor

# ==> CELL 98
def sample_energy_source(dist_df):
    return dist_df.sample(1, weights=dist_df['probability']).iloc[0]['energy_source']

# ==> CELL 99
def normalize_usage_types(series):

    mapping = {
        'residencial': 'residential',
        'rural': 'agriculture',
        'outros': 'other',
        'industrial': 'industrial',
        'commercial': 'commercial'
    }

    return (
        series
        .str.strip()
        .str.lower()
        .replace(mapping)
    )

# ==> CELL 100
def generate_event(profiles, energy_dist, emission_df):

    usage_types = normalize_usage_types(profiles['usage_type'])

    weights = usage_types.map(usage_probs)

    if weights.sum() == 0:
        raise ValueError("usage_probs não corresponde aos usage_type do profile")

    row = profiles.sample(1, weights=weights).iloc[0]

    consumption = generate_consumption(row)

    energy_source = sample_energy_source(energy_dist)

    co2 = calculate_emission(consumption, energy_source, emission_df)

    return {
        'usage_type': row['usage_type'],
        'fuel_type': row['fuel_type'],
        'energy_kwh': consumption,
        'energy_source': energy_source,
        'co2_emission': co2
    }

# ==> CELL 101
import pandas as pd
profiles = pd.read_csv('../data/processed/v2_consumption_profiles.csv')

energy_dist = pd.read_csv('../data/processed/v2_energy_source_distribution.csv')

emission_df = pd.read_csv('../data/processed/v2_energy_source_emission_factors.csv')

# ==> CELL 102
event = generate_event(profiles, energy_dist, emission_df)
event

# ==> CELL 103
def generate_dataset(n, profiles, energy_dist, emission_df):
    data = []

    for _ in range(n):
        event = generate_event(profiles, energy_dist, emission_df)
        data.append(event)

    return pd.DataFrame(data)

# ==> CELL 104
df = generate_dataset(10000, profiles, energy_dist, emission_df)
df.describe()

# ==> CELL 105
df.head()

# ==> CELL 107
company_id = f"C{np.random.randint(1000,9999)}"

# ==> CELL 108
date = pd.Timestamp('2025-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')

# ==> CELL 109
states = [
'SP','MG','RJ','BA','PR','RS','SC','GO','PE','CE',
'PA','MT','ES','DF','MS','MA','RN','PB','AL','PI',
'RO','SE','TO','AC','AP','RR','AM'
]

state_weights = [
0.22,0.10,0.09,0.07,0.06,0.06,0.04,0.04,0.04,0.04,
0.03,0.03,0.02,0.02,0.02,0.02,0.015,0.015,0.01,0.01,
0.008,0.008,0.006,0.005,0.005,0.003,0.02
]


# ==> CELL 110
len(states), len(state_weights)

# ==> CELL 111
state_weights = np.array(state_weights)
state_weights = state_weights / state_weights.sum()
state_weights

# ==> CELL 112
def generate_event(profiles, energy_dist, emission_df):

    usage_types = normalize_usage_types(profiles['usage_type'])

    weights = usage_types.map(usage_probs)

    if weights.sum() == 0:
        raise ValueError("usage_probs não corresponde aos usage_type do profile")

    row = profiles.sample(1, weights=weights).iloc[0]

    consumption = generate_consumption(row)

    energy_source = sample_energy_source(energy_dist)

    co2 = calculate_emission(consumption, energy_source, emission_df)

    return {
        'company_id': f"C{np.random.randint(100000,999999)}",
        'date': pd.Timestamp('2025-01-01') + pd.to_timedelta(np.random.randint(0,365), unit='D'),
        'state': np.random.choice(states, p=state_weights),
        'usage_type': row['usage_type'],
        'fuel_type': row['fuel_type'],
        'energy_kwh': consumption,
        'energy_source': energy_source,
        'co2_emission': co2
    }

# ==> CELL 113
def generate_dataset(n, profiles, energy_dist, emission_df):
    data = []

    for _ in range(n):
        event = generate_event(profiles, energy_dist, emission_df)
        data.append(event)

    return pd.DataFrame(data)

# ==> CELL 114
df = generate_dataset(10000, profiles, energy_dist, emission_df)
df.describe()

# ==> CELL 115
df

# ==> CELL 117
df_epe = pd.read_csv('../data/raw/EPE - Dados_abertos_Consumo_Mensal.CSV',
                    encoding='latin-1',
                    sep=';',
                    decimal=',')

# ==> CELL 118
df_epe.columns

# ==> CELL 119
df_epe.head(5)

# ==> CELL 120
df_epe.info()

# ==> CELL 121
df_epe['Consumo'] = (
    df_epe['Consumo']
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# ==> CELL 122
df_sector_state = (
    df_epe
    .groupby(['UF','Classe'])['Consumo']
    .sum()
    .reset_index()
)

# ==> CELL 123
df_sector_state.head(20)

# ==> CELL 124
df_sector_state['probability'] = (
    df_sector_state
    .groupby('UF')['Consumo']
    .transform(lambda x: x / x.sum())
)

# ==> CELL 125
usage_distribution_by_state = df_sector_state.pivot(
    index='UF',
    columns='Classe',
    values='probability'
)
usage_distribution_by_state.columns = [category_map.get(c, c.lower()) for c in usage_distribution_by_state.columns]

# ==> CELL 126
usage_distribution_by_state.to_csv('../data/processed/v2_usage_distribution_by_state.csv')

# ==> CELL 128
df_epe

# ==> CELL 129
state_consumption = df_epe.groupby("UF")["Consumo"].sum()

state_distribution = state_consumption / state_consumption.sum()


# ==> CELL 130
state_distribution

# ==> CELL 131
state_distribution.to_csv("../data/processed/v2_state_distribution.csv")

# ==> CELL 132
df_state = pd.read_csv("../data/processed/v2_state_distribution.csv")

states = df_state["UF"]
state_weights = df_state["Consumo"]


# ==> CELL 133
def generate_event(profiles, energy_dist, emission_df):

    # sorteia estado
    state = np.random.choice(states, p=state_weights)

    # pega probabilidades de setor para esse estado
    usage_probs_state = usage_distribution_by_state.loc[state].values
    usage_probs_state = usage_probs_state / usage_probs_state.sum()

    # sorteia setor
    usage_types = profiles['usage_type'].unique()

    usage_type = np.random.choice(
        usage_types,
        p=usage_probs_state
    )

    # filtra profiles para esse setor
    profiles_subset = profiles[profiles['usage_type'] == usage_type]

    # escolhe linha de profile
    row = profiles_subset.sample(1).iloc[0]

    # gera consumo
    consumption = generate_consumption(row)

    # sorteia fonte de energia
    energy_source = sample_energy_source(energy_dist)

    # calcula CO2
    co2 = calculate_emission(consumption, energy_source, emission_df)

    return {
        'company_id': f"C{np.random.randint(100000,999999)}",
        'date': pd.Timestamp('2025-01-01') + pd.to_timedelta(np.random.randint(0,365), unit='D'),
        'state': np.random.choice(states, p=state_weights),
        'usage_type': usage_type,
        'fuel_type': row['fuel_type'],
        'energy_kwh': consumption,
        'energy_source': energy_source,
        'co2_emission': co2
    }

# ==> CELL 134
def generate_dataset(n, profiles, energy_dist, emission_df):
    data = []

    for _ in range(n):
        event = generate_event(profiles, energy_dist, emission_df)
        data.append(event)

    return pd.DataFrame(data)

# ==> CELL 135
df = generate_dataset(10000, profiles, energy_dist, emission_df)
df.describe()

# ==> CELL 136
df

# ==> CELL 137
df = generate_dataset(10000, profiles, energy_dist, emission_df)

# ==> CELL 138
df.info()

# ==> CELL 140
df_epe = pd.read_csv('../data/raw/EPE - Dados_abertos_Consumo_Mensal.CSV',
                    encoding='latin-1',
                    sep=';',
                    decimal=',')

# ==> CELL 141
df_epe['Consumo'] = (
    df_epe['Consumo']
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# ==> CELL 142
df_epe['DataExcel'] = pd.to_datetime(df_epe['DataExcel'], dayfirst=True)

# ==> CELL 143
df_epe['year'] = df_epe['DataExcel'].dt.year
df_epe['month'] = df_epe['DataExcel'].dt.month

# ==> CELL 144
df_2025 = df_epe[df_epe['year'] == 2025].copy()

# ==> CELL 145
df_2025

# ==> CELL 146
df_2025['DataExcel'].unique()

# ==> CELL 147
df_2025['year'].unique()

# ==> CELL 148
df_epe = df_2025.copy()

# ==> CELL 149
def classify_company_size(row):

    usage = row['Classe']
    energy = row['Consumo']

    if usage == 'Industrial':
        if energy < 20000:
            return 'small'
        elif energy < 100000:
            return 'medium'
        else:
            return 'large'

    if usage == 'Comercial':
        if energy < 5000:
            return 'small'
        elif energy < 30000:
            return 'medium'
        else:
            return 'large'

    if usage == 'Residencial':
        return 'small'

    if usage == 'Rural':
        if energy < 10000:
            return 'small'
        elif energy < 50000:
            return 'medium'
        else:
            return 'large'

    if usage == 'Outros':
        if energy < 10000:
            return 'small'
        elif energy < 50000:
            return 'medium'
        else:
            return 'large'

# ==> CELL 150
df_epe['company_size'] = df_epe.apply(classify_company_size, axis=1)

# ==> CELL 151
df_epe['company_size'].value_counts()

# ==> CELL 152
size_dist = (
    df_epe
    .groupby('Classe')['company_size']
    .value_counts(normalize=True)
    .reset_index(name='probability')
)

# ==> CELL 153
size_dist

# ==> CELL 154
size_dist.to_csv(
    '../data/processed/v2_company_size_distribution_by_usage.csv',
    index=False
)

# ==> CELL 156
df_epe = pd.read_csv('../data/raw/EPE - Dados_abertos_Consumo_Mensal.CSV',
                    encoding='latin-1',
                    sep=';',
                    decimal=',')

# ==> CELL 157
df_epe['Consumo'] = (
    df_epe['Consumo']
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# ==> CELL 158
df_epe['DataExcel'] = pd.to_datetime(df_epe['DataExcel'], dayfirst=True)

# ==> CELL 159
df_epe['year'] = df_epe['DataExcel'].dt.year
df_epe['month'] = df_epe['DataExcel'].dt.month

# ==> CELL 160
df_2025 = df_epe[df_epe['year'] == 2025].copy()

# ==> CELL 161
df_2025

# ==> CELL 162
df_epe = df_2025.copy()

# ==> CELL 163
df_epe['month'] = df_epe['DataExcel'].dt.month

# ==> CELL 164
monthly_stats = (
    df_epe
    .groupby(['UF','Classe','month'])['Consumo']
    .agg(['mean','var'])
    .reset_index()
)

# ==> CELL 165
annual_mean = (
    df_epe
    .groupby(['UF','Classe'])['Consumo']
    .mean()
    .reset_index()
    .rename(columns={'Consumo':'annual_mean'})
)

# ==> CELL 166
monthly_stats = monthly_stats.merge(
    annual_mean,
    on=['UF','Classe']
)

# ==> CELL 167
monthly_stats['seasonal_factor'] = (
    monthly_stats['mean'] /
    monthly_stats['annual_mean']
)

# ==> CELL 168
monthly_stats

# ==> CELL 169
monthly_stats = monthly_stats[[
    'UF',
    'Classe',
    'month',
    'seasonal_factor',
    'var'
]]

monthly_stats.to_csv(
    '../data/processed/v2_seasonality_state_class_month.csv',
    index=False
)

# ==> CELL 171
# !ls

# ==> CELL 172
from pathlib import Path

ROOT = Path().resolve().parent

# ==> CELL 173
# !pwd

# ==> CELL 174
# !git pull

# ==> CELL 176
import pandas as pd
import numpy as np

profiles = pd.read_csv('../data/processed/v2_consumption_profiles.csv')

energy_dist = pd.read_csv('../data/processed/v2_energy_source_distribution.csv')

emission_df = pd.read_csv('../data/processed/v2_energy_source_emission_factors.csv')

usage_distribution_by_state = pd.read_csv(
    '../data/processed/v2_usage_distribution_by_state.csv',
    index_col=0
)

company_size_dist = pd.read_csv(
    '../data/processed/v2_company_size_distribution_by_usage.csv'
)

seasonality = pd.read_csv(
    '../data/processed/v2_seasonality_state_class_month.csv'
)

# ==> CELL 178
category_map = {
    'comercial': 'commercial',
    'industrial': 'industrial',
    'outros': 'other',
    'residencial': 'residential',
    'rural': 'agriculture'
}

def normalize_classe(df, col):
    df[col] = df[col].astype(str).str.lower().replace(category_map)

normalize_classe(profiles, 'usage_type')
normalize_classe(company_size_dist, 'Classe')
normalize_classe(seasonality, 'Classe')

usage_distribution_by_state.columns = [category_map.get(c.lower(), c.lower()) for c in usage_distribution_by_state.columns]

# ==> CELL 179
print('profiles: '+profiles.columns,'\n')
print('energy_dist: '+energy_dist.columns,'\n')
print('emission_df: '+emission_df.columns,'\n')
print('usage_distribution_by_state: '+usage_distribution_by_state.columns,'\n')
print('company_size_dist: '+company_size_dist.columns,'\n')
print('seasonality: '+seasonality.columns,'\n')

# ==> CELL 180
def show_uniques(df, name):
    print(f"\n{name}")
    for col in df.select_dtypes(include='object').columns:
        print(col, "->", df[col].unique())

# ==> CELL 181
show_uniques(profiles, "profiles")
show_uniques(company_size_dist, "company_size_dist")
show_uniques(usage_distribution_by_state, "usage_distribution")
show_uniques(seasonality, "seasonality")

# ==> CELL 182
print(set(profiles['usage_type']))
print(set(company_size_dist['Classe']))
print(set(usage_distribution_by_state.columns))
print(set(seasonality['Classe']))

# ==> CELL 183
print("usage_types possíveis:", usage_distribution_by_state.columns.tolist())
print("classes em company_size:", company_size_dist['Classe'].unique())

# ==> CELL 184
for u in usage_distribution_by_state.columns:
    subset = company_size_dist[company_size_dist['Classe'] == u]
    print(u, "->", len(subset))

# ==> CELL 185
print(energy_dist['probability'].sum())

# ==> CELL 186
print(company_size_dist.groupby('Classe')['probability'].sum())

# ==> CELL 188
def generate_consumption(profile_row):

    if profile_row['distribution_type'] == 'lognormal':

        mu = profile_row['param_1']
        sigma = profile_row['param_2']

        value = np.random.lognormal(mu, sigma)

        max_value = 10 * np.exp(mu)
        value = min(value, max_value)

        return value

    else:
        raise ValueError("Distribuição não suportada")

# ==> CELL 190
def sample_energy_source(dist_df):

    return dist_df.sample(
        1,
        weights=dist_df['probability']
    ).iloc[0]['energy_source']

# ==> CELL 192
def calculate_emission(energy_kwh, energy_source, emission_df):

    row = emission_df.loc[
        emission_df['energy_source'] == energy_source
    ]

    factor = row['emission_factor'].values[0]

    return energy_kwh * factor

# ==> CELL 194
def sample_company_size(usage_type):

    subset = company_size_dist[company_size_dist['Classe'] == usage_type]

    if subset.empty:
        return 'small'

    if len(subset) == 1:
        return subset['company_size'].iloc[0]

    # Renormalize probabilities
    probs = subset['probability']
    probs = probs / probs.sum()

    return np.random.choice(
        subset['company_size'],
        p=probs
    )

# ==> CELL 196
def apply_seasonality(consumption, state, usage_class, month):

    subset = seasonality[
        (seasonality['UF'] == state) &
        (seasonality['Classe'] == usage_class.capitalize()) &
        (seasonality['month'] == month)
    ]

    if subset.empty:
        return consumption

    factor = subset['seasonal_factor'].values[0]

    return consumption * factor

# ==> CELL 198
def generate_event(profiles):

    # -------------------------------------------------
    # 1) Escolha do estado
    # -------------------------------------------------
    state = np.random.choice(states, p=state_weights)


    # -------------------------------------------------
    # 2) Sorteio do mês
    # -------------------------------------------------
    month = np.random.randint(1, 13)


    # -------------------------------------------------
    # 3) Setor econômico condicionado ao estado
    # -------------------------------------------------
    usage_probs_state = usage_distribution_by_state.loc[state].values
    usage_probs_state = usage_probs_state / usage_probs_state.sum()

    usage_types = usage_distribution_by_state.columns

    usage_type = np.random.choice(
        usage_types,
        p=usage_probs_state
    )


    # -------------------------------------------------
    # 4) Perfil do setor
    # -------------------------------------------------
    profiles_subset = profiles[profiles['usage_type'] == usage_type]

    if profiles_subset.empty:
        raise ValueError(f"Nenhum profile encontrado para {usage_type}")

    row = profiles_subset.sample(1).iloc[0]


    # -------------------------------------------------
    # 5) Consumo base
    # -------------------------------------------------
    consumption = generate_consumption(row)


    # -------------------------------------------------
    # 6) Ajuste de sazonalidade
    # -------------------------------------------------
    consumption = apply_seasonality(
        consumption,
        state,
        usage_type,
        month
    )


    # -------------------------------------------------
    # 7) RUÍDO REALISTA DE CONSUMO
    # -------------------------------------------------
    # Mesmo equipamentos idênticos nunca operam exatamente
    # no mesmo regime. Pequenas variações operacionais,
    # carga parcial e comportamento do usuário geram
    # flutuações naturais no consumo energético.
    #
    # Usamos um ruído multiplicativo moderado (~8%).
    #
    operational_variation = np.random.normal(1, 0.08)
    consumption = consumption * operational_variation


    # -------------------------------------------------
    # 8) Tamanho da empresa
    # -------------------------------------------------
    company_size = sample_company_size(usage_type)


    # -------------------------------------------------
    # 9) Fonte energética
    # -------------------------------------------------
    energy_source = sample_energy_source(energy_dist)


    # -------------------------------------------------
    # 10) Emissão base (sua lógica atual)
    # -------------------------------------------------
    co2 = calculate_emission(consumption, energy_source, emission_df)


    # -------------------------------------------------
    # 11) VARIAÇÃO REAL DO FATOR DE EMISSÃO
    # -------------------------------------------------
    # Mesmo dentro da mesma fonte energética existe
    # variação operacional:
    #
    # • qualidade do combustível
    # • eficiência da planta
    # • mistura de geração
    # • condições de operação
    #
    # Isso é modelado como uma pequena variação
    # no fator efetivo de emissão (~6%).
    #
    emission_factor_variation = np.random.normal(1, 0.06)
    co2 = co2 * emission_factor_variation


    # -------------------------------------------------
    # 12) RUÍDO FINAL DE MEDIÇÃO / PROCESSO
    # -------------------------------------------------
    # Última camada de ruído representa:
    #
    # • imprecisão de medição
    # • pequenas perdas do sistema
    # • arredondamentos operacionais
    #
    measurement_noise = np.random.normal(1, 0.03)
    co2 = co2 * measurement_noise


    # -------------------------------------------------
    # 13) Data dentro do mês sorteado
    # -------------------------------------------------
    date = (
        pd.Timestamp('2025-01-01')
        + pd.DateOffset(months=month-1)
        + pd.to_timedelta(np.random.randint(0,28), unit='D')
    )


    # -------------------------------------------------
    # 14) Retorno do evento
    # -------------------------------------------------
    return {

        'company_id': f"C{np.random.randint(100000,999999)}",

        'date': date,

        'state': state,

        'usage_type': usage_type,

        'company_size': company_size,

        'fuel_type': row['fuel_type'],

        'energy_kwh': consumption,

        'energy_source': energy_source,

        'co2_emission': co2
    }

# ==> CELL 200
def generate_dataset(n):

    data = []

    for _ in range(n):
        data.append(generate_event(profiles))

    return pd.DataFrame(data)

# ==> CELL 202
df = generate_dataset(100000)

df.head()

# ==> CELL 203
df.to_csv('../data/processed/synthetic_energy_emissions_dataset.csv')

# ==> CELL 204
