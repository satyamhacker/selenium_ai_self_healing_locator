# pages/sauce_login_page.py (Current - Classical)
from selenium.webdriver.common.by import By
from utils.webdriver_extensions import WebDriverExtensions

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.CSS_SELECTOR, "[data-test='wrong-username-locator']")
        self.password_field = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
    
    def _find(self, locator):
        return WebDriverExtensions.AIfind_element_sync(self.driver, locator[0], locator[1])

    def enter_username(self, text):
        self._find(self.username).send_keys(text)
    
    def enter_password(self, text):
        self._find(self.password_field).send_keys(text)
    
    def click_login(self):
        self._find(self.login_btn).click()