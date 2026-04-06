import joblib
from sklearn.pipeline import Pipeline
import os

# Model path
model_path = r'c:\Repositorio\carbon-footprint-analysis\models\carbon_footprint_rf_v1.joblib'

if os.path.exists(model_path):
    # Load the model
    # Note: Using joblib, which was mentioned in README as the persistence tool
    model = joblib.load(model_path)
    
    # Access the regressor from the pipeline
    # The pipeline step name is 'regressor' based on create_model_training.py
    if isinstance(model, Pipeline):
        regressor = model.named_steps['regressor']
    else:
        regressor = model
    
    # Check the max depth of the trees in the forest
    # RandomForestRegressor has an 'estimators_' attribute
    depths = [estimator.get_depth() for estimator in regressor.estimators_]
    avg_depth = sum(depths) / len(depths)
    max_depth = max(depths)
    min_depth = min(depths)
    
    print(f"Número de árvores: {len(regressor.estimators_)}")
    print(f"Altura mínima: {min_depth}")
    print(f"Altura máxima: {max_depth}")
    print(f"Altura média: {avg_depth:.2f}")
else:
    print(f"Erro: Modelo não encontrado em {model_path}")
