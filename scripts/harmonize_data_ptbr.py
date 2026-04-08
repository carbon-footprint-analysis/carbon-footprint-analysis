import pandas as pd
import os

# Define the maps
setor_map = {
    'agriculture':  'rural',
    'commercial':   'comercial',
    'industrial':   'industrial',
    'other':        'outros',
    'residential':  'residencial',
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

# Paths to data files
DATA_DIR = 'data/processed'

def harmonize_file(filename, column_mappings):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"! File not found: {filepath}")
        return

    df = pd.read_csv(filepath)
    
    # Check if there's an unnamed index column and remove if found (to avoid duplication on save)
    if df.columns[0].startswith('Unnamed') or df.columns[0] == '':
        df = df.iloc[:, 1:]

    modified = False
    for col, mapping in column_mappings.items():
        if col in df.columns:
            df[col] = df[col].map(lambda x: mapping.get(x, x))
            modified = True
        elif col == '_columns_':  # Special case for column labels
            df.columns = [mapping.get(c, c) for c in df.columns]
            modified = True

    if modified:
        df.to_csv(filepath, index=False)
        print(f"✓ Harmonized: {filename}")
    else:
        print(f"• No changes needed for: {filename}")

def run_harmonization():
    print("Starting data harmonization to PT-BR...")
    
    # 1. Consumption Profiles
    harmonize_file('v2_consumption_profiles.csv', {'usage_type': setor_map})
    
    # 2. Energy Source Distribution
    harmonize_file('v2_energy_source_distribution.csv', {'energy_source': fonte_map})
    
    # 3. Company Size Distribution
    harmonize_file('v2_company_size_distribution_by_usage.csv', {
        'Classe': setor_map,
        'company_size': porte_map
    })
    
    # 4. Usage Distribution by State (Column labels)
    harmonize_file('v2_usage_distribution_by_state.csv', {'_columns_': setor_map})
    
    # 5. Seasonality
    harmonize_file('v2_seasonality_state_class_month.csv', {'Classe': setor_map})
    
    # 6. Emission Factors (already PT-BR but ensure consistency)
    harmonize_file('v2_energy_source_emission_factors.csv', {'energy_source': fonte_map})

    print("\nVerifying consistency...")
    verify_consistency()

def verify_consistency():
    try:
        profiles = pd.read_csv(os.path.join(DATA_DIR, 'v2_consumption_profiles.csv'))
        energy_dist = pd.read_csv(os.path.join(DATA_DIR, 'v2_energy_source_distribution.csv'))
        emission_df = pd.read_csv(os.path.join(DATA_DIR, 'v2_energy_source_emission_factors.csv'))
        
        prof_sources = set(profiles['usage_type'].unique())
        dist_sources = set(energy_dist['energy_source'].unique())
        emis_sources = set(emission_df['energy_source'].unique())
        
        print(f"Usage types in profiles: {prof_sources}")
        print(f"Energy sources in distribution: {dist_sources}")
        print(f"Energy sources in emission factors: {emis_sources}")
        
        mismatch = dist_sources - emis_sources
        if mismatch:
            print(f"❌ MISMATCH: {mismatch} in distribution but not in emission factors!")
        else:
            print("✓ Distribution and Emission Factors are in sync.")
            
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    # Ensure we are in the root directory
    if not os.path.exists('data'):
        os.chdir('..')
    run_harmonization()
