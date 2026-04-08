import pandas as pd
import os

DATA_DIR = '../data/processed' if os.path.exists('../data/processed') else 'data/processed'

def check_assertions():
    try:
        profiles = pd.read_csv(os.path.join(DATA_DIR, 'v2_consumption_profiles.csv'))
        company_size_dist = pd.read_csv(os.path.join(DATA_DIR, 'v2_company_size_distribution_by_usage.csv'))
        seasonality = pd.read_csv(os.path.join(DATA_DIR, 'v2_seasonality_state_class_month.csv'))
        usage_distribution_by_state = pd.read_csv(os.path.join(DATA_DIR, 'v2_usage_distribution_by_state.csv'), index_col=0)

        expected = {'comercial', 'industrial', 'outros', 'residencial', 'rural'}
        
        print("Checking profiles['usage_type']...")
        profiles_types = set(profiles['usage_type'].unique())
        print(f"Found: {profiles_types}")
        assert profiles_types <= expected, f"usage_type inesperado em profiles: {profiles_types}"

        print("\nChecking company_size_dist['Classe']...")
        company_classes = set(company_size_dist['Classe'].unique())
        print(f"Found: {company_classes}")
        assert company_classes <= expected, f"Classe inesperada em company_size_dist: {company_classes}"

        print("\nChecking seasonality['Classe']...")
        seasonality_classes = set(seasonality['Classe'].unique())
        print(f"Found: {seasonality_classes}")
        assert seasonality_classes <= expected, f"Classe inesperada em seasonality: {seasonality_classes}"

        print("\nChecking usage_distribution_by_state.columns...")
        state_columns = set(usage_distribution_by_state.columns)
        print(f"Found: {state_columns}")
        # Profiles might have a subset, but let's check if they are all in expected or match profiles
        assert state_columns <= expected or state_columns == profiles_types, f"Mismatch setores: state={state_columns} | expected={expected}"

        print("\n✓ ALL ASSERTIONS PASSED!")
        
    except Exception as e:
        print(f"\n❌ ASSERTION FAILED: {e}")
        exit(1)

if __name__ == "__main__":
    check_assertions()
