import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pytesseract
import os

# Function to read credentials from a JSON file
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        credentials = json.load(file)
    return credentials

# Ensure Tesseract-OCR is installed and added to PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Maximize the window
    driver.maximize_window()

    # Open the IRCTC login page
    driver.get("https://www.irctc.co.in/nget/train-search")

    # Wait for the page to load
    time.sleep(random.uniform(3, 5))

    # Click on the login button using the given XPath
    login_button_xpath = '/html/body/app-root/app-home/div[1]/app-header/div[2]/div[2]/div[1]/a[1]'
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, login_button_xpath))
    )
    login_button.click()

    # Wait for the login modal to appear
    time.sleep(random.uniform(2, 4))

    # Read credentials from the JSON file
    credentials = read_credentials('credentials.json')
    username = credentials['username']
    password = credentials['password']
    fromd = credentials['fromd']
    to = credentials['to']
    date = credentials['date']

    

    # Enter username
    username_field_xpath = '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[1]/input'
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, username_field_xpath))
    )
    username_field.send_keys(username)
    time.sleep(random.uniform(1, 2))

    # Enter password
    password_field_xpath = '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[2]/input'
    password_field = driver.find_element(By.XPATH, password_field_xpath)
    password_field.send_keys(password)
    time.sleep(random.uniform(1, 2))

    # Save the captcha image
    captcha_image_xpath = '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[4]/div/app-captcha/div/div/div[2]/span[1]/img'
    captcha_image_element = driver.find_element(By.XPATH, captcha_image_xpath)
    captcha_image_element.screenshot("captcha.png")
    print("Captcha image saved.")

    # Perform OCR on the captcha image
    captcha_text = pytesseract.image_to_string(Image.open("captcha.png"))
    print(f"Captcha text: {captcha_text}")

    # Enter the captcha text
    captcha_input_xpath = '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/div[4]/div/app-captcha/div/div/input'
    captcha_input = driver.find_element(By.XPATH, captcha_input_xpath)
    captcha_input.send_keys(captcha_text.strip())
    print("Captcha text entered.")

    # Submit the login form
    login_submit_xpath = '/html/body/app-root/app-home/div[3]/app-login/p-dialog[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/form/span/button'
    login_submit = driver.find_element(By.XPATH, login_submit_xpath)
    login_submit.click()
    print("Login form submitted.")

    # Wait for the login process to complete
    time.sleep(random.uniform(3, 6))

    # Enter input into the specified element
    input_xpath = '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[1]/div[1]/p-autocomplete/span/input'
    input_element_from = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, input_xpath))
    )
    input_element_from.send_keys(fromd)
    print("Input entered into From")
    time.sleep(random.uniform(1,2))

    # Enter input into the 'to' element
    input_xpath = '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[1]/div[2]/p-autocomplete/span/input'
    input_element_to = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, input_xpath))
    )
    input_element_to.send_keys(to)
    print("Input entered into to")
    time.sleep(random.uniform(1,2))


    # Enter input into the date field
    input_xpath = '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[2]/div[2]/div[1]/p-calendar/span/input'
    input_element_date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, input_xpath))
    )
    input_element_date.clear()
    print("input cleared")
    input_element_date.send_keys(date)
    print("Input entered into date field")

    time.sleep(random.uniform(30, 60))

    # Submit the form
    submit_xpath = '/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[2]/div[1]/app-jp-input/div/form/div[5]/div[1]/button'
    submit = driver.find_element(By.XPATH, submit_xpath)
    submit.click()
    print("form submitted.")

finally:
    # Optionally, close the browser
    driver.quit()
