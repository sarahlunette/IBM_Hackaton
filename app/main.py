from fastapi import FastAPI, Query
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.allocation_model import AllocationModel

app = FastAPI()
model = AllocationModel()

@app.get("/predict-allocation")
def predict(urgency: str, location: str, needs: str):
    needs_data = {
        "urgency_level": urgency,
        "location": location,
        "resources_needed": needs.split(",")
    }
    prediction = model.predict_allocation(needs_data)
    return {"suggested_allocation": prediction}
