import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import webdriver and confirm that driver is compatible with Python
driver = webdriver.Chrome()

# File name of xlsx file containing tickers
file_name = 'sample_output.xlsx' 
df = pd.read_excel(file_name, sheet_name='Ticker')
data = pd.DataFrame(df)

# Maybe commented when local development
# List of all tickers from .xlsx file
tickers = []
for tick in data.values:
    tickers.append(tick[0])

# Maybe uncomment for local debugging
# tickers = ["AALU"]

# This loop iterates through the loaded tickers and performs scraping of the needed data
for ticker in tickers:
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
            break

    # Reports page URL
    reports_url = driver.current_url

    # Report that we need the data from
    report_types = [ "Statement of financial position",
                    "Income statement",
                    "Statement of cash flows, indirect method",
                    "Notes - Subclassifications of assets",
                    "Notes - Subclassifications of liabilities and equities"
                    ]

    reports_row_xpath = '//a[@ng-click="GetTaxonomyData(row)"]'
    rendering_platform_body_xpath = "//div[@class='main-header']"

    def page_load_by_element(element_xpath, timeout=30):
        element_present = EC.presence_of_element_located((By.XPATH, element_xpath))
        WebDriverWait(driver, timeout).until(element_present)
        return True

    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[0].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()
                """Scrap data here"""
            except:
                driver.quit()
            break

    driver.get(reports_url)
    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[1].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()
                """Scrap data here"""
            except:
                driver.quit()
            break

    driver.get(reports_url)
    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[2].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()
                """Scrap data here"""
            except:
                driver.quit()
            break

    driver.get(reports_url)
    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[3].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()
                """Scrap data here"""
            except:
                driver.quit()
            break

    driver.get(reports_url)
    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[4].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()
                """Scrap data here"""
            except:
                driver.quit()
            break

driver.close()
