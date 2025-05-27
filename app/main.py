from fastapi import FastAPI, Query
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.allocation_model import AllocationModel
from models.llm_allocator import LLMResourceAllocator  # <-- NEW IMPORT

app = FastAPI()
model = AllocationModel()
llm_allocator = LLMResourceAllocator()  # <-- NEW INITIALIZATION

@app.get("/predict-allocation")
def predict(urgency: str, location: str, needs: str):
    needs_data = {
        "urgency_level": urgency,
        "location": location,
        "resources_needed": needs.split(",")
    }
    prediction = model.predict_allocation(needs_data)
    return {"suggested_allocation": prediction}

@app.get("/predict-allocation-llm")  # <-- NEW ENDPOINT
def predict_llm(urgency: str, location: str, needs: str):
    tweet = f"Urgency: {urgency}, Location: {location}, Needs: {needs}"
    result = llm_allocator.allocate_with_llm([tweet])
    return {
        "summary": result["summary"],
        "plan": result["plan"]
    }
