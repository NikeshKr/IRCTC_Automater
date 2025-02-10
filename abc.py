import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to login manually and wait for user to press Enter
def manual_login():
    driver.get("https://www.linkedin.com/login")
    input("Please log in to LinkedIn manually and press Enter here once done...")

# Function to search LinkedIn and extract results
def search_linkedin(query):
    driver.get("https://www.linkedin.com/search/results/people/?keywords=" + query)
    profiles = []
    
    while True:
        try:
            # Wait until search results are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results__list"))
            )

            results = driver.find_elements(By.CSS_SELECTOR, "div.search-result__info")
            print(f"Found {len(results)} results on this page")

            for result in results:
                try:
                    name_element = result.find_element(By.CSS_SELECTOR, "span.entity-result__title-text")
                    profile_url = result.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
                    
                    full_name = name_element.text.split()
                    first_name = full_name[0]
                    last_name = full_name[1] if len(full_name) > 1 else ""
                    
                    profiles.append({
                        "First Name": first_name,
                        "Last Name": last_name,
                        "Profile URL": profile_url
                    })
                except Exception as e:
                    print(f"Error processing a result: {e}")
                    continue
            
            # Check for the next button and click it if available
            try:
                next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
                if not next_button.is_enabled():
                    break
                next_button.click()
                time.sleep(2)  # Wait for next page to load
            except Exception as e:
                print(f"No more pages or error finding next button: {e}")
                break
        
        except Exception as e:
            print(f"Error in search results extraction: {e}")
            break
    
    return profiles

# Function to save results to Excel
def save_to_excel(profiles, filename):
    df = pd.DataFrame(profiles)
    df.to_excel(filename, index=False)

def main():
    manual_login()
    
    query = "Data Scientist"
    profiles = search_linkedin(query)
    save_to_excel(profiles, "linkedin_profiles.xlsx")
    
    driver.quit()

if __name__ == "__main__":
    main()
