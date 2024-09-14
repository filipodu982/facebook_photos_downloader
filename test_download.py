from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import sys
import time
import urllib.request
import os


def open_chat_options(driver):
    """
    Locate and click the chat options button to access shared media and files.
    """
    try:
        # Find the options button (gear icon or three dots)
        options_button = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Informacje o konwersacji"]'
        )

        # Click the options button to open the menu
        options_button.click()
        time.sleep(1)  # Wait for the menu to appear

    except Exception as e:
        print(f"Failed to find or click the options button: {e}")


def open_multimedia_button(driver):
    """
    Locate and click multimedia, files and links option button after options button
    """
    try:
        multimedia_button = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Multimedia, pliki i linki"]'
        )
        multimedia_button.click()
        time.sleep(1)
    except Exception as e:
        print(f"Failed to find or click the multimedia button: {e}")
        open_chat_options(driver)
        open_multimedia_button(driver)


def open_multimedia(driver):
    """
    Locate and click the final multimedia button to access shared photos and videos.
    """
    try:
        # Find the 'Multimedia' tab/button
        media_files_button = driver.find_element(
            By.XPATH, "//span[text()='Multimedia']"
        )

        # Click the button to open the media view
        media_files_button.click()
        time.sleep(2)  # Wait for the media/files view to load
    except Exception as e:
        print(f"Failed to find or click the 'Media, Files and Links' option: {e}")
        open_multimedia_button(driver)
        open_multimedia(driver)


def open_first_photo(driver):
    """
    Locate first photo on the list of multimedia and click it
    """
    try:
        # Find the first photo in the fallery
        image_button = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Otwórz zdjęcie"]'
        )

        # Click the image
        image_button.click()
        time.sleep(1)  # Wait for the image to appear

    except Exception as e:
        print(f"Failed to find or click the options button: {e}")


def download_opened_image(driver, file_number):
    """
    Locate download button in the image, find underlying link and download the photo
    """
    try:
        # Find the download button
        download_button = driver.find_element(
            By.CSS_SELECTOR, 'a[aria-label="Pobierz"]'
        )

        image_url = download_button.get_attribute("href")
        download_image(image_url, file_number=file_number)
        time.sleep(1)

    except Exception as e:
        print(f"Failed to find or click the options button: {e}")


def download_image(url, file_number, folder_path="downloaded_imagesheheh"):
    """
    Download the image from the given URL and save it.
    """
    import requests
    from urllib.parse import urlsplit
    import os

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the image content
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the image file name from the URL
        filename = os.path.basename(urlsplit(url).path).split(".")
        filename = f"{file_number}.{filename[-1]}"
        # filename = os.path.basename(file_number)
        # Create the full file path
        file_path = os.path.join(folder_path, filename)

        # Save the image
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {url}")


chrome_profile_path = (
    r"user-data-dir=C:\Users\Filip\AppData\Local\Google\Chrome\User Data"
)
profile_directory = r"profile-directory=Profile 1"

options = webdriver.ChromeOptions()
options.add_argument(chrome_profile_path)
options.add_argument(profile_directory)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-pipe")

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=options)

group_chat_url = "https://www.facebook.com/messages/t/8547827728584318"
time.sleep(1)
# Log in to Facebook
driver.get(group_chat_url)
time.sleep(3)  # Let the chat load
input("Check if the correct profile is loaded. Press Enter to continue...")

open_chat_options(driver)
open_multimedia_button(driver)
open_multimedia(driver)
open_first_photo(driver)
x = 0
while True:
    x += 1
    try:
        download_opened_image(driver, str(x))
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)
        time.sleep(1)
    except KeyboardInterrupt:
        driver.quit()
        sys.exit
