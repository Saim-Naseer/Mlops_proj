import pickle
import numpy as np
import requests
import json
import pandas as pd

# Load scaler
scaler = pickle.load(open("models/scaling_model.pkl", "rb"))

columns = list(scaler.feature_names_in_)


# New student data
X_new = np.array([[320, 110, 4, 4.5, 4.0, 9.0, 1]])  # raw 0-100 values
X_new_df = pd.DataFrame(X_new, columns=columns)

print(X_new_df)
X_scaled = scaler.transform(X_new_df)




# Call MLflow API
url = "http://127.0.0.1:1234/invocations"
payload = {"inputs": X_scaled.tolist()}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print("Predicted Chance of Admit:", response.json())