# pages/sauce_login_page.py (Current - Classical)
from selenium.webdriver.common.by import By
from utils.webdriver_extensions import WebDriverExtensions

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.CSS_SELECTOR, "[data-test='wrong-username-locator']")
        self.password_field = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
    
    def enter_username(self, text):
        WebDriverExtensions.AIfind_element_sync(self.driver, self.username[0].name, self.username[1]).send_keys(text)
    
    def enter_password(self, text):
        WebDriverExtensions.AIfind_element_sync(self.driver, self.password_field[0].name, self.password_field[1]).send_keys(text)
    
    def click_login(self):
        WebDriverExtensions.AIfind_element_sync(self.driver, self.login_btn[0].name, self.login_btn[1]).click()