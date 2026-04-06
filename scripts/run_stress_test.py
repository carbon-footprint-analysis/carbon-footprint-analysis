import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os

# Semente aleatória
np.random.seed(42)

# Path to data
data_path = r'c:\Repositorio\carbon-footprint-analysis\data\processed\synthetic_energy_emissions_dataset.csv'
df = pd.read_csv(data_path)

# Preprocessing
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
def get_season(month):
    if month in [12, 1, 2]: return 'Verao'
    if month in [3, 4, 5]: return 'Outono'
    if month in [6, 7, 8]: return 'Inverno'
    return 'Primavera'
df['season'] = df['month'].apply(get_season)

# Features
target = 'co2_emission'
features = ['energy_kwh', 'state', 'usage_type', 'energy_source', 'month', 'season']
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline Preprocessor
numeric_features = ['energy_kwh', 'month']
categorical_features = ['state', 'usage_type', 'energy_source', 'season']
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Random Forest
model_rf = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))])
model_rf.fit(X_train, y_train)

# Original Metric
y_pred = model_rf.predict(X_test)
r2_original = r2_score(y_test, y_pred)

# STRESS TEST: 5% Noise
X_test_noisy = X_test.copy()
noise_scale = X_test_noisy['energy_kwh'] * 0.05
noise = np.random.normal(0, 1, size=len(X_test_noisy)) * noise_scale
X_test_noisy['energy_kwh'] += noise

y_pred_noisy = model_rf.predict(X_test_noisy)
r2_noisy = r2_score(y_test, y_pred_noisy)

print(f"R2_ORIGINAL:{r2_original:.4f}")
print(f"R2_NOISY:{r2_noisy:.4f}")
print(f"DROP_PERCENT:{((r2_original - r2_noisy) / r2_original) * 100:.2f}%")
