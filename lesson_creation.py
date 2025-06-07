import pandas as pd
from selenium.webdriver.common.by import By
import os
import logging
from dotenv import load_dotenv
from abii_utils import AbiiUtils

# load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

# Configure logging at the top of your script
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more details
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Process spreadsheet
logging.info("Processing Excel Spreadsheet...")
df = pd.read_excel("all questions.xlsx")
logging.info("Processed Excel Spreadsheet.")

# Set up
abii = AbiiUtils(email=EMAIL, password=PASS)

# get driver and wait
driver = abii.get_driver()
wait = abii.get_wait()

# Login
abii.login()

for index, row in df.iterrows():
    logging.info("Opening lesson creation page...")
    abii.open_lesson_creation_page()
    
    # Start with static elements
    logging.info("Loading static elements...")
    elements = abii.load_static_elements()
    logging.info("Loaded static elements.")
    
    # Set up static elements
    # Wait until the lesson type dropdown is clickable before selecting 'Math'
    abii.select_from_dropdown_by_visible_text(elements.lesson_options.lesson_type_dropdown, 'Math')
    abii.select_from_dropdown_by_visible_text(
        elements.lesson_options.grade_dropdown,"Grade K" if row['Set'] == 1 or row['Set'] == '1' else "Grade 1"
    )
    abii.select_from_dropdown_by_index(elements.lesson_options.unit_dropdown, 2)
    abii.select_from_dropdown_by_index(elements.lesson_options.standard_dropdown, 2)
    elements.lesson_name_input.send_keys(f"V1: Lesson Set {row['Set']} Q{row['Question Number']}")
    elements.mascot_buttons[1].click() 

    # temp pause to output
    input("Waiting...")





# Close the browser when done
driver.quit()


