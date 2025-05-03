from granite import GraniteModel

class GraniteChatModel:
    def __init__(self, model_id: str = "ibm/granite-13b-chat-v2"):
        self.model = GraniteModel(model_id=model_id)

    def chat(self, prompt: str, system: str = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.model.chat(messages)
        return response['generation']
