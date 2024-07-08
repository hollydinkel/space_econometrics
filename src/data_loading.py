import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from utils import *

# Lookup company-specific parameters from dictionary (plotting style, name, filename)
company_keys = './financial_data/company_keys.json'
keys = json.load(open(company_keys))

# Set up plotting parameters outside of for loop.
fig1 = plt.figure(dpi=300)
ax1 = fig1.add_subplot()
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Total Asset Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig1_path = "./images/total_asset_growth_rate.png"

fig2 = plt.figure(dpi=300)
ax2 = fig2.add_subplot()
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Total Liabilities Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig2_path = "./images/total_liabilities_growth_rate.png"

fig3 = plt.figure(dpi=300)
ax3 = fig3.add_subplot()
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.set_xlabel('Year', fontsize=12)
ax3.set_ylabel('Total Equity Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig3_path = "./images/total_equity_growth_rate.png"

fig4, ax4 = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
fig4_path = "./images/acf_test.png"

fig5, ax5 = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
fig5_path = "./images/pacf_test.png"

for i, key in enumerate(keys):
    print("KEY: ", key)
    filename = keys[f"{key}"]["file"]
    data = pd.read_excel(f"./financial_data/{filename}","consolidated")

    start_date = pd.to_datetime(keys[f"{key}"]["start_date"])
    end_date = pd.to_datetime(keys[f"{key}"]["end_date"])
    data['Quarter'] = pd.to_datetime(data['Quarter'])

    filtered_data = data[data['Quarter'].between(start_date, end_date)]
    
    totalAssets = filtered_data["Total Assets"].values
    totalLiabilities = filtered_data["Total Liabilities"].values
    totalEquity = filtered_data["Total Equity"].values

    # Transformed data
    transformed_data = {"totalAssets": totalAssets,
                        "totalLiabilities": totalLiabilities,
                        "totalEquity": totalEquity,
                        "diffAssets": np.diff(totalAssets),
                        "diffLiabilities": np.diff(totalLiabilities),
                        "diffEquity": np.diff(totalEquity),
                        "diff2Assets": np.diff(np.diff(totalAssets)),
                        "diff2Liabilities": np.diff(np.diff(totalLiabilities)),
                        "diff2Equity": np.diff(np.diff(totalEquity)),
                        "lnAssets": np.log(totalAssets),
                        "lnLiabilities": np.log(totalLiabilities),
                        "lnEquity": np.log(totalEquity),
                        "growthAssets": (np.diff(totalAssets)/totalAssets[1:])*100,
                        "growthLiabilities": (np.diff(totalLiabilities)/totalLiabilities[1:])*100,
                        "growthEquity": (np.diff(totalEquity)/totalEquity[1:])*100,
                        }

    if key == "synspective" or key == "satellogic":
        print("Not enough revenue data")
    else:
        revenue = filtered_data["Revenue"].values
        transformed_data["Revenue"] = revenue
        transformed_data["lnRevenue"] = np.log(revenue)
        transformed_data["diffRevenue"] = np.diff(revenue)
        transformed_data["diff2Revenue"] = np.diff(np.diff(revenue))
        transformed_data["growthRevenue"] = (np.diff(revenue)/revenue[1:])*100

    # ADF unit root test for stationarity
    stationary_vars = []
    nonstationary_vars = []
    error_list = []
    for idx, dtype in enumerate(transformed_data):
        try:
            stationarity = adf_test(transformed_data[dtype], dtype)
            if stationarity:
                stationary_vars.append(dtype)
            else:
                nonstationary_vars.append(dtype)
        except:
            error_list.append(dtype)
            # print("Error in testing for stationarity, ", f"{dtype}: ", transformed_data[dtype])
    print("Stationary variables: ", stationary_vars)
    print("Nonstationary variables: ", nonstationary_vars)
    print("Error testing for stationarity: ", error_list)

    if key == "planet":
        date_range = filtered_data["Quarter"][1:]
        frame = np.column_stack((transformed_data["diffRevenue"], transformed_data["diffAssets"], transformed_data["diffEquity"]))
    elif key == "synspective":
        date_range = filtered_data["Quarter"][1:]
        frame = np.column_stack((transformed_data['diffAssets'],transformed_data['diffEquity'],transformed_data['diffLiabilities']))
    elif key == "iQPS":
        # date_range = filtered_data["Quarter"][1:]
        # frame = np.column_stack((transformed_data["lnAssets"], transformed_data["lnEquity"], transformed_data["lnLiabilities"]))
        date_range = filtered_data["Quarter"][2:]
        frame = np.column_stack((transformed_data["diff2Assets"], transformed_data["diff2Liabilities"], transformed_data["diff2Equity"]))
        # # why won't this work?
        # date_range = filtered_data["Quarter"][:].values
        # frame = np.column_stack((transformed_data["totalAssets"], transformed_data["totalEquity"], transformed_data["totalLiabilities"]))
        print(date_range, frame)
    elif key == "satellogic":
        date_range = filtered_data["Quarter"][:]
        frame = np.column_stack((transformed_data["totalAssets"], transformed_data["totalEquity"], transformed_data["totalLiabilities"]))

    try:
        vecm = johansen_vecm(date_range, frame)
        print("VECM Summary: ", vecm.summary())
        print("Gamma: ", vecm.gamma)
        print("Alpha: ", vecm.alpha)
        print("Beta: ", vecm.beta)
        print("Var_rep: ", vecm.var_rep)
    except:
        print(f"skipping {key} vecm")
    
    logAssets = np.diff(transformed_data["lnAssets"])
    logLiabilities = np.diff(transformed_data["lnLiabilities"])
    logEquity = np.diff(transformed_data["lnEquity"])

    companyColor = np.asarray(keys[key]["color"])/255
    ax1.plot(filtered_data["Quarter"].values[1:], transformed_data["growthAssets"], color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    ax2.plot(filtered_data["Quarter"].values[1:], transformed_data["growthLiabilities"], color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    ax3.plot(filtered_data["Quarter"].values[1:], transformed_data["growthEquity"], color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    plot_acf(logAssets, lags=3, title=key, ax = ax4[i//2, i%2], color = 'red')
    plot_pacf(logAssets, lags=2, title=key, ax = ax5[i//2, i%2], color = 'red')

plt.rcParams['legend.title_fontsize'] = '12'

fig1.tight_layout()
box1 = ax1.get_position()
ax1.set_position([box1.x0, box1.y0 + box1.height * 0.2,
                 box1.width, box1.height * 0.8])
ax1.legend(ncol=4, bbox_to_anchor=(1, -0.15),
          fancybox=True, title=legendTitle, fontsize='12', frameon=True)
fig1.savefig(f"{fig1_path}")

fig2.tight_layout()
box2 = ax2.get_position()
ax2.set_position([box2.x0, box2.y0 + box2.height * 0.2,
                 box2.width, box2.height * 0.8])
ax2.legend(ncol=4, bbox_to_anchor=(1, -0.15),
          fancybox=True, title=legendTitle, fontsize='12', frameon=True)
fig2.savefig(f"{fig2_path}")

fig3.tight_layout()
box3 = ax3.get_position()
ax3.set_position([box3.x0, box3.y0 + box3.height * 0.2,
                 box3.width, box3.height * 0.8])
ax3.legend(ncol=4, bbox_to_anchor=(1, -0.15),
          fancybox=True, title=legendTitle, fontsize='12', frameon=True)
ax3.text(0.65, 0.96, 'SATL moves to U.S.A.', weight='bold', transform=ax3.transAxes)
fig3.savefig(f"{fig3_path}")

fig4.tight_layout()
fig4.savefig(f"{fig4_path}")

fig5.tight_layout()
fig5.savefig(f"{fig5_path}")