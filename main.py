from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from datetime import datetime, timedelta
import os

def sleep_until_next_hour():
    now = datetime.now()
    next_hour = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
    sleep_seconds = (next_hour - now).total_seconds()
    print(f"Sleeping {sleep_seconds:.0f} seconds until {next_hour}")
    time.sleep(sleep_seconds)

def log_data(wCount: int):
    logs_dir = "/home/kevin/Desktop/pi-monitor/public/logs/"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    curr_time = datetime.now()
    date_str = curr_time.strftime('%Y-%m-%d')
    time_str = curr_time.strftime('%H:%M')
    
    log_file_path = os.path.join(logs_dir, f"{date_str}.csv")
    line = f"{time_str}, {wCount}\n"
    with open(log_file_path, "a") as f:
        f.write(line)
        
    print(line.strip())  # also print to console for visibility

def main():
    # Path to chromium-browser and chromedriver on Raspberry Pi
    chromium_path = "/usr/bin/chromium-browser"
    chromedriver_path = "/usr/bin/chromedriver"  # installed via apt

    # Setup Chrome options for Raspberry Pi
    options = webdriver.ChromeOptions()
    options.binary_location = chromium_path
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment if you want background mode

    # Use the system chromedriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    try:
        # Open Google
        driver.get("https://www.google.com")
        page_load_wait = 15
        time.sleep(page_load_wait)  # wait for page to load
        for remaining in range(page_load_wait, 0, -1):
            print(f"loading: {remaining} ", end="\r", flush=True)

        # Find the ENTER button by its CSS class and click it
        enter_button = driver.find_element(By.CSS_SELECTOR, "button.button.btn.btn-red.agree")
        enter_button.click()

        time.sleep(5)  # wait to see the effect of the click
        # Wait for and click the Sign-In button in the nav bar
        sign_in_btn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "button.signin"))
        )
        sign_in_btn.click()

        # Wait for the login form popup to appear
        page_load_wait = 15
        time.sleep(page_load_wait)  # wait for page to load
        for remaining in range(page_load_wait, 0, -1):
            print(f"Opening form in : {remaining} ", end="\r", flush=True)
        #
        # # Fill in username and password
        username_field = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "form#login-form input.username"))
        )

        # Send username text
        # username_field.clear()
        password_field = driver.find_element(By.CSS_SELECTOR, "form#login-form input.password")
        #
        username_field.send_keys("USERNAME")  # replace with actual username
        time.sleep(5)
        password_field.send_keys("PASSWORD")  # replace with actual password
        time.sleep(5)
        # # Click the SIGN-IN button
        sign_in_submit = driver.find_element(By.CSS_SELECTOR, "button.submit")
        sign_in_submit.click()

        page_load_wait = 30
        time.sleep(page_load_wait)  # wait for page to load
        for remaining in range(page_load_wait, 0, -1):
            print(f"logging-in in : {remaining} ", end="\r", flush=True)

        #Open next page
        driver.get("https://gmail.com")

        page_load_wait = 20
        time.sleep(page_load_wait)  # wait for page to load
        for remaining in range(page_load_wait, 0, -1):
            print(f"New page in : {remaining} ", end="\r", flush=True)

        wButton = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "button"))
        )
        time.sleep(10)

        wButton.click()
        time.sleep(10)

        # --- wait for counter to appear ---
        counter_span = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "div.w-counter span.value"))
        )
         
        # Get the counter value as an integer
        wCount = int(counter_span.text)
        log_data(wCount)
    
    except:
        main()
        
        

    finally:
        driver.quit()


if __name__ == "__main__":
    while True:
        main()
        sleep_until_next_hour()
