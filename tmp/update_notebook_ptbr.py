"""
Atualiza as células do notebook 01_build_dataset_generation_config.ipynb
para usar PT-BR em tudo:
 - Remove category_map / normalize_classe (não precisa mais)
 - Atualiza Cell 176 (carga dos dados) com carregamento direto
 - Atualiza Cell 178 (normalize) para apenas renomear colunas do usage_distribution
 - Atualiza Cell 194 (sample_company_size) - mantém defensivo
 - Atualiza Cell 196 (apply_seasonality) - já usa 'Classe' direto
 - Atualiza Cell 198 (generate_event) - colunas em PT-BR
 - Adiciona Cell 200 (generate_dataset) - sem mudanças
"""
import json

nb = json.load(open('notebooks/01_build_dataset_generation_config.ipynb', encoding='utf-8'))
cells = nb['cells']

# ─────────────────────────────────────────────
# CELL 176: carga dos dados (remover import desnecessário, manter limpo)
# ─────────────────────────────────────────────
CELL_176_NEW = """\
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

state_dist = pd.read_csv('../data/processed/v2_state_distribution.csv')
states = state_dist['UF'].values
state_weights = state_dist['Consumo'].values / state_dist['Consumo'].sum()
"""

# ─────────────────────────────────────────────
# CELL 178: normalize_classe → substituída por validação simples
# ─────────────────────────────────────────────
CELL_178_NEW = """\
# Todos os CSVs já estão em português minúsculo após a conversão.
# Verificação de consistência:

assert set(profiles['usage_type'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\
    f"usage_type inesperado em profiles: {set(profiles['usage_type'].unique())}"

assert set(company_size_dist['Classe'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\
    f"Classe inesperada em company_size_dist: {set(company_size_dist['Classe'].unique())}"

assert set(seasonality['Classe'].unique()) <= {'comercial', 'industrial', 'outros', 'residencial', 'rural'}, \\
    f"Classe inesperada em seasonality: {set(seasonality['Classe'].unique())}"

setores_state = set(usage_distribution_by_state.columns)
setores_profiles = set(profiles['usage_type'].unique())
assert setores_state == setores_profiles, \\
    f"Mismatch setores: state={setores_state} | profiles={setores_profiles}"

print("✓ Todas as categorias estão consistentes em PT-BR")
print("  Setores:", sorted(setores_profiles))
print("  Fontes:", sorted(energy_dist['energy_source'].unique()))
print("  Portes:", sorted(company_size_dist['company_size'].unique()))
"""

# ─────────────────────────────────────────────
# CELL 194: sample_company_size (PT-BR, defensivo)
# ─────────────────────────────────────────────
CELL_194_NEW = """\
def sample_company_size(setor):
    \"\"\"
    Sorteia o porte da empresa para o setor dado.
    Retorna 'pequena' como fallback se o setor não for encontrado.
    \"\"\"
    subset = company_size_dist[company_size_dist['Classe'] == setor].copy()

    if subset.empty:
        return 'pequena'

    portes = subset['company_size'].values
    probs  = subset['probability'].values.astype(float)

    total = probs.sum()
    if total <= 0:
        return 'pequena'

    probs = probs / total

    return np.random.choice(portes, p=probs)
"""

# ─────────────────────────────────────────────
# CELL 196: apply_seasonality (sem mudanças de lógica, só comentário PT)
# ─────────────────────────────────────────────
CELL_196_NEW = """\
def apply_seasonality(consumo, estado, setor, mes):
    \"\"\"
    Ajusta o consumo pelo fator de sazonalidade (estado × setor × mês).
    Retorna o consumo original se não houver dado para a combinação.
    \"\"\"
    subset = seasonality[
        (seasonality['UF']     == estado) &
        (seasonality['Classe'] == setor)  &
        (seasonality['month']  == mes)
    ]

    if subset.empty:
        return consumo

    fator = subset['seasonal_factor'].values[0]
    return consumo * fator
"""

