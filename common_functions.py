from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def abii_setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False
    })
    driver = webdriver.Chrome(options=options)
    driver.get("https://mylessons.abiis-world.com/creators/login/?next=/")
    wait = WebDriverWait(driver, timeout=10)
    
    return driver, wait

def abii_login(driver, wait, email, password):
    email_box = wait.until(lambda _: driver.find_element(by=By.NAME, value="email"))
    password_box = wait.until(lambda _: driver.find_element(by=By.NAME, value="password"))
    submit_button = wait.until(lambda _: driver.find_element(by=By.CLASS_NAME, value="login-btn"))

    email_box.send_keys(email)
    password_box.send_keys(password)
    submit_button.click()