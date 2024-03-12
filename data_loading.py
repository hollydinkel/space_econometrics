import pandas_datareader as pdr
import pandas as pd
import numpy as np
import json

# df = pd.read_excel('path/to/sheet.xlsx', 'sheet_name')
#company_keys = './company_keys.json'
#filename = './financial_data/planet_compiled.xlsx'
filename = './financial_data/iQPS.xlsx'
sheet_name = 'income' # 'income' or 'consolidated'

#keys = json.load(open(company_keys))
#print(keys["planet"]["sheet"])
mydata = pd.read_excel(filename,sheet_name)
print(mydata["Current Assets"])
