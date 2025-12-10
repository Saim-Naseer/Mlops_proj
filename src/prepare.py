import pandas as pd
import numpy as np
import argparse
import os

def convert_to_fast(df):

    df["entry_test_score"] = (df["GRE Score"] - 260) / (340 - 260) * 100

    df["entry_test_score"] = df["entry_test_score"].clip(0, 110)

    df["intermediate_marks_percent"] = df["TOEFL Score"] / 120 * 100
    df["intermediate_marks_percent"] = df["intermediate_marks_percent"].clip(0, 100)

    df["matric_marks_percent"] = (df["CGPA"] / 10 * 85) + np.random.uniform(-3, 3, size=len(df))
    df["matric_marks_percent"] = df["matric_marks_percent"].clip(0, 100)
    df["chance_of_admit"] = df["Chance of Admit"]

    fast_df = df[[
        "entry_test_score",
        "intermediate_marks_percent",
        "matric_marks_percent",
        "chance_of_admit"
    ]].copy()

    return fast_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=str, default="data")
    parser.add_argument("--orig_data", type=str)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    df = pd.read_csv(os.path.join(args.out_dir, args.orig_data))
    df_final=convert_to_fast(df)

    df_final.to_csv(os.path.join(args.out_dir, "Fast_Admission_Predict.csv"), index=False)
    print("Saved Fast_Admission_Predict.csv in", args.out_dir)