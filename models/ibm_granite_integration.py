import os
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
import torch

class GraniteChatModel:
    def __init__(self, model_name="ibm-granite/granite-3.3-2b-base", token_env_var="HF_TOKEN"):
        token = os.getenv(token_env_var)
        if not token:
            raise EnvironmentError(f"Missing environment variable: {token_env_var}")
        login(token=token)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16, device_map="auto", load_in_8bit=True
        )
        self.pipe = TextGenerationPipeline(model=self.model, tokenizer=self.tokenizer)

    def chat(self, prompt: str, system: str = None) -> str:
        full_prompt = f"{system}\n{prompt}" if system else prompt
        output = self.pipe(full_prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
        return output[0]["generated_text"]

    def summarize_crisis(self, posts: list[str]) -> str:
        prompt = "Summarize the following crisis reports:\n" + "\n".join(posts)
        return self.chat(prompt, system="You are an expert in emergency crisis summarization.")

    def generate_response_plan(self, context: str) -> str:
        prompt = f"Given this context, propose a resource allocation:\n{context}"
        return self.chat(prompt, system="You are an emergency logistics coordinator.")

    def generate_call_to_action(self, needs: str, location: str) -> str:
        prompt = f"Write a short social media post to ask for help. Needs: {needs}, Location: {location}"
        return self.chat(prompt, system="You write public crisis alerts.")
