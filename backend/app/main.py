from fastapi import FastAPI
from app.schema import StudentInput
from app.utils import predict_admission
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="University Admission Predictor")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/predict")
def predict(input_data: StudentInput):
    prediction = predict_admission(input_data.dict())
    return {"chance_of_admission": prediction}