# ─────────────────────────────────────────────
# CELL 198: generate_event (COLUNAS EM PT-BR)
# ─────────────────────────────────────────────
CELL_198_NEW = """\
def generate_event(profiles):

    # -------------------------------------------------
    # 1) Escolha do estado
    # -------------------------------------------------
    estado = np.random.choice(states, p=state_weights)


    # -------------------------------------------------
    # 2) Sorteio do mês
    # -------------------------------------------------
    mes = np.random.randint(1, 13)


    # -------------------------------------------------
    # 3) Setor econômico condicionado ao estado
    # -------------------------------------------------
    probs_estado = usage_distribution_by_state.loc[estado].values.astype(float)
    probs_estado = probs_estado / probs_estado.sum()

    setores = usage_distribution_by_state.columns.tolist()

    setor = np.random.choice(setores, p=probs_estado)


    # -------------------------------------------------
    # 4) Perfil do setor
    # -------------------------------------------------
    profiles_subset = profiles[profiles['usage_type'] == setor]

    if profiles_subset.empty:
        raise ValueError(f"Nenhum perfil encontrado para o setor: {setor!r}")

    row = profiles_subset.sample(1).iloc[0]


    # -------------------------------------------------
    # 5) Consumo base
    # -------------------------------------------------
    consumo = generate_consumption(row)


    # -------------------------------------------------
    # 6) Ajuste de sazonalidade
    # -------------------------------------------------
    consumo = apply_seasonality(consumo, estado, setor, mes)


    # -------------------------------------------------
    # 7) Ruído operacional (~8%)
    # -------------------------------------------------
    consumo = consumo * np.random.normal(1, 0.08)


    # -------------------------------------------------
    # 8) Porte da empresa
    # -------------------------------------------------
    porte = sample_company_size(setor)


    # -------------------------------------------------
    # 9) Fonte de energia
    # -------------------------------------------------
    fonte = sample_energy_source(energy_dist)


    # -------------------------------------------------
    # 10) Emissão de CO₂ base
    # -------------------------------------------------
    co2 = calculate_emission(consumo, fonte, emission_df)


    # -------------------------------------------------
    # 11) Variação do fator de emissão (~6%)
    # -------------------------------------------------
    co2 = co2 * np.random.normal(1, 0.06)


    # -------------------------------------------------
    # 12) Ruído de medição (~3%)
    # -------------------------------------------------
    co2 = co2 * np.random.normal(1, 0.03)


    # -------------------------------------------------
    # 13) Data dentro do mês sorteado
    # -------------------------------------------------
    data = (
        pd.Timestamp('2025-01-01')
        + pd.DateOffset(months=mes - 1)
        + pd.to_timedelta(np.random.randint(0, 28), unit='D')
    )


    # -------------------------------------------------
    # 14) Retorno do evento
    # -------------------------------------------------
    return {
        'id_empresa':      f"C{np.random.randint(100000, 999999)}",
        'data':            data,
        'estado':          estado,
        'setor':           setor,
        'porte':           porte,
        'tipo_combustivel': row['fuel_type'],
        'consumo_kwh':     consumo,
        'fonte_energia':   fonte,
        'emissao_co2':     co2,
    }
"""

# ─────────────────────────────────────────────
# CELL 200: generate_dataset
# ─────────────────────────────────────────────
CELL_200_NEW = """\
def generate_dataset(n):
    \"\"\"Gera n eventos sintéticos de consumo e emissão de CO₂.\"\"\"
    data = []

    for _ in range(n):
        data.append(generate_event(profiles))

    return pd.DataFrame(data)
"""

# ─────────────────────────────────────────────
# MAPA: índice da célula → novo conteúdo
# ─────────────────────────────────────────────
cell_updates = {
    176: CELL_176_NEW,
    178: CELL_178_NEW,
    194: CELL_194_NEW,
    196: CELL_196_NEW,
    198: CELL_198_NEW,
    200: CELL_200_NEW,
}

for idx, new_src in cell_updates.items():
    cells[idx]['source'] = new_src
    print(f'  ✓ Cell {idx} atualizada')

with open('notebooks/01_build_dataset_generation_config.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('\n✓ Notebook salvo com sucesso')
