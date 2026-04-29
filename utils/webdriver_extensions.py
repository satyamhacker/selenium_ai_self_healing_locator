# utils/webdriver_extensions.py
import asyncio
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

# utils/webdriver_extensions.py

class WebDriverExtensions:
    @staticmethod
    def AIfind_element_sync(driver, locator_type: str, locator_value: str, timeout: int = 10):
        try:
            # 🔹 Happy Path: locator_type is already a By string (e.g. "css selector", "id")
            element = driver.find_element(locator_type, locator_value)
            print(f"✅ Primary: {locator_type}='{locator_value}'")
            return element
            
        except NoSuchElementException as e:
            print(f"⚠️ Primary FAILED: {locator_type}='{locator_value}'")
            print("🔍 Extracting DOM snippet...")
            
            page_snippet = driver.page_source[:3000]
            
            from utils.llm_client import LocalLLMClient
            llm = LocalLLMClient()
            prompt = llm.build_healing_prompt(locator_type, locator_value, page_snippet)
            
            import json, re
            ai_response = llm.call_local_ai(prompt)
            # Strip markdown code fences if model wraps response
            clean = re.sub(r"```(?:json)?\s*|\s*```", "", ai_response).strip()
            suggestions = json.loads(clean)
            print(f"🤖 AI Suggestions: {suggestions}")
            
            # Handle both {"alternatives": [...]} and flat {"ID": ..., "XPATH": ...} formats
            alternatives = suggestions.get("alternatives", [])
            if not alternatives:
                alternatives = [
                    {"strategy": k, "value": v}
                    for k, v in suggestions.items()
                    if k in ("ID", "XPATH", "CSS_SELECTOR")
                ]
            
            for alt in alternatives:
                strategy_key = alt.get("strategy", "").upper()
                new_value = alt.get("value", "")
                new_strategy = getattr(By, strategy_key, None)
                if not new_strategy or not new_value:
                    continue
                print(f"🔄 Retrying with {strategy_key}='{new_value}'")
                try:
                    return driver.find_element(new_strategy, new_value)
                except:
                    continue
            
            raise e