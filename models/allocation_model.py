from models.ibm_granite_integration import GraniteChatModel

class AllocationModel:
    def __init__(self):
        self.chat_model = GraniteChatModel()

    def predict_allocation(self, needs_data: dict) -> dict:
        """
        Predict resource allocation based on needs.
        """
        prompt = (
            f"The following area has an urgent situation:\n"
            f"Urgency Level: {needs_data.get('urgency_level')}\n"
            f"Location: {needs_data.get('location')}\n"
            f"Resources Needed: {', '.join(needs_data.get('resources_needed', []))}\n"
            f"Please suggest how to allocate available emergency resources (e.g., ambulances, medical teams). "
            f"Respond with a JSON object like {{'ambulance': 2, 'medical_team': 1}}."
        )

        system_message = "You are an emergency response assistant trained to allocate disaster relief resources efficiently."

        response = self.chat_model.chat(prompt, system=system_message)

        try:
            return eval(response) if isinstance(response, str) else response
        except Exception:
            return {"error": "Failed to parse model response."}
