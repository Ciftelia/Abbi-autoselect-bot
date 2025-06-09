from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import time
import re
import logging

# Import LessonOptions if it's defined in abbi_lesson_creation_elements
from abbi_lesson_creation_elements import LessonOptions, StaticElements, PreAssessmentElements, AnswerElements, \
    IntroductionElements, StepNElements, RecapElements

def parse_html_to_text(html):
    """
    Convert HTML to plain text, replacing <br> tags with newlines.

    Args:
        html (str): HTML string to convert.

    Returns:
        str: Plain text with newlines where <br> tags were present, and double newlines collapsed.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text()
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return f"Hint:\n\n{text}"

class AbiiUtils:
    """
    Utility class for automating lesson creation and interaction with the Abii platform using Selenium.
    """

    def __init__(self, email, password, options=None, url="https://mylessons.abiis-world.com/"):
        """
        Initialize the AbiiUtils object and open the browser.

        Args:
            email (str): User email for login.
            password (str): User password for login.
            options (webdriver.ChromeOptions, optional): Chrome options for Selenium.
            url (str, optional): URL to open. Defaults to Abii lessons site.
        """
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
        """
        Returns the Selenium WebDriver instance.
        """
        return self.driver
    
    def get_wait(self):
        """
        Returns the WebDriverWait instance.
        """
        return self.wait

    def select_from_dropdown_by_index(self, element, index):
        """
        Select an option from a dropdown by its index.

        Args:
            element (WebElement): The dropdown element to click.
            index (int): The index of the option to select (1-based).
        """
        element.click()
        menu = self.wait.until(lambda d: d.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        option = self.wait.until(lambda d: menu.find_element(By.XPATH, f'.//li[{index}]'))
        option.click()

    def select_from_dropdown_by_visible_text(self, element, text):
        """
        Select an option from a dropdown by its visible text.

        Args:
            element (WebElement): The dropdown element to click.
            text (str): The visible text of the option to select.
        """
        element.click()
        time.sleep(0.2)
        menu = self.wait.until(lambda d: d.find_element(By.XPATH, '//ul[contains(@class, "MuiList-root")]'))
        options = self.wait.until(lambda d: menu.find_elements(By.TAG_NAME, "li"))
        found = False
        for option in options:
            if option.text.strip().lower() == text.strip().lower():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()
                found = True
                break
        if not found:
            raise Exception(f"Dropdown option '{text}' not found.")
            
    def login(self):
        """
        Log in to the Abii platform using the provided email and password.
        """
        email_box = self.wait.until(lambda d: d.find_element(by=By.NAME, value="email"))
        password_box = self.wait.until(lambda d: d.find_element(by=By.NAME, value="password"))
        submit_button = self.wait.until(lambda d: d.find_element(by=By.CLASS_NAME, value="login-btn"))
        email_box.send_keys(self.email)
        password_box.send_keys(self.password)
        submit_button.click()
        
    def open_lesson_creation_page(self):
        """
        Open the lesson creation page and close the initial popup.
        """
        create_lesson_btn = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, 'button[data-title-left="Create A New Lesson"]'))
        create_lesson_btn.click()
        close_popup_btn = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '#info-modal-inner > p'))
        close_popup_btn.click()

    def add_multiple_choice_answers(self, elements, divisibility):
        """
        Fill in multiple choice answers based on divisibility.

        Args:
            elements: Elements object containing answer buttons.
            divisibility (str): "Yes" or "No" to determine answer order.
        """
        if (divisibility== "Yes"):
            elements.answers.answer_buttons[0].send_keys("Yes")
            elements.answers.answer_buttons[1].send_keys("No")
            elements.answers.answer_buttons[2].send_keys("I don't know")
        else:
            elements.answers.answer_buttons[0].send_keys("No")
            elements.answers.answer_buttons[1].send_keys("Yes")
            elements.answers.answer_buttons[2].send_keys("I don't know")

    def add_image(self, element, index):
        """
        Select an image by index from the image selection container.

        Args:
            element (WebElement): The button to open the image selector.
            index (int): The index of the image to select (1-based).
        """
        element.click()
        self.wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, f'#image_selection_container > div:nth-child({index}) > button')).click()

    def fill_intro_page(self, elements, onload_audio, img_index):
        """
        Fill the introduction page with an image and onload audio.

        Args:
            elements: Elements object for the intro page.
            onload_audio (str): Text for the onload audio.
            img_index (int): Index of the image to select.
        """
        self.add_image(elements.select_existing_image_button, img_index)
        self.generate_onload_audio(elements.text_to_speech_buttons[0], onload_audio)
        
    def fill_subject_page(self, elements, onload_audio, img_index):
        """
        Alias for fill_intro_page().
        
        """
        self.fill_intro_page(elements, onload_audio, img_index)

    def generate_onload_audio(self, element, text):
        """
        Generate onload audio for a given element and text.

        Args:
            element (WebElement): The button to trigger audio generation.
            text (str): The text to convert to audio.
        """
        element.click()
        input_box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#text-to-audio-input')))
        input_box.clear()
        input_box.send_keys(text)
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '#option_whitebox_invisible_scroll > span:nth-child(3) > div > span > div > div.text_to_audio_overlay > div > div > button')).click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.success-box.convert-msg-box')))
        self.wait.until(lambda d: d.find_element(By.CLASS_NAME, 'info_popup_close_btn')).click()
        
    def generate_wrong_audio(self, element, text):
        """ 
        Alias for generate_onload_audio().
        """
        self.generate_onload_audio(element, text)

    def generate_choice_audio(self, element):
        """
        Generate audio for multiple choice options.

        Args:
            element (WebElement): The button to trigger audio generation for choices.
        """
        element.click()
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,
                                            '#choice-audio-btn > div.text_to_audio_overlay > div > div:nth-child(2) > button')).click()
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,
                                            '#choice-audio-btn > div.text_to_audio_overlay > div > div:nth-child(2) > div:nth-child(4) > button')).click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.success-box.convert-msg-box')))
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,
                                            '#choice-audio-btn > div.text_to_audio_overlay > div > div:nth-child(2) > div:nth-child(5) > button')).click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.success-box.convert-msg-box')))
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,
                                            '#choice-audio-btn > div.text_to_audio_overlay > div > div:nth-child(2) > div:nth-child(6) > button')).click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.success-box.convert-msg-box')))
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR,
                                            '#choice-audio-btn > div.text_to_audio_overlay > div > div.close-btn-wrapper > button')).click()

    def load_static_elements(self):
        """
        Load and return all static elements used across the lesson creation flow.

        Returns:
            StaticElements: Object containing references to static elements.
        """
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
        """
        Load and return lesson options dropdown elements.

        Returns:
            LessonOptions: Object containing dropdown elements for lesson options.
        """
        return LessonOptions(
            lesson_type_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "lesson_type")),
            grade_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "grade")),
            language_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "language")),
            unit_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "unit")),
            standard_dropdown = self.wait.until(lambda d: d.find_element(By.ID, "standard"))
        )

    def load_answer_elements(self, answer_type_selection):
        """
        Load and return answer elements for the specified answer type.

        Args:
            answer_type_selection (str): The answer type to select.

        Returns:
            AnswerElements: Object containing answer-related elements.
        """
        answer_type_dropdown = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#body_whitebox > div:nth-child(6) > div.long_textarea_container > div > div"))
        answer_type_dropdown.click()
        self.select_from_dropdown_by_visible_text(answer_type_dropdown, answer_type_selection)

        answer_container=None
        answer_buttons=None
        if answer_type_selection == 'Multiple choice large text answer':
            answer_container = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#sng_dsp_input_container"))
            answer_buttons = self.wait.until(lambda d: answer_container.find_elements(By.CSS_SELECTOR, '#sng_dsp_input_container > span > textarea'))

        return AnswerElements(
            answer_type_dropdown=answer_type_dropdown,
            answer_container=answer_container,
            answer_buttons=answer_buttons,
        )

    def load_preasssessment_elements(self, answer_type_selection):
        """
        Load and return pre-assessment elements.

        Args:
            answer_type_selection (str): The answer type to use for pre-assessment.

        Returns:
            PreAssessmentElements: Object containing pre-assessment elements.
        """
        return PreAssessmentElements(
            answers = self.load_answer_elements(answer_type_selection),
            text_to_speech_buttons = self.wait.until(lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn")),
            question_input = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#overall_question_input")),
            select_existing_image_button = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
        )

    def load_introduction_elements(self):
        """
        Load and return introduction elements after clicking the introduction tab.

        Returns:
            IntroductionElements: Object containing introduction elements.
        """
        self.wait.until(lambda d: d.find_element(By.ID, "0")).click()
        return IntroductionElements(
            select_existing_image_button=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
            text_to_speech_buttons=self.wait.until(
                lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn")),
        )

    def load_subject_elements(self):
        """
        Load and return subject elements after clicking the subject tab.

        Returns:
            IntroductionElements: Object containing subject elements.
        """
        self.wait.until(lambda d: d.find_element(By.ID, "1")).click()
        return IntroductionElements(
            select_existing_image_button=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
            text_to_speech_buttons=self.wait.until(
                lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn")),
        )

    def load_step1_elements(self, answer_type_selection):
        """
        Load and return elements for step 1 after clicking the step 1 tab.

        Args:
            answer_type_selection (str): The answer type to use for step 1.

        Returns:
            StepNElements: Object containing step 1 elements.
        """
        self.wait.until(lambda d: d.find_element(By.ID, "3")).click()
        return StepNElements(
            step_name_input=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '#sidebar_tabs_container > div:nth-child(5) > textarea')),
            select_existing_image_button = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
            step_question_input=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '#body_whitebox > div:nth-child(5) > textarea')),
            answers = self.load_answer_elements(answer_type_selection),
            text_to_speech_buttons=self.wait.until(lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn"))
        )

    def load_step_n_elements(self, answer_type_selection):
        """
        Load and return elements for step n after adding a new screen and clicking the step n tab.

        Args:
            answer_type_selection (str): The answer type to use for step n.

        Returns:
            StepNElements: Object containing step n elements.
        """
        self.wait.until(lambda d: d.find_element(By.ID, "add_screen")).click()
        self.wait.until(lambda d: d.find_element(By.ID, "4")).click()
        return StepNElements(
            step_name_input=self.wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, '#sidebar_tabs_container > div:nth-child(6) > textarea')),
            select_existing_image_button=self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
            step_question_input=self.wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, '#body_whitebox > div:nth-child(5) > textarea')),
            answers=self.load_answer_elements(answer_type_selection),
            text_to_speech_buttons=self.wait.until(
                lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn"))
        )

    def load_recap_elements(self):
        """
        Load and return recap elements after clicking the recap tab.

        Returns:
            RecapElements: Object containing recap elements.
        """
        self.wait.until(lambda d: d.find_element(By.ID, "5")).click()
        return RecapElements(
            select_existing_image_button = self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#screenImage")),
            recap_question_input= self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "#body_whitebox > div:nth-child(5) > textarea")),
            text_to_speech_buttons = self.wait.until(
            lambda d: d.find_elements(By.CLASS_NAME, "convert_text_to_audio_btn"))
        )


