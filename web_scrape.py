import os
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Centralize selectors
SELECTORS = {
    "first_button": "#store_inventory_table > div.bootstrap-table > div.fixed-table-container > div.fixed-table-pagination > div.pull-left.pagination-detail > span.page-list > span > button > span.page-size",
    "second_button": "#store_inventory_table > div.bootstrap-table > div.fixed-table-container > div.fixed-table-pagination > div.pull-left.pagination-detail > span.page-list > span > ul > li:nth-child(4) > a",
    "third_button": "#store_inventory_table > div.bootstrap-table > div.fixed-table-toolbar > div.columns.columns-left.btn-group.pull-left > div.export.btn-group > button",
    "fourth_button": "#store_inventory_table > div.bootstrap-table > div.fixed-table-toolbar > div.columns.columns-left.btn-group.pull-left > div.export.btn-group.open > ul > li:nth-child(3) > a",
}


# Function to handle button click
def click_button(wait, selector, max_attempts=3):
    for _ in range(max_attempts):
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            button.click()
            break
        except StaleElementReferenceException:
            continue


webdriver_service = Service(
    "D:\\Users\\nickl\\Downloads\\chromedriver_win32\\chromedriver.exe"
)

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Load webpage
driver.get("https://lcbo.watch/store-inventory/568")

# Wait for the page to load completely
wait = WebDriverWait(driver, 20)

# Click buttons
click_button(wait, SELECTORS["first_button"])
click_button(wait, SELECTORS["second_button"])
click_button(wait, SELECTORS["third_button"])
click_button(wait, SELECTORS["fourth_button"])

# Wait for the download to complete
time.sleep(5)

# Get the download directory and the file downloaded
download_dir = "D:\\Users\\nickl\\Downloads"

# Get the most recently downloaded .csv file
file_name = max(
    [
        os.path.join(download_dir, f)
        for f in os.listdir(download_dir)
        if f.endswith(".csv")
    ],
    key=os.path.getctime,
)

# Destination file path
destination = os.path.join(download_dir, "LCBO_store_inventory.csv")

# Rename the file
if os.path.exists(destination):
    os.remove(destination)
os.rename(file_name, destination)

# Close the browser
driver.quit()
