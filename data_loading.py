import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# Store company-specific parameters (plotting style, name, filename)
# in a json dictionary for later lookup
company_keys = './company_keys.json'
sheet_name = 'income'

keys = json.load(open(company_keys))

# Set up plotting parameters outside of for loop.
fig = plt.figure()
ax = fig.add_subplot()
ax.tick_params(axis='both', which='major', labelsize=12)
legendTitle = "Company"

for i, key in enumerate(keys):
    filename = keys[f"{key}"]["file"]
    # TODO: fix data column names so capitalization convention
    # is consistent across data sheets. This will eliminate the need 
    # for the below if-else statement.
    if key == "planet":
        data = pd.read_excel(f"./financial_data/{filename}","consolidated")
        totalAssets = data["Total current assets"]
    else:
        data = pd.read_excel(f"./financial_data/{filename}","income")
        totalAssets = data["Total Assets"]

    logAssets = np.log(totalAssets)

    logs = []
    divs = []
    for i in range(1, len(logAssets)):
        logs.append(logAssets[i] - logAssets[i-1])
        divs.append((totalAssets[i]/totalAssets[i-1]) - 1)

    companyColor = np.asarray(keys[key]["color"])/255
    ax.plot(data["Quarter"][1:], logs, color=companyColor, linestyle=keys[key]["style"], label=key)

ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Total Asset Growth Rate (%)', fontsize=12)
fig.tight_layout()
plt.rcParams['legend.title_fontsize'] = '12' 
ax.legend(loc='upper right', title=legendTitle, fontsize='12', frameon=True)
plt.savefig("./images/total_asset_growth_rate_logs.png")