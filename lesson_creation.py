import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import os
from dotenv import load_dotenv
import abii_utils

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
logging.info("Processed Excel Spreadsheet. :D")

# Set up
driver, wait = abii_utils.driver_setup()

# Login
abii_utils.abii_login(driver, wait, EMAIL, PASS)

# ... your automation code here ...
# Loop through every row in the DataFrame
for index, row in df.iterrows():
    # You can access each cell with row['column_name']
    # Example: print(row['question'])
    
    ##
    ## PreAssessment
    ##
    
    ############################################### Side Bar ############################################################################################## 
    # Click create lesson
    create_lesson_btn = wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/section/section/div/div[6]/div[1]/div/div/div[2]/button[2]'))
    create_lesson_btn.click()

    # Close the popup
    close_popup_btn = wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[4]/form/div/div[13]/div[1]/div/p'))
    close_popup_btn.click()

    # Set lesson type to math
    lesson_type_dropdown = wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="option_whitebox_invisible_scroll"]/span[1]/div/span/div[1]/div'))
    lesson_type_dropdown.click()
    math_option = wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="menu-lesson_type"]/div[3]/ul/li[2]'))
    math_option.click()
    
    # BUG: Select doesn't work for everything below must use method used by lesson_type.
    # Choose Grade
    grade_input = Select(wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[4]/form/div/div[13]/span[1]/div/span/div[1]/div/div/input')))
    # If Set 1: Grade K
    if (row[set] == 1):
        grade_input.select_by_index(1)
    # If Set 2: Grade 1
    else:
        grade_input.select_by_index(2)
        
    # Select National Standard Unit Name
    rand = Select(wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[4]/form/div/div[13]/span[1]/div/span/div[4]/div/div/input')))
    rand.select_by_index(1)
    
    # Select National Standard Unit Number
    rand = Select(wait.until(lambda d: d.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[4]/form/div/div[13]/span[1]/div/span/div[5]/div/div/input')))
    rand.select_by_index(1)
    
    input("Waiting...")
    





# Close the browser when done
driver.quit()


