from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def sleep_until_next_hour():
    now = datetime.now()
    next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    sleep_seconds = (next_hour - now).total_seconds()
    print(f"Sleeping {sleep_seconds:.0f} seconds until {next_hour}")
    time.sleep(sleep_seconds)

def log_data(wcount: int):
    logs_dir = os.getenv("LOG_PATH")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    curr_time = datetime.now()
    date_str = curr_time.strftime('%Y-%m-%d')
    time_str = curr_time.strftime('%H:%M')
    
    log_file_path = os.path.join(logs_dir, f"{date_str}.csv")
    line = f"{time_str}, {wcount}\n"
    with open(log_file_path, "a") as f:
        f.write(line)
    print(line.strip())

def main():
    global driver
    options = webdriver.ChromeOptions()
    options.binary_location = os.getenv("CHROMIUM_PATH")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(os.getenv("CHROMIUM_PATH")), options=options)

    # options = webdriver.SafariOptions()
    # driver = webdriver.Safari(options=options)
    try:
        url = f"https://{os.getenv("URL")}"
        driver.get(url)
        driver.fullscreen_window()
        time.sleep(5)
        enter_button = driver.find_element(By.CSS_SELECTOR, "button.button.btn.btn-red.agree")
        enter_button.click()
        time.sleep(5)
        sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button.signin")
        sign_in_btn.click()
        time.sleep(5)
        username_field = driver.find_element(By.CSS_SELECTOR, "form#login-form input.username")
        password_field = driver.find_element(By.CSS_SELECTOR, "form#login-form input.password")
        username_field.send_keys(os.getenv("USERNAME"))
        password_field.send_keys(os.getenv("PASSWORD"))
        time.sleep(5)
        sign_in_submit = driver.find_element(By.CSS_SELECTOR, "button.submit")
        sign_in_submit.click()
        time.sleep(10)

    except:
        main()

def follow_user(wdriver):
    try:
        url_dom = f"https://{os.getenv("URL")}/{os.getenv("URI_1")}/{os.getenv("URI_UNAME")}"
        wdriver.get(url_dom)
        time.sleep(10)
        wbutton = wdriver.find_element(By.ID, os.getenv("BTN_TAG"))
        wbutton.click()
        time.sleep(5)
        counter_span = wdriver.find_element(By.CSS_SELECTOR, os.getenv("CSS_TAG"))
        wcount = int(counter_span.text)
        log_data(wcount)

    except:
        main()
        follow_user(wdriver)

if __name__ == "__main__":
    load_dotenv()
    main()
    while True:
        follow_user(driver)
        sleep_until_next_hour()
