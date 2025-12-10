import requests
import pandas as pd
import json
from pickle import load

# Load scaler
scaler = load(open("models/scaling_model.pkl", "rb"))

MLFLOW_URL = "http://mlflow-serve:1234/invocations"

def predict_admission(data: dict):

    key_mapping = {
        'GRE_Score': 'GRE Score',
        'TOEFL_Score': 'TOEFL Score',
        'University_Rating': 'University Rating',
        'SOP': 'SOP',
        'LOR': 'LOR',
        'CGPA': 'CGPA',
        'Research': 'Research'
    }

    data_renamed = {key_mapping[k]: v for k, v in data.items()}

    df = pd.DataFrame([data_renamed], columns=scaler.feature_names_in_)
    X_scaled = scaler.transform(df)

    payload = {"inputs": X_scaled.tolist()}
    headers = {"Content-Type": "application/json"}
    response = requests.post(MLFLOW_URL,  data=json.dumps(payload), headers=headers)
    print(response.json()["predictions"][0])
    return response.json()["predictions"][0]
