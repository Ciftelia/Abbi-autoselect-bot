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
class StaticElements:
    """Elements that persist across all pages in the lesson creation flow."""
    lesson_options: LessonOptions          # Lesson options section (dropdowns)
    lesson_name_input: WebElement          # lesson_name_input
    mark_as_ready_button: WebElement       # lesson_submit_btn
    save_button: WebElement                # lesson_save_btn
    back_to_dashboard_button: WebElement   # whiteboard_redirect_btn
    logo_upload_input: WebElement          # logo-upload-input
    mascot_buttons: list[WebElement]       # character_overlay