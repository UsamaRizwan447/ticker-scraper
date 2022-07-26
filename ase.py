from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Import webdriver and confirm that driver is compatible with Python
driver = webdriver.Chrome()

# TODO: replace this ticker with a for loop iterator
ticker = "AALU"

import pandas as pd

# File name of xlsx file containing tickers
file_name = 'sample_output.xlsx' 
df = pd.read_excel(file_name, sheet_name='Ticker')
data = pd.DataFrame(df)

# List of all tickers from .xlsx file
tickers = [];
for tick in data.values:
    tickers.append(tick[0])


# The main url for the company history page which will be used
main_url = f"https://www.ase.com.jo/en/company_historical/{ticker}"

driver.get(main_url)

# Find the Disclosure tab from navbar and click
element = driver.find_elements(By.XPATH, "//ul[@class='tabs--primary nav nav-tabs']//a")[2]
element.click()

# Find the "Annual Financial Report" and open it
elements = driver.find_elements(By.XPATH, "//tr[td/@headers='view-name-table-column' and td/@headers='view-filename-html-table-column']")
for element in elements:
    if "Annual Financial Report" in element.text:
        element.find_element(By.XPATH, "//td[@headers='view-filename-html-table-column']").click()

driver.close()
