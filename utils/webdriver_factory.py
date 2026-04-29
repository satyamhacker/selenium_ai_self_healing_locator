from selenium import webdriver

def create_chrome_driver():
    print("Creating Chrome driver...")
    driver = webdriver.Chrome()
    print("Chrome driver created successfully!")
    return driver
