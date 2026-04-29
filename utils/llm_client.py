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
        

    def build_healing_prompt(self, locator_type: str, locator_value: str, page_source: str, driver=None) -> str:
        if driver:
            dom_snippet = driver.execute_script("""
                const form = document.querySelector('form') || document.body;
                return form.innerHTML.substring(0, 800);
            """)
        else:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")
            form = soup.find("form") or soup.find("body")
            dom_snippet = str(form)[:800] if form else page_source[:800]

        return f"""You are a Selenium locator healer. A locator failed. Suggest alternatives.
Broken: type={locator_type}, value={locator_value}
DOM:
{dom_snippet}
Return ONLY this JSON, no explanation:
{{"alternatives":[{{"strategy":"ID","value":"...","confidence":90}},{{"strategy":"XPATH","value":"...","confidence":80}}]}}"""