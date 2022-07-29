import re

from bs4 import BeautifulSoup

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

with open('sample_report_html/company_history.html', 'r') as contents:
    print(get_reports_link(contents))

































# # Code to scrap page of "Notes - Subclassifications of assets"
# import re

# from bs4 import BeautifulSoup

# with open('sample_report_html/notes_subclassification_of_assets.html', 'r') as contents:
#     soup = BeautifulSoup(contents, 'html.parser')

# table_rows = []
# tables = soup.find_all('table', attrs={"ng-repeat": "tbl in MultiTableCellCombinationList"})
# for i in range(len(tables)):
#     if i!=3 and i!=4 and i!=len(tables)-2:
#         for element in tables[i].find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
#             first_column = element.find('a')
#             other_columns = element.find_all('label')
#             strings = []
#             if first_column is not None:
#                 strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
#                 for element in other_columns:
#                     if element.string is not None:
#                         strings.append(element.string.strip('\n').strip())
                    
#                 if len(strings) < 3:
#                     while len(strings) != 3:
#                         strings.append("")
#                 table_rows.append(strings)

# if len(table_rows) > 0:
#     del table_rows[0]

# print(table_rows)
















# # Code to scrap page of "Notes - Subclassifications of liabilities and equities"
# import re

# from bs4 import BeautifulSoup

# with open('sample_report_html/notes_subclassification_of_liabilities_and_equities.html', 'r') as contents:
#     soup = BeautifulSoup(contents, 'html.parser')

# table_rows = []
# for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
#     first_column = element.find('a')
#     other_columns = element.find_all('label')
#     strings = []
#     if first_column is not None:
#         strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
#         for element in other_columns:
#             strings.append(element.string.strip('\n').strip())
#         if len(strings) < 3:
#             while len(strings) != 3:
#                 strings.append("")
#         table_rows.append(strings)

# if len(table_rows) > 0:
#     del table_rows[0]

# print(table_rows)












# # Code to scrap page of "Income Statement"
# import re

# from bs4 import BeautifulSoup

# with open('sample_report_html/statement_of_cash_flows_indirect_method.html', 'r') as contents:
#     soup = BeautifulSoup(contents, 'html.parser')

# table_rows = []
# for element in soup.find_all('tr', attrs={"ng-repeat": "row in tbl.RowElementsList track by $index"}):
#     first_column = element.find('a')
#     other_columns = element.find_all('label')
#     strings = []
#     if first_column is not None:
#         strings.append(re.sub(' +', ' ', first_column.string.replace('\n', '').strip().strip(':')))
#         for element in other_columns:
#             strings.append(element.string.strip('\n').strip())
#         if len(strings) < 3:
#             while len(strings) != 3:
#                 strings.append("")
#         table_rows.append(strings)

# if len(table_rows) > 0:
#     del table_rows[0]

# print(table_rows)









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
