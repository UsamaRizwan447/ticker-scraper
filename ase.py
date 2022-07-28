from lib2to3.pytree import type_repr
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import xlsxwriter
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
tickers = []
for tick in data.values:
    tickers.append(tick[0])


r1 = [['Assets', '', ''], ['Non-current assets', '', ''], ['Property, plant and equipment', '4,280,053', '4,502,135'], ['Projects in progress', '421,989', '181,950'], ['Investment property', '265,747', '265,747'], ['Investments in subsidiaries, joint ventures and associates', '39,176', '39,176'], ['Intangible assets', '', ''], ['Financial assets at fair value through other comprehensive income', '252,035', '215,402'], ['Financial assets at amortized cost', '', ''], ['Deferred tax assets', '', ''], ['Long term loans receivable', '', ''], ['Employee loans ,long term', '', ''], ['Restricted bank balances', '', ''], ['Trade and other non-current receivables', '', ''], ['Non-current derivative financial assets', '', ''], ['Non-current receivables due from related parties', '', ''], ['Other non-current assets', '', ''], ['Total non-current assets', '5,259,000', '5,204,410']]
r2 = [['Assets', '2', '42432'], ['Property, plant and equipment', '1,537,495', '2,028,762'], ['Accounts receivable', '397,397', '1,045,373'], ['Current receivables due from related parties', '', ''], ['Inventories', '3,656,451', '2,614,141'], ['Spare parts and supplies', '621,513', '786,767'], ['Employee loans short term', '', ''], ['Financial assets at fair value through profit or loss', '', ''], ['Current derivative financial assets', '', ''], ['Current tax assets, current', '', ''], ['Loans receivable', '', ''], ['Other current assets', '3,660,216', '2,553,855'], ['Assets held for sale', '', ''], ['Total current assets', '9,873,072', '9,028,898'], ['Total assets', '15,132,072', '14,233,308'], ['Equity and liabilities', '', ''], ['Equity', '', ''], ['Paid-up capital', '6,750,000', '6,750,000'], ['Additional paid-in capital', '', ''], ['Retained earnings', '1,197,501', '356,097']]
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

    for tickerNumber, tick in enumerate(tickers):
        #base row number for current ticker in sheet
        base_row = tickerNumber * slack_for_cols + header_slack_for_rows

        # To make 2 rows for each tickers in order to store records of 2021 and 2022
        output_file.write_column(base_row, 0, [tickers[tickerNumber], tickers[tickerNumber]])
        output_file.write_column(base_row, 1, ["2021", "2022"]) 
        for data in r1:
            try:
                column_number = titles.index(data[0])
            except:
                column_number = len(titles)
                titles.append(data[0])
            column_number += slack_for_cols
            output_file.write_column(title_row, column_number, [data[0]])
            output_file.write_column(base_row, column_number, [data[1], data[2]])
            tickers_sheet.write(tickerNumber+header_slack_for_rows,0, tickers[tickerNumber])
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

elements = driver.find_elements(By.XPATH, '//a[@ng-click="GetTaxonomyData(row)"]')
for element in elements:
    if report_types[0].strip() == element.text.strip():
        driver.implicitly_wait(3)
        """Scrap data here"""
        break

driver.get(reports_url)
elements = driver.find_elements(By.XPATH, '//a[@ng-click="GetTaxonomyData(row)"]')
for element in elements:
    if report_types[1].strip() == element.text.strip():
        driver.implicitly_wait(3)
        """Scrap data here"""
        break

driver.get(reports_url)
elements = driver.find_elements(By.XPATH, '//a[@ng-click="GetTaxonomyData(row)"]')
for element in elements:
    if report_types[2].strip() == element.text.strip():
        driver.implicitly_wait(3)
        """Scrap data here"""
        break

driver.get(reports_url)
elements = driver.find_elements(By.XPATH, '//a[@ng-click="GetTaxonomyData(row)"]')
for element in elements:
    if report_types[3].strip() == element.text.strip():
        driver.implicitly_wait(3)
        """Scrap data here"""
        break

driver.get(reports_url)
elements = driver.find_elements(By.XPATH, '//a[@ng-click="GetTaxonomyData(row)"]')
for element in elements:
    if report_types[4].strip() == element.text.strip():
        driver.implicitly_wait(3)
        print("Pressed 5")
        """Scrap data here"""
        break
print("Exited 5")

# This gets us all of the reports and we iterate through them and open the ones we need

driver.close()
