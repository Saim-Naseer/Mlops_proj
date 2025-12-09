# src/evaluate.py
import pandas as pd
import joblib
from sklearn.metrics import r2_score, mean_squared_error
import json
import yaml

with open("params.yaml") as f:
    params = yaml.safe_load(f)

val = pd.read_csv("data/processed/val.csv")
val.columns = val.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
target = params["train"]["target_col"]
X_val = val.drop(columns=[target])
y_val = val[target]

model = joblib.load(params["paths"]["model_out"])
pred = model.predict(X_val)

metrics = {
    "r2": r2_score(y_val, pred),
    "mse": mean_squared_error(y_val, pred)
}
os.makedirs("metrics", exist_ok=True)
with open(params["paths"]["metrics_out"], "w") as f:
    json.dump(metrics, f, indent=2)
print("wrote metrics:", metrics)
