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
            # 🔹 Happy Path: Standard Selenium call
            strategy = getattr(By, locator_type.upper(), None)
            element = driver.find_element(strategy, locator_value)
            print(f"✅ Primary: {locator_type}='{locator_value}'")
            return element
            
        except NoSuchElementException as e:
            # 🔹 🔥 YAHAN SE AI HEALING SHURU HOTI HAI 🔥
            print(f"⚠️ Primary FAILED: {locator_type}='{locator_value}'")
            print("🔍 Extracting DOM snippet...")
            
            # Step 1: DOM snapshot lo (sirf 3000 chars)
            page_snippet = driver.page_source[:3000]
            
            # Step 2: Prompt banayo (utils/llm_client.py se import)
            from utils.llm_client import LocalLLMClient
            llm = LocalLLMClient()
            prompt = llm.build_healing_prompt(locator_type, locator_value, page_snippet)
            
            # Step 3: 🤖 AI CALL YAHAN HO RAHA HAI 🤖
            from utils.llm_client import LocalLLMClient
            llm = LocalLLMClient()
            ai_response = llm.call_local_ai(prompt)  # ← HTTP POST to Ollama
            
            # Step 4: JSON parse karo
            import json
            suggestions = json.loads(ai_response)
            print(f"🤖 AI Suggestions: {suggestions}")
            
            # Step 5: Retry loop (pehla successful locator return karo)
            for strat_key in ["ID", "XPATH", "CSS_SELECTOR"]:
                if strat_key in suggestions:
                    new_strategy = getattr(By, strat_key)
                    new_value = suggestions[strat_key]
                    print(f"🔄 Retrying with {strat_key}='{new_value}'")
                    try:
                        return driver.find_element(new_strategy, new_value)
                    except:
                        continue  # Agar yeh bhi fail hua, next strategy try karo
            
            # Sab strategies fail → Original error raise karo
            raise e