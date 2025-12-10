import argparse
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
import yaml
import os

def load_params():
    with open("params.yml", "r") as f:
        return yaml.safe_load(f)

def preprocess(input_path, output_path, scaler_path):
    
    df = pd.read_csv(input_path)
    
    if "Serial No." in df.columns:
        df.drop(columns=["Serial No."], inplace=True)

    x = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    pickle.dump(scaler, open(scaler_path, "wb"))

    vif_df = pd.DataFrame()
    vif_df["VIF"] = [variance_inflation_factor(x_scaled, i)
                     for i in range(x_scaled.shape[1])]
    vif_df["Feature"] = x.columns

    print("VIF Values:")
    print(vif_df)

    processed_df = pd.DataFrame(x_scaled, columns=x.columns)
    processed_df["y"] = y.values
    processed_df.to_csv(output_path, index=False)

    print(f"Processed full data saved to {output_path}")
    print(f"Scaler saved to {scaler_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--out_dir", required=True)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    params = load_params()
    preprocess(
        input_path=args.input,
        output_path=args.output,
        scaler_path=params["preprocess"]["scaling_out"]
    )