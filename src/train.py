# src/train.py
import pandas as pd
import yaml
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

with open("params.yaml") as f:
    params = yaml.safe_load(f)

mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
mlflow.set_experiment(params["mlflow"]["experiment_name"])

train = pd.read_csv("data/processed/train.csv")
train.columns = train.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
target = params["train"]["target_col"]
X = train.drop(columns=[target])
y = train[target]

# simple pipeline
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("rf", RandomForestRegressor(
        n_estimators=params["train"]["n_estimators"],
        max_depth=params["train"]["max_depth"],
        random_state=params["train"]["random_seed"]
    ))
])

# automatic logging
mlflow.sklearn.autolog()

with mlflow.start_run():
    pipe.fit(X, y)
    # save model artifact to models/
    os.makedirs("models", exist_ok=True)
    joblib.dump(pipe, params["paths"]["model_out"])
    mlflow.log_artifact(params["paths"]["model_out"])
print("trained and saved model.")
