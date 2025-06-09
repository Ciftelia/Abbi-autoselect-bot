import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
from dotenv import load_dotenv

from abii_utils import AbiiUtils, parse_html_to_text
import time

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
    logging.info(f"Processing question %d...", index)
    logging.info("Opening lesson creation page...")
    abii.open_lesson_creation_page()
    logging.info("Opened lesson creation page.")
    
    #########################################################################################
    # Static Elements #######################################################################
    #########################################################################################
    logging.info("Loading static elements...")
    elements_static = abii.load_static_elements()
    logging.info("Loaded static elements.")
    time.sleep(1)
    # TODO:  Make the lines below more clear with encapsulation.
    abii.select_from_dropdown_by_visible_text(elements_static.lesson_options.lesson_type_dropdown, 'Math')
    abii.select_from_dropdown_by_visible_text(
        elements_static.lesson_options.grade_dropdown,"Grade K" if row['Set'] == 1 or row['Set'] == '1' else "Grade 1"
    )
    abii.select_from_dropdown_by_index(elements_static.lesson_options.unit_dropdown, 2)
    abii.select_from_dropdown_by_index(elements_static.lesson_options.standard_dropdown, 2)
    elements_static.lesson_name_input.send_keys(f"Abii: Lesson Set {row['Set']} Q{row['Question Number']:02d}")
    # TODO: Make this more clear.
    elements_static.mascot_buttons[1].click()
    logging.info("Entered static elements.")

    ##########################################################################################
    ## PreAssessment Elements ################################################################
    ##########################################################################################
    logging.info("Loading pre-assessment elements...")
    elements = abii.load_preasssessment_elements("Multiple choice large text answer")
    logging.info("Loaded pre-assessment elements.")
    time.sleep(1)
    # Add question
    elements.question_input.send_keys(row['Question'])
    # Choose Image
    abii.add_image(1)
    # Gen answers

    if row['Is Divisable?'] == 'Yes':
        answers = ['Yes', "No", 'Hint 1']
    else:
        answers = ['No', "Yes", 'Hint 1']

    # Add choices
    abii.add_multiple_choice_answers(answers)
    # Add audio
    abii.generate_onload_audio(row['Question'])
    logging.info("Entered pre-assessment elements.")

    ##########################################################################################
    ## Introduction and Subject Elements #####################################################
    ##########################################################################################
    logging.info("Entering introduction elements...")
    abii.fill_intro_page( f'Lesson Set {row['Set']}, Question {row['Question Number']}', 1)
    logging.info("Entered introduction elements.")
    logging.info("Entering subject elements...")
    abii.fill_subject_page(f"Let's get started!", 1)
    logging.info("Entered subject elements.")

    ##########################################################################################
    ## Step 1 Elements #######################################################################
    # ##########################################################################################
    logging.info("Loading step 1 elements...")
    elements = abii.load_step1_elements("Multiple choice large text answer")
    logging.info("Loaded step 1 elements.")
    time.sleep(1)
    # Set step name
    elements.step_name_input.send_keys('Step 1')
    # add image
    abii.add_image(1)
    # add step question
    elements.step_question_input.send_keys(row['General Hint (Text + Audio)'])
    # Gen answers

    if row['Is Divisable?'] == 'Yes':
        answers = ['Yes', "No", 'Hint 2']
    else:
        answers = ['No', "Yes", 'Hint 2']

    # add answers
    abii.add_multiple_choice_answers(answers)
    # add audio
    abii.generate_onload_audio(row['General Hint (Text + Audio)'])
    abii.generate_wrong_audio(' ')
    abii.generate_choice_audio()
    logging.info("Entered step 1 elements.")

    ##########################################################################################
    ## Step 2 Elements #######################################################################
    ##########################################################################################
    logging.info("Loading step 2 elements...")
    elements = abii.load_step_n_elements("Multiple choice large text answer")
    logging.info("Loaded step 2 elements.")
    time.sleep(1)
    # Set step name
    elements.step_name_input.send_keys('Step 2')
    # add image
    abii.add_image(1)
    # add step question
    elements.step_question_input.send_keys(row['Specific (Text)'])
    # add answers
    if row['Is Divisable?'] == 'Yes':
        answers = ['Yes', "No", 'Hint 3']
    else:
        answers = ['No', "Yes", 'Hint 3']
    abii.add_multiple_choice_answers(answers)
    # add audio
    abii.generate_onload_audio(row['Specific (Audio)'])
    abii.generate_wrong_audio(' ')
    abii.generate_choice_audio()
    logging.info("Entered step 2 elements.")

    ##########################################################################################
    ## Recap Elements ########################################################################
    ##########################################################################################

    logging.info("Loading recap elements...")
    elements = abii.load_recap_elements()
    logging.info("Loaded recap elements.")
    time.sleep(1)
    # add image
    abii.add_image(1)
    # add step question
    elements.recap_question_input.send_keys(parse_html_to_text(row['Detailed Hint (HTML Text)']))
    # add audio
    abii.generate_onload_audio(row['Detailed Hint (Audio)'])
    logging.info("Entered recap elements.")

    logging.info("Processed question %d.", index)

    # Save and move on
    elements_static.mark_as_ready_button.click()
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)


# Close the browser when done
driver.quit()


