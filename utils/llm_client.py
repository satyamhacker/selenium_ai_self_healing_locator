# utils/llm_client.py

import requests
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class LocalLLMClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/api/generate")
        self.model_name = os.getenv("LOCAL_LLM_MODEL_NAME", "qwen:1.8b") # Default model name

    def call_local_ai(self, prompt: str) -> str:
        """
        Send a prompt to the local AI server and return the response text.
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.base_url, json=payload)

            # Raise error if request failed
            response.raise_for_status()

            # Assuming API returns JSON with 'response' field
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling local AI: {e}")
            return ""