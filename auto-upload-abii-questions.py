from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import os
from dotenv import load_dotenv

def main():
    POSSIBLE_VALUES = ["1015", "Mental Math"]
    load_dotenv()
    EMAIL = os.getenv("EMAIL")
    PASS = os.getenv("PASS")
    text = ""

    while (text not in POSSIBLE_VALUES):
        print("Type in the lesson type you'd like to pick: ", POSSIBLE_VALUES)
        text = input()
        
    if text == POSSIBLE_VALUES[0]:
        selections = ["Python", "puzzle"]
    else:
        selections = ["Lesson Set 1", "Lesson Set 2"]

    # set up
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("prefs", {
        "profile.password_manager_leak_detection": False
    })
    driver = webdriver.Chrome(options=options)
    driver.get("https://mylessons.abiis-world.com/creators/login/?next=/")
    wait = WebDriverWait(driver, timeout=10)

    # login
    email_box = wait.until(lambda _: driver.find_element(by=By.NAME, value="email"))
    password_box = wait.until(lambda _: driver.find_element(by=By.NAME, value="password"))
    submit_button = wait.until(lambda _: driver.find_element(by=By.CLASS_NAME, value="login-btn"))

    email_box.send_keys(EMAIL)
    password_box.send_keys(PASS)
    submit_button.click()

    # Click Send Lessons to ABii
    send_lessons_btn = wait.until(
        lambda d: d.find_element(By.XPATH, "//div[@id='dashboard_banner_btns']//button[contains(., 'Send Lessons to ABii')]"), 50
    )
    send_lessons_btn.click()

    # get chosen lessons
    table_body = wait.until(
        lambda d: d.find_element(By.XPATH, '//*[@id="dashboard_div"]/section/section/div/div[6]/div[3]/div[2]/div/div[2]/div/table/tbody'))

    rows = wait.until(lambda _: table_body.find_elements(By.TAG_NAME, "tr"))

    for row in rows:
        first_th = wait.until(lambda d: row.find_element(By.TAG_NAME, "th"))
        first_td = wait.until(lambda d: row.find_element(By.TAG_NAME, "td"))
        # check if clicked
        if (row.get_attribute("class") == "MuiTableRow-root MuiTableRow-hover Mui-selected"):
            if not any(sel in first_th.text for sel in selections):
                first_td.click()
        else:
            if any(sel in first_th.text for sel in selections):
                first_td.click()
                
    print("\nLesson selection complete, please review the selection and send the results to the robot with the 'Save Changes' button at the bottom of the screen.")
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        