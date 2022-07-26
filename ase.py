from lib2to3.pytree import type_repr
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Import webdriver and confirm that driver is compatible with Python
driver = webdriver.Chrome()

# TODO: replace this ticker with a for loop iterator
ticker = "AALU"


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
