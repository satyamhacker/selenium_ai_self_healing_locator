# pages/sauce_login_page.py

from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators (using data-test attributes for robustness)
        self.username = (By.CSS_SELECTOR, "[data-test='username']")
        self.password = (By.CSS_SELECTOR, "[data-test='password']")
        self.login_btn = (By.CSS_SELECTOR, "[data-test='login-button']")

    # Actions
    def enter_username(self, username_text):
        self.driver.find_element(*self.username).send_keys(username_text)

    def enter_password(self, password_text):
        self.driver.find_element(*self.password).send_keys(password_text)

    def click_login(self):
        self.driver.find_element(*self.login_btn).click()