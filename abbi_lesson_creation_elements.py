from dataclasses import dataclass
from selenium.webdriver.remote.webelement import WebElement

@dataclass
class LessonOptions:
    """Elements inside the Lesson Options section (dropdowns)."""
    lesson_type_dropdown: WebElement
    grade_dropdown: WebElement
    language_dropdown: WebElement
    unit_dropdown: WebElement
    standard_dropdown: WebElement

@dataclass
class AnswerElements:
    answer_type_dropdown: WebElement
    answer_container: WebElement
    answer_buttons: list[WebElement]

@dataclass
class StaticElements:
    """Elements that persist across all pages in the lesson creation flow."""
    lesson_options: LessonOptions          # Lesson options section (dropdowns)
    lesson_name_input: WebElement          # lesson_name_input
    mark_as_ready_button: WebElement       # lesson_submit_btn
    save_button: WebElement                # lesson_save_btn
    back_to_dashboard_button: WebElement   # whiteboard_redirect_btn
    logo_upload_input: WebElement          # logo-upload-input
    mascot_buttons: list[WebElement]       # character_overlay

@dataclass
class PreAssessmentElements:
    """Elements that are in the pre assessment section."""
    answers: AnswerElements
    text_to_speech_buttons: list[WebElement]
    question_input: WebElement
    select_existing_image_button: WebElement

@dataclass
class IntroductionElements:
    select_existing_image_button: WebElement
    text_to_speech_buttons: list[WebElement]

@dataclass
class SubjectElements:
    select_existing_image_button: WebElement
    text_to_speech_buttons: list[WebElement]

@dataclass
class StepNElements:
    step_name_input: WebElement
    step_question_input: WebElement
    select_existing_image_button: WebElement
    answers: AnswerElements
    text_to_speech_buttons: list[WebElement]

@dataclass
class RecapElements:
    select_existing_image_button: WebElement
    recap_question_input: WebElement
    text_to_speech_buttons: list[WebElement]
