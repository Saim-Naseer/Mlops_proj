# src/preprocess.py
import pandas as pd
import os
import yaml
from sklearn.model_selection import train_test_split

with open("params.yaml") as f:
    params = yaml.safe_load(f)

raw = params["data"]["raw_path"]
outdir = params["data"]["processed_dir"]
os.makedirs(outdir, exist_ok=True)

df = pd.read_csv(raw)

# normalize column names to safe names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

# if column name contains trailing underscores etc, inspect and adjust
# target column - try to normalize expected column names
if "chance_of_admit" not in df.columns and "chance_of_admit_" in df.columns:
    df = df.rename(columns={"chance_of_admit_":"chance_of_admit"})

# simple preprocessing: drop na's
df = df.dropna()

# split
test_size = params["train"]["test_size"]
seed = params["train"]["random_seed"]
train_df, val_df = train_test_split(df, test_size=test_size, random_state=seed)

train_df.to_csv(os.path.join(outdir, "train.csv"), index=False)
val_df.to_csv(os.path.join(outdir, "val.csv"), index=False)
print("wrote processed files to", outdir)
