# ibm_granite_integration.py
import os
from huggingface_hub import login
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextGenerationPipeline,
)
import torch


class GraniteChatModel:
    def __init__(self, model_name="ibm-granite/granite-3.3-2b-base", token_env_var="HF_TOKEN"):
        token = os.getenv(token_env_var)
        if not token:
            raise EnvironmentError(f"Missing environment variable: {token_env_var}")
        login(token=token)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_8bit=True,  # 2B models often fit in 8bit with 8GB VRAM
        )

        self.pipe = TextGenerationPipeline(model=self.model, tokenizer=self.tokenizer)

    def chat(self, prompt: str, system: str = None) -> str:
        full_prompt = f"{system}\n{prompt}" if system else prompt
        try:
            output = self.pipe(full_prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
            return output[0]["generated_text"]
        except Exception as e:
            return f"Error: {str(e)}"


# Optional CLI test
if __name__ == "__main__":
    os.environ["HF_TOKEN"] = "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"
    model = GraniteChatModel()
    result = model.chat(
        "What are the main responsibilities of emergency medical services during a disaster?",
        system="You are an expert in emergency response systems."
    )
    print("Model Response:\n", result)
