from bdb import set_trace
import re
from xml.dom.minidom import Document
from attr import attr
import pandas as pd
import time
import xlsxwriter

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import webdriver and confirm that driver is compatible with Python
driver = webdriver.Chrome()

# File name of xlsx file containing tickers
file_name = 'input_output.xlsx' 
df = pd.read_excel(file_name, sheet_name='Ticker')
data = pd.DataFrame(df)

# List of all tickers from .xlsx file
tickers = [ticker[0] for ticker in data.values]

tickers = ['ABUS']

def get_reports_link(contents):
    soup = BeautifulSoup(contents, 'html.parser')
    table_rows = soup.find('tbody').find_all("tr")

    reports_link = ''
    for row in table_rows:
        html_link = row.find("a")
        if html_link is not None:
            if 'xbrljordan' in html_link['href']:
                reports_link = html_link['href']
                break

    return reports_link

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

with xlsxwriter.Workbook(file_name) as workbook:
    output_file = workbook.add_worksheet("Data")
    output_file.write("A1", "asetickers")
    output_file.write("B1", "years")

    # Saving tickers before scraping so they might not get lost in case of miss flow in code.
    tickers_sheet = workbook.add_worksheet("Ticker")
    tickers_sheet.write(0, 0, "aseticker")
    for ticker_num in range(len(tickers)):
        tickers_sheet.write(ticker_num+1,0, tickers[ticker_num])

    # Some variables to help build a generic logic for data writing in file.
    title_row = 0
    header_slack_for_rows = 1
    slack_for_cols = 2
    column_number = 0

    # Maintains all the titles in list, helps to decide whether current value goes as new colum or in an existing column 
    titles = []

    # This loop iterates through the loaded tickers and performs scraping of the needed data
    for tickerNumber, ticker in enumerate(tickers):
        # Base row number for current ticker in sheet
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
        driver.get(get_reports_link(driver.page_source))

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

        time.sleep(5)
        WebDriverWait(driver, 5)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            if report_types[0].strip() == element.text.strip():
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()
                    time.sleep(3)

                    statement_of_financial_position = table_parser(driver.page_source)
                except:
                    driver.quit()
                break

        driver.get(reports_url)
        time.sleep(5)
        WebDriverWait(driver, 5)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            if report_types[1].strip() == element.text.strip():
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()
                    time.sleep(3)

                    income_statement = table_parser(driver.page_source)
                except:
                    driver.quit()
                break

        driver.get(reports_url)
        time.sleep(5)
        WebDriverWait(driver, 5)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            if report_types[2].strip() == element.text.strip():
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()
                    time.sleep(3)

                    statement_of_cash_flows_indirect_method = table_parser(driver.page_source)
                except:
                    driver.quit()
                break

        driver.get(reports_url)
        time.sleep(5)
        WebDriverWait(driver, 5)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            if report_types[3].strip() == element.text.strip():
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()
                    time.sleep(3)

                    table_rows = []
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
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
        time.sleep(5)
        WebDriverWait(driver, 5)
        elements = driver.find_elements(By.XPATH, reports_row_xpath)
        for element in elements:
            if report_types[4].strip() == element.text.strip():
                try:
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rendering_platform_body_xpath)))
                    element.click()
                    time.sleep(3)

                    notes_subclassifications_of_liabilities_and_equities = table_parser(driver.page_source)
                except:
                    driver.quit()
                break

        table_values = statement_of_financial_position + income_statement + statement_of_cash_flows_indirect_method \
                        + notes_subclassifications_of_assets + notes_subclassifications_of_liabilities_and_equities

        for data in table_values:
            try:
                column_number = titles.index(data[0])
            except:
                column_number = len(titles)
                titles.append(data[0])
            column_number += slack_for_cols
            output_file.write_column(title_row, column_number, [data[0]])
            output_file.write_column(base_row, column_number, [data[1], data[2]])

driver.close()
