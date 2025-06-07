from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
import logging

# Import LessonOptions if it's defined in abbi_lesson_creation_elements
from abbi_lesson_creation_elements import LessonOptions, StaticElements

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
        self.wait = WebDriverWait(self.driver, timeout=30)
        self.email = email
        self.password = password
        
    def get_driver(self):
        return self.driver
    
    def get_wait(self):
        return self.wait

    def select_from_dropdown_by_index(self, element, index):
        element.click()
        menu = self.wait.until(lambda d: d.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        option = self.wait.until(lambda d: menu.find_element(By.XPATH, f'.//li[{index}]'))
        option.click()

    def select_from_dropdown_by_visible_text(self, element, text):
        element.click()
        menu = self.wait.until(lambda d: d.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        options = self.wait.until(lambda d: menu.find_elements(By.TAG_NAME, "li"))
        for option in options:
            if option.text == text:
                option.click()
                break
            
    def login(self):
        email_box = self.wait.until(lambda d: d.find_element(by=By.NAME, value="email"))
        password_box = self.wait.until(lambda d: d.find_element(by=By.NAME, value="password"))
        submit_button = self.wait.until(lambda d: d.find_element(by=By.CLASS_NAME, value="login-btn"))
        email_box.send_keys(self.email)
        password_box.send_keys(self.password)
        submit_button.click()
        
    def open_lesson_creation_page(self):
        # Click create lesson
        create_lesson_btn = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[data-title-left="Create A New Lesson"]'))
        create_lesson_btn.click()
        
        # Close the popup
        close_popup_btn = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '#info-modal-inner > p'))
        close_popup_btn.click()
        
    def load_static_elements(self):
        '''
        Loads and returns all static elements used across the lesson creation flow.
        '''
        return StaticElements(
            lesson_options=self.load_lesson_options(),
            lesson_name_input=self.wait.until(lambda d: d.find_element(By.ID, "lesson_name_input")),
            mark_as_ready_button=self.wait.until(lambda d: d.find_element(By.ID, "lesson_submit_btn")),
            save_button=self.wait.until(lambda d: d.find_element(By.ID, "lesson_save_btn")),
            back_to_dashboard_button=self.wait.until(lambda d: d.find_element(By.ID, "whiteboard_redirect_btn")),
            logo_upload_input=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#logo_upload_and_info_btn > div:nth-child(2) > div:nth-child(1) > div > div > label > span")),
            mascot_buttons=self.wait.until(lambda d: d.find_element(By.ID, "character_overlay").find_elements(By.XPATH, ".//button")),
        )
        
        
    def load_lesson_options(self) -> LessonOptions:
        '''
        '''
        return LessonOptions(
            lesson_type_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "lesson_type")),
            grade_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "grade")),
            language_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "language")),
            unit_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "unit")),
            standard_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "standard"))
        )

