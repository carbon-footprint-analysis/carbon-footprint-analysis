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

# Seleção de atributos e target
target = 'co2_emission'
# Removemos o target e colunas não-preditivas (IDs e Datas brutas)
X = df.drop(columns=[target, 'company_id', 'date'])
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

# 1. Linear Regression
model_lr = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', LinearRegression())])
model_lr.fit(X_train, y_train)
r2_lr = r2_score(y_test, model_lr.predict(X_test))

# 2. Random Forest
model_rf = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))])
model_rf.fit(X_train, y_train)
r2_rf = r2_score(y_test, model_rf.predict(X_test))

print(f"LR_R2:{r2_lr:.4f}")
print(f"RF_R2:{r2_rf:.4f}")
