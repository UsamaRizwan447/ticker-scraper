import re
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import xlsxwriter
# Import webdriver and confirm that driver is compatible with Python
driver = webdriver.Chrome()

# File name of xlsx file containing tickers
file_name = 'sample_output.xlsx' 
df = pd.read_excel(file_name, sheet_name='Ticker')
data = pd.DataFrame(df)

# List of all tickers from .xlsx file
tickers = []
for tick in data.values:
    tickers.append(tick[0])

with xlsxwriter.Workbook(file_name) as workbook:
    output_file = workbook.add_worksheet("Sample Output")
    tickers_sheet = workbook.add_worksheet("Ticker")
    tickers_sheet.write(0, 0, "aseticker")
    output_file.write("A1", "asetickers")
    output_file.write("B1", "years")

    title_row = 0
    header_slack_for_rows = 1
    slack_for_cols = 2
    column_number = 0
    # Maintains all the titles in list, helps to decide whether current value goes as new colum or in an existing column 
    titles = []

    # This loop iterates through the loaded tickers and performs scraping of the needed data
    for tickerNumber, ticker in enumerate(tickers):
        #base row number for current ticker in sheet
        base_row = tickerNumber * slack_for_cols + header_slack_for_rows

        # To make 2 rows for each tickers in order to store records of 2021 and 2022
        output_file.write_column(base_row, 0, [ticker, ticker])
        output_file.write_column(base_row, 1, ["2021", "2022"]) 

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

                    page_content = driver.page_source
                    soup = BeautifulSoup(page_content, 'html.parser')
                    for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
                        first_column = element.find('a')
                        other_columns = element.find_all('label')
                        strings = []
                        strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip()))
                        for element in other_columns:
                            strings.append(element.string.strip())
                        if len(strings) < 3:
                            while len(strings) != 3:
                                strings.append("")
                        statement_of_financial_position.append(strings)
                    if len(statement_of_financial_position) > 0:
                        del statement_of_financial_position[0]
                except:
                    driver.quit()
                break

        driver.get(reports_url)
        WebDriverWait(driver, 5)
        driver.find_element(By.XPATH, rendering_platform_body_xpath)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            from pdb import set_trace; set_trace();
            if report_types[1].strip() == element.text.strip():
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()

                    page_content = driver.page_source
                    soup = BeautifulSoup(page_content, 'html.parser')
                    for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
                        first_column = element.find('a')
                        other_columns = element.find_all('label')
                        strings = []
                        strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip()))
                        for element in other_columns:
                            strings.append(element.string.strip())
                        if len(strings) < 3:
                            while len(strings) != 3:
                                strings.append("")
                        income_statement.append(strings)
                    if len(income_statement) > 0:
                        del income_statement[0]

                    from pdb import set_trace; set_trace();
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

        for data in table_values:
            try:
                column_number = titles.index(data[0])
            except:
                column_number = len(titles)
                titles.append(data[0])
            column_number += slack_for_cols
            output_file.write_column(title_row, column_number, [data[0]])
            output_file.write_column(base_row, column_number, [data[1], data[2]])
        tickers_sheet.write(tickerNumber+header_slack_for_rows,0, ticker)

driver.close()
