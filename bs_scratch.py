# Code to scrap page of "Income Statement"
import re

from bs4 import BeautifulSoup

with open('sample_report_html/statement_of_cash_flows_indirect_method.html', 'r') as contents:
    soup = BeautifulSoup(contents, 'html.parser')

table_rows = []
for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
    first_column = element.find('a')
    other_columns = element.find_all('label')
    strings = []
    if first_column is not None:
        strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
        for element in other_columns:
            strings.append(element.string.strip('\n').strip())
        if len(strings) < 3:
            while len(strings) != 3:
                strings.append("")
        table_rows.append(strings)

if len(table_rows) > 0:
    del table_rows[0]

print(table_rows)









# # Code to scrap page of "Income Statement"
# import re

# from bs4 import BeautifulSoup

# with open('sample_report_html/income_statement.html', 'r') as contents:
#     soup = BeautifulSoup(contents, 'html.parser')

# table_rows = []
# for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
#     first_column = element.find('a')
#     other_columns = element.find_all('label')
#     strings = []
#     strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip()))
#     for element in other_columns:
#         strings.append(element.string.strip('\n').strip())
#     if len(strings) < 3:
#         while len(strings) != 3:
#             strings.append("")
#     table_rows.append(strings)

# if len(table_rows) > 0:
#     del table_rows[0]

# print(table_rows)










# Code to scrap page of "Statement of financial position"

# from bs4 import BeautifulSoup

# with open('sample_report_html/statement_of_financial_positions.html', 'r') as contents:
#     soup = BeautifulSoup(contents, 'html.parser')

# table_rows = []
# for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
#     first_column = element.find('a')
#     other_columns = element.find_all('label')
#     strings = []
#     strings.append(first_column.string.strip())
#     for element in other_columns:
#         strings.append(element.string.strip())
#     if len(strings) < 3:
#         while len(strings) != 3:
#             strings.append("")
#     table_rows.append(strings)

# if len(table_rows) > 0:
#     del table_rows[0]

# print(table_rows)
