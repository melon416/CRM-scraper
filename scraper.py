import time
import subprocess
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from pynput import keyboard

def open_chrome_with_profile(chrome_path, chrome_user_data_path, profile_directory):
    chrome_cmd = [
        chrome_path,
        f"--user-data-dir={chrome_user_data_path}",
        f"--profile-directory={profile_directory}",
        "--no-first-run",
        "--no-default-browser-check"
    ]
    chrome_process = subprocess.Popen(chrome_cmd)
    print(f"Chrome opened with process ID: {chrome_process.pid}")
    time.sleep(3)
    return chrome_process

def connect_to_chrome(user_data_dir, profile_directory, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f'--profile-directory={profile_directory}')
    driver = webdriver.Chrome(options=options)
    print("Successfully connected to Chrome!")
    driver.get(url)
    return driver

def wait_for_f_key_press():
    f_pressed = False
    def on_press(key):
        nonlocal f_pressed
        try:
            if key.char.lower() == 'f':
                f_pressed = True
                return False
        except AttributeError:
            pass
    print("Waiting for 'f' key press...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print("'f' key pressed. Starting to scrape data...")
    return True

def scrape_data(driver):
    try:
        data = {
            "Full Name": driver.find_element(By.CSS_SELECTOR, "h1").text,
            "Gender": driver.find_element(By.XPATH, '//*[@id="beneath-top-navbar"]/div/div[1]/div[1]/div[1]/div[1]/div[2]/dl[1]/dd[1]').text,
            "DOB": driver.find_element(By.XPATH, '//*[@id="beneath-top-navbar"]/div/div[1]/div[1]/div[1]/div[1]/div[2]/dl[1]/dd[2]').text,
            "Address": driver.find_element(By.XPATH, '//*[@id="beneath-top-navbar"]/div/div[1]/div[1]/div[2]/dl/dd[3]/span').text,
            "Phone": driver.find_element(By.XPATH, '//*[@id="beneath-top-navbar"]/div/div[1]/div[1]/div[2]/dl/dd[1]/a/span').text,
            "Email": driver.find_element(By.XPATH, '//*[@id="beneath-top-navbar"]/div/div[1]/div[1]/div[2]/dl/dd[2]/a/span').text,
            "URL": driver.find_element(By.XPATH, '//*[@id="id_row_chart_photo-original_image"]/div/a').get_attribute('href')
        }

        print("Scraped Data:")
        for key, value in data.items():
            print(f"{key}: {value}")

        # Save to CSV
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

        print("Data saved to scraped_data.csv")

    except Exception as e:
        print(f"Error during scraping: {str(e)}")

def main():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
    profile_directory = "YOUR CHROME PROFILE NAME"
    url = "YOUR CRM LOGGED IN PATH"

    open_chrome_with_profile(chrome_path, user_data_dir, profile_directory)
    driver = connect_to_chrome(user_data_dir, profile_directory, url)

    if wait_for_f_key_press():
        scrape_data(driver)
        driver.quit()

if __name__ == "__main__":
    main()
