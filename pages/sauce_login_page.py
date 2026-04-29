# pages/sauce_login_page.py (Current - Classical)
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
    
    def enter_username(self, text):
        self.driver.find_element(*self.username_field).send_keys(text)
    
    def enter_password(self, text):
        self.driver.find_element(*self.password_field).send_keys(text)
    
    def click_login(self):
        self.driver.find_element(*self.login_btn).click()