from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
