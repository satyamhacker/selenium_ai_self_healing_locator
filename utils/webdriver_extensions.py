# utils/webdriver_extensions.py
import json
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.llm_client import LocalLLMClient

class WebDriverExtensions:
    @staticmethod
    async def AIfind_element(driver, locator_type: str, locator_value: str):
        """
        Tries the primary locator; on failure asks the LLM for alternatives.
        Returns the first working WebElement.
        
        Args:
            driver: WebDriver instance
            locator_type: String representing locator strategy ('ID', 'CSS_SELECTOR', 'XPATH')
            locator_value: The locator value string
            
        Returns:
            WebElement: The found element
            
        Raises:
            NoSuchElementException: If no valid locator works
        """
        # Convert string locator_type to By constant
        locator_type_map = {
            'ID': By.ID,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'XPATH': By.XPATH,
            'NAME': By.NAME,
            'CLASS_NAME': By.CLASS_NAME,
            'TAG_NAME': By.TAG_NAME,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT
        }
        
        by_type = locator_type_map.get(locator_type.upper())
        if not by_type:
            raise ValueError(f"Invalid locator type: {locator_type}")

        # 1. Primary attempt
        try:
            return driver.find_element(by_type, locator_value)
        except NoSuchElementException:
            print("Locator jeopardized. Healing...")

        # 2. Build prompt and call AI
        try:
            llm = LocalLLMClient()
            prompt = llm.build_healing_prompt(
                locator_type, locator_value, driver.page_source, driver
            )
            raw = llm.call_local_ai(prompt)
        except Exception as e:
            raise NoSuchElementException(f"AI client error: {str(e)}")

        # 3. Guard against empty / malformed response
        if not raw or not raw.strip():
            raise NoSuchElementException("AI returned no alternatives")

        # 4. Strip markdown fences and parse JSON
        raw = re.sub(r"```(?:json)?", "", raw).strip()
        try:
            alternatives = json.loads(raw)
            if not isinstance(alternatives, list):
                alternatives = [alternatives]
            if not alternatives:
                raise ValueError("Empty alternatives list")
        except json.JSONDecodeError as e:
            raise NoSuchElementException(f"AI response is not valid JSON: {str(e)}")

        # 5. Try each alternative until one works
        for alt in alternatives:
            if not isinstance(alt, dict):
                continue
                
            strategy = alt.get("strategy", "").upper()
            value = alt.get("value", "")
            
            if not strategy or not value:
                continue
                
            by_const = locator_type_map.get(strategy)
            if not by_const:
                continue
                
            try:
                return driver.find_element(by_const, value)
            except NoSuchElementException:
                continue

        # 6. Nothing worked
        raise NoSuchElementException("All AI-suggested locators failed")
