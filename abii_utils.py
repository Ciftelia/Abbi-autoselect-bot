from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class AbiiUtils:
    def __init__(self, email, password, options=None, url="https://mylessons.abiis-world.com/"):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            options.add_experimental_option("prefs", {
                "profile.password_manager_leak_detection": False
            })
        self.options = options
        self.url = url
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.email = email
        self.password = password
        
    def get_driver(self):
        return self.driver
    
    def get_wait(self):
        return self.wait

    def login(self):
        email_box = self.wait.until(lambda _: self.driver.find_element(by=By.NAME, value="email"))
        password_box = self.wait.until(lambda _: self.driver.find_element(by=By.NAME, value="password"))
        submit_button = self.wait.until(lambda _: self.driver.find_element(by=By.CLASS_NAME, value="login-btn"))
        email_box.send_keys(self.email)
        password_box.send_keys(self.password)
        submit_button.click()
        
    def open_lesson_creation_page(self):
        # Click create lesson
        create_lesson_btn = self.wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/section/section/div/div[6]/div[1]/div/div/div[2]/button[2]'))
        create_lesson_btn.click()
        
        # Close the popup
        close_popup_btn = self.wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[4]/form/div/div[13]/div[1]/div/p'))
        close_popup_btn.click()

    def select_from_dropdown_by_index(self, element, index):
        element.click()
        menu = self.wait.until(lambda _: self.driver.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        option = menu.find_element(By.XPATH, f'.//li[{index}]')
        option.click()

    def select_from_dropdown_by_innertext(self, element, text):
        element.click()
        menu = self.wait.until(lambda _: self.driver.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        options = menu.find_elements(By.TAG_NAME, "li")
        for option in options:
            if option.text.strip() == text:
                option.click()
                break

