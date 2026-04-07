"""
Converte todos os CSVs processados e o notebook para usar categorias em português brasileiro.
"""
import json
import pandas as pd

# ─────────────────────────────────────────────
# 1. MAPAS DE CONVERSÃO
# ─────────────────────────────────────────────

setor_map = {
    # inglês → PT-BR
    'agriculture':  'rural',
    'commercial':   'comercial',
    'industrial':   'industrial',
    'other':        'outros',
    'residential':  'residencial',
    # title case PT → PT minúsculo
    'Comercial':    'comercial',
    'Industrial':   'industrial',
    'Outros':       'outros',
    'Residencial':  'residencial',
    'Rural':        'rural',
}

fonte_map = {
    'hydro':    'hidrelétrica',
    'nuclear':  'nuclear',
    'solar':    'solar',
    'thermal':  'térmica',
    'wind':     'eólica',
}

porte_map = {
    'small':    'pequena',
    'medium':   'média',
    'large':    'grande',
}

# ─────────────────────────────────────────────
# 2. ATUALIZAR CSVs
# ─────────────────────────────────────────────

# -- v2_consumption_profiles --
df = pd.read_csv('data/processed/v2_consumption_profiles.csv')
df['usage_type'] = df['usage_type'].map(lambda x: setor_map.get(x, x))
df.to_csv('data/processed/v2_consumption_profiles.csv', index=False)
print('v2_consumption_profiles:', sorted(df['usage_type'].unique()))

# -- v2_company_size_distribution_by_usage --
df = pd.read_csv('data/processed/v2_company_size_distribution_by_usage.csv')
df['Classe'] = df['Classe'].map(lambda x: setor_map.get(x, x))
df['company_size'] = df['company_size'].map(lambda x: porte_map.get(x, x))
df.to_csv('data/processed/v2_company_size_distribution_by_usage.csv', index=False)
print('v2_company_size_dist Classe:', sorted(df['Classe'].unique()))
print('v2_company_size_dist porte:', sorted(df['company_size'].unique()))

# -- v2_usage_distribution_by_state (colunas) --
df = pd.read_csv('data/processed/v2_usage_distribution_by_state.csv', index_col=0)
df.columns = [setor_map.get(c, c) for c in df.columns]
df.to_csv('data/processed/v2_usage_distribution_by_state.csv')
print('v2_usage_distribution_by_state cols:', sorted(df.columns.tolist()))

# -- v2_seasonality_state_class_month --
df = pd.read_csv('data/processed/v2_seasonality_state_class_month.csv')
df['Classe'] = df['Classe'].map(lambda x: setor_map.get(x, x))
df.to_csv('data/processed/v2_seasonality_state_class_month.csv', index=False)
print('v2_seasonality Classe:', sorted(df['Classe'].unique()))

# -- v2_energy_source_distribution --
df = pd.read_csv('data/processed/v2_energy_source_distribution.csv')
df['energy_source'] = df['energy_source'].map(lambda x: fonte_map.get(x, x))
df.to_csv('data/processed/v2_energy_source_distribution.csv', index=False)
print('v2_energy_source_distribution:', sorted(df['energy_source'].unique()))

# -- v2_energy_source_emission_factors --
df = pd.read_csv('data/processed/v2_energy_source_emission_factors.csv')
df['energy_source'] = df['energy_source'].map(lambda x: fonte_map.get(x, x))
df.to_csv('data/processed/v2_energy_source_emission_factors.csv', index=False)
print('v2_emission_factors:', sorted(df['energy_source'].unique()))

print('\n✓ Todos os CSVs atualizados')
