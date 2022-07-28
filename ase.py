import re
import pandas as pd

from bs4 import BeautifulSoup
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

# This is the common parser for most of the tables
def table_parser(contents):
    list_of_lists = []

    soup = BeautifulSoup(contents, 'html.parser')
    for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
        first_column = element.find('a')
        other_columns = element.find_all('label')
        strings = []
        if first_column is not None:
            strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
            for element in other_columns:
                strings.append(element.string.strip())
            if len(strings) < 3:
                while len(strings) != 3:
                    strings.append("")
            list_of_lists.append(strings)
    if len(list_of_lists) > 0:
        del list_of_lists[0]
    
    return list_of_lists

import pandas as pd

# File name of xlsx file containing tickers
file_name = 'sample_output.xlsx' 
df = pd.read_excel(file_name, sheet_name='Ticker')
data = pd.DataFrame(df)

# List of all tickers from .xlsx file
tickers = [];
for tick in data.values:
    tickers.append(tick[0])


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

    # The following block of variables is to store data about a ticker for its iteration
    statement_of_financial_position = []
    income_statement = []
    statement_of_cash_flows_indirect_method = []
    notes_subclassifications_of_assets = []
    notes_subclassifications_of_liabilities_and_equities = []

    WebDriverWait(driver, 5)
    driver.find_element(By.XPATH, rendering_platform_body_xpath)
    elements = driver.find_elements(By.XPATH, reports_row_xpath)
    for element in elements:
        if report_types[0].strip() == element.text.strip():
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                element.click()

                statement_of_financial_position = table_parser(driver.page_source)
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

                income_statement = table_parser(driver.page_source)
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

                statement_of_cash_flows_indirect_method = table_parser(driver.page_source)
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

                table_rows = []
                tables = soup.find_all('table', attrs={"ng-repeat": "tbl in MultiTableCellCombinationList"})
                for i in range(len(tables)):
                    if i!=3 and i!=4 and i!=len(tables)-2:
                        for element in tables[i].find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
                            first_column = element.find('a')
                            other_columns = element.find_all('label')
                            strings = []
                            if first_column is not None:
                                strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
                                for element in other_columns:
                                    if element.string is not None:
                                        strings.append(element.string.strip('\n').strip())
                                    
                                if len(strings) < 3:
                                    while len(strings) != 3:
                                        strings.append("")
                                notes_subclassifications_of_assets.append(strings)
                        if len(notes_subclassifications_of_assets) > 0:
                            del notes_subclassifications_of_assets[0]

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

                notes_subclassifications_of_liabilities_and_equities = table_parser(driver.page_source)
            except:
                driver.quit()
            break

    tabel_values = statement_of_financial_position + income_statement + statement_of_cash_flows_indirect_method \
                    + notes_subclassifications_of_assets + notes_subclassifications_of_liabilities_and_equities
driver.close()
