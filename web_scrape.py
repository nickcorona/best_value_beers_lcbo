from selenium import webdriver
import pandas as pd

# Use the path to your chromedriver as the argument
driver = webdriver.Chrome("D:\\Users\\nickl\\Downloads\\chromedriver_win32\\chromedriver.exe")

# Open the page
driver.get('https://lcbo.watch/store-inventory/568')

# Selenium waits for the page to load
driver.implicitly_wait(10)

# Find the table
table = driver.find_element_by_xpath('//table')

# Get table headers
headers = [header.text for header in table.find_elements_by_xpath('.//th')]

# Get table rows
rows = table.find_elements_by_xpath('.//tr')

data = []
for row in rows[1:]:  # Exclude header
    cols = row.find_elements_by_xpath('.//td')
    cols = [ele.text for ele in cols]
    data.append(cols)

df = pd.DataFrame(data, columns=headers)

print(df)

# Close the browser
driver.quit()
