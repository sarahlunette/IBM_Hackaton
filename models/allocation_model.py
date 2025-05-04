# models/allocation_model.py

import requests

class AllocationModel:
    def __init__(self, model_name="granite3.2:8b", endpoint="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint

    def predict_allocation(self, needs_data: dict) -> str:
        # Convert structured input into a prompt
        prompt = (
            f"The following emergency has occurred:\n"
            f"- Urgency level: {needs_data['urgency_level']}\n"
            f"- Location: {needs_data['location']}\n"
            f"- Resources needed: {', '.join(needs_data['resources_needed'])}\n\n"
            "Based on this, suggest how resources should be allocated efficiently."
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error during model call: {e}"
