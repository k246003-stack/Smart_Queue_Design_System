from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
from src.scheduler.customer_scheduler import Teller, assign_customer
import uvicorn
import os

MODEL_PATH = "models/rf_queue_model.pkl"

app = FastAPI(title="Smart Queue Model API")

class CustomerIn(BaseModel):
    Customer_ID: str
    Arrival_Time: str  # ISO datetime
    Transaction_Type: str
    Priority: str
    Teller_Specialization: str
    Teller_Efficiency: float
    Queue_Length_At_Arrival: int
    Wait_Time: int

# load model
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    print("Model file not found. Train model first and place at", MODEL_PATH)

# init tellers
tellers = [
    Teller("T01","General",0.95),
    Teller("T02","Accounts",0.85),
    Teller("T03","General",0.90),
    Teller("T04","Loans",0.80),
    Teller("T05","General",0.92),
]

@app.post("/predict-and-assign")
def predict_and_assign(customer: CustomerIn):
    df = pd.DataFrame([{
        "Transaction_Type": customer.Transaction_Type,
        "Priority": customer.Priority,
        "Teller_Specialization": customer.Teller_Specialization,
        "Teller_Efficiency": customer.Teller_Efficiency,
        "Queue_Length_At_Arrival": customer.Queue_Length_At_Arrival,
        "Wait_Time": customer.Wait_Time
    }])
    if model is None:
        return {"error": "Model not loaded. Train model first."}
    pred = round(float(model.predict(df)[0]), 1)
    customer_dict = customer.dict()
    customer_dict["Arrival_Time"] = datetime.fromisoformat(customer_dict["Arrival_Time"])
    customer_dict["Predicted_Service_Time"] = float(pred)
    assignment = assign_customer(customer_dict, tellers)
    return {
        "Predicted_Service_Time": float(pred),
        "Assignment": {
            "Assigned_Teller": assignment["Assigned_Teller"],
            "Start_Time": assignment["Start_Time"].isoformat(),
            "Service_Duration": assignment["Service_Duration"],
            "End_Time": assignment["End_Time"].isoformat()
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
