from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")

    def enter_username(self, text):
        username_field = self.driver.find_element(*self.username)
       
        username_field.send_keys(text)

    def enter_password(self, text):
        password_field = self.driver.find_element(*self.password_field)
      
        password_field.send_keys(text)

    def click_login(self):
        login_button = self.driver.find_element(*self.login_btn)
        login_button.click()
