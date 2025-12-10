import pandas as pd
import pickle
import yaml
from sklearn.metrics import r2_score, mean_squared_error
import json
from sklearn.model_selection import train_test_split
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--out_dir", required=True)
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)

# Load params
with open("params.yml", "r") as f:
    params = yaml.safe_load(f)

preprocess_params = params["preprocess"]
paths = params["paths"]

# Load data
df = pd.read_csv("data/processed.csv")
x = df.drop(columns=["y"])
y = df["y"]

# Split (same as train)
x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=preprocess_params["test_size"],
    random_state=preprocess_params["random_state"]
)

# Load model
model = pickle.load(open(paths["model_out"], "rb"))

# Evaluate
r2 = model.score(x_test, y_test)
mse = mean_squared_error(y_test, model.predict(x_test))
metrics = {"r2": r2, "mse": mse}

with open(paths["metrics_out"], "w") as f:
    json.dump(metrics, f)

print("Evaluation metrics:", metrics)