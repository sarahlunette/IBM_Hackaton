import ollama

class StreamingGraniteModel:
    def __init__(self, model_name="granite3.2:8b"):
        self.model_name = model_name

    def stream_response(self, prompt):
        stream = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            yield chunk['message']['content']
