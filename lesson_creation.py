import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import os
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

# ... your automation code here ...
# Loop through every row in the DataFrame
for index, row in df.iterrows():
    # You can access each cell with row['column_name']
    # Example: print(row['question'])
    
    abii.open_lesson_creation_page()
    # abii.load_preassessment_elements()

    
    # temp pause to output
    input("Waiting...")
    





# Close the browser when done
driver.quit()


