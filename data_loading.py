import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# df = pd.read_excel('path/to/sheet.xlsx', 'sheet_name')
#company_keys = './company_keys.json'
#filename = './financial_data/planet_compiled.xlsx'
filename1 = './financial_data/iQPS.xlsx'
filename2 = './financial_data/synspective.xlsx'
filename3 = './financial_data/planet.xlsx'
sheet_name = 'income' # 'income' or 'consolidated'

#keys = json.load(open(company_keys))
#print(keys["planet"]["sheet"])
iQPS_data = pd.read_excel(filename1,sheet_name)
iQPS_total_assets = iQPS_data["Total Assets"]
synspective_data = pd.read_excel(filename2,sheet_name)
synspective_total_assets = synspective_data["Total Assets"]
planet_data = pd.read_excel(filename3,"consolidated")
planet_total_assets = planet_data["Total assets"]
print(planet_total_assets)

logAssets_iQPS = np.log(iQPS_total_assets)
logAssets_synspective = np.log(synspective_total_assets)
logAssets_planet = np.log(planet_total_assets)
print(logAssets_planet)

logs_iQPS = []
divs_iQPS = []
logs_synspective = []
divs_synspective = []
logs_planet = []
divs_planet = []
for i in range(1, len(logAssets_iQPS)):
    logs_iQPS.append(logAssets_iQPS[i] - logAssets_iQPS[i-1])
    divs_iQPS.append((iQPS_total_assets[i]/iQPS_total_assets[i-1]) - 1)
for i in range(1, len(logAssets_synspective)):
    logs_synspective.append(logAssets_synspective[i] - logAssets_synspective[i-1])
    divs_synspective.append(synspective_total_assets[i]/synspective_total_assets[i-1] - 1)
for i in range(1, len(logAssets_planet)):
    logs_planet.append(logAssets_planet[i]-logAssets_planet[i-1])
    divs_planet.append((planet_total_assets[i]/planet_total_assets[i-1])-1)

plt.plot(iQPS_data["Quarter"][1:], logs_iQPS, synspective_data["Quarter"][1:], logs_synspective, planet_data["Quarter"][1:], logs_planet)
plt.savefig("./images/logs.png")
plt.plot(iQPS_data["Quarter"][1:], divs_iQPS, synspective_data["Quarter"][1:], divs_synspective, planet_data["Quarter"][1:], divs_planet)
plt.savefig("./images/divs.png")