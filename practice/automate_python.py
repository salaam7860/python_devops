import openpyxl

inventory_file = openpyxl.load_workbook("inventory.xlsx")

product_list = inventory_file["Sheet1"]