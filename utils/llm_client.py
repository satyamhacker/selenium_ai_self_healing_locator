
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

class LocalLLMClient:
    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/api/generate")
        self.model_name = os.getenv("LOCAL_LLM_MODEL_NAME", "mistral:7b")

    # ---------- existing ----------
    def call_local_ai(self, prompt: str) -> str:
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            resp = requests.post(f"{self.base_url}", json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception:
            return ""

    # ---------- new ----------
    def build_healing_prompt(self, locator_type: str, locator_value: str,
                             page_source: str, driver=None) -> str:
        """
        Builds a concise prompt for the LLM.
        If driver is given we use execute_script for speed; else fall back to BS4.
        DOM snippet is capped at ~800 chars to stay within token limits.
        """
        # 1. Grab relevant DOM snippet
        if driver:
            # Fast path: browser already has the live DOM
            snippet = driver.execute_script(
                "return document.querySelector('form')?.outerHTML ?? document.body.outerHTML"
            ) or ""
        else:
            # Fallback: parse static page_source
            soup = BeautifulSoup(page_source, "html.parser")
            form = soup.find("form")
            snippet = str(form) if form else str(soup.find("body") or soup)[:800]

        snippet = snippet[:800]  # hard cap

        # 2. Craft the prompt
        prompt = f"""
        The following locator failed:
        - strategy: {locator_type}
        - value: {locator_value}

        Current DOM context (≤800 chars):
        {snippet}

        Return ONLY a valid JSON array with alternative locators, sorted by confidence (highest first). Each object MUST have:
        {{
        "strategy": "ID" | "CSS_SELECTOR" | "XPATH",
        "value": "<new_locator>",
        "confidence": <0-100 integer>
        }}

        Do NOT include any extra text or markdown fences.
        """.strip()
        return prompt