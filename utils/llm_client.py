# utils/llm_client.py

import requests
import os
from dotenv import load_dotenv
import requests
import json

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
            response = requests.post(self.base_url, json=payload, timeout=120)

            # Raise error if request failed
            response.raise_for_status()

            # Assuming API returns JSON with 'response' field
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling local AI: {e}")
            return ""
        

    def build_healing_prompt(self, locator_type: str, locator_value: str, page_source: str) -> str:
                """
                AI ke liye strict JSON prompt banata hai taaki hallucination na ho.
                """
                return f"""
            You are an expert Selenium locator healer. 
            Given a broken locator, suggest alternative valid locators for the same element.

            Broken Locator Type: {locator_type}
            Broken Locator Value: {locator_value}

            Current DOM Context (snippet):
            {page_source[:3000]}  # First 3000 chars to avoid token overflow

            RULES:
            1. Return ONLY valid JSON format. No markdown, no explanations.
            2. Use double quotes strictly for keys and values.
            3. Provide at least 2 alternative strategies if possible.

            Expected JSON Schema:
            {{
                "alternatives": [
                    {{"strategy": "ID", "value": "new-id-here", "confidence": 95}},
                    {{"strategy": "XPATH", "value": "//input[@data-test='username']", "confidence": 85}}
                ]
            }}
            """.strip()