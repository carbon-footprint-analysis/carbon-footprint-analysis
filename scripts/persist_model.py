import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Semente aleatória
np.random.seed(42)

# Path to data
data_path = r'c:\Repositorio\carbon-footprint-analysis\data\processed\synthetic_energy_emissions_dataset.csv'
df = pd.read_csv(data_path)

# Preprocessing from EDA
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
def get_season(month):
    if month in [12, 1, 2]: return 'Verao'
    if month in [3, 4, 5]: return 'Outono'
    if month in [6, 7, 8]: return 'Inverno'
    return 'Primavera'
df['season'] = df['month'].apply(get_season)

# Seleção de atributos e target
target = 'co2_emission'
# Removemos o target e colunas não-preditivas (IDs e Datas brutas)
X = df.drop(columns=[target, 'company_id', 'date'])
y = df[target]

# Train/Test Split (we train on the whole set for the final model deployment)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing Pipeline
numeric_features = ['energy_kwh', 'month']
categorical_features = ['state', 'usage_type', 'energy_source', 'season']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Model Pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))
])

# Final Training
print("Treinando o modelo final...")
model_pipeline.fit(X_train, y_train)

# Persist the Model
model_dir = 'models'
model_file = os.path.join(model_dir, 'carbon_footprint_rf_v1.joblib')

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

joblib.dump(model_pipeline, model_file)
print(f"Modelo salvo com sucesso em: {model_file}")

# Verify metrics one last time
y_pred = model_pipeline.predict(X_test)
from sklearn.metrics import r2_score
print(f"Integridade final (R²): {r2_score(y_test, y_pred):.4f}")
