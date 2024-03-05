import pandas as pd
import numpy as np
import json

# filename = './data/boeing_practice.csv'
# df = pd.read_excel('path/to/sheet.xlsx', 'sheet_name')
company_keys = './company_keys.json'
filename = './financial_data/planet_compiled.xlsx'
sheet_name = 'income' # 'income' or 'consolidated'

keys = json.load(open(company_keys))
print(keys["planet"]["sheet"])
mydata = pd.read_excel(f'./financial_data/{keys["planet"]["file"]}', keys["planet"]["sheet"])
print(mydata)
