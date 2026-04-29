# utils/llm_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # pulls variables from .env into environ

class LocalLLMClient:
    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("LOCAL_LLM_MODEL_NAME", "mistral:7b")

    def call_local_ai(self, prompt: str) -> str:
        """
        Calls the local Ollama API and returns the generated text.
        Returns empty string on any failure to keep the framework resilient.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            resp = requests.post(
                f"{self.base_url}",
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception:
            return ""
