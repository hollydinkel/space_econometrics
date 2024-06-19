import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import VECM

def adf_test(series):
    result = adfuller(series)
    # print('ADF Statistic:', result[0])
    # print('p-value:', result[1])
    return result[1]

# Store company-specific parameters (plotting style, name, filename)
# in a json dictionary for later lookup
company_keys = './company_keys.json'
sheet_name = 'income'

keys = json.load(open(company_keys))

# Set up plotting parameters outside of for loop.
fig1 = plt.figure()
ax1 = fig1.add_subplot()
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Total Asset Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig1_path = "./images/total_asset_growth_rate.png"

fig2 = plt.figure()
ax2 = fig2.add_subplot()
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Total Liabilities Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig2_path = "./images/total_liabilities_growth_rate.png"

fig3 = plt.figure()
ax3 = fig3.add_subplot()
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.set_xlabel('Year', fontsize=12)
ax3.set_ylabel('Total Equity Growth Rate (%)', fontsize=12)
legendTitle = "Company"
fig3_path = "./images/total_equity_growth_rate.png"

fig4, axs = plt.subplots(2, 2, figsize=(12, 10))
fig4_path = "./images/acf_test.png"

for i, key in enumerate(keys):
    print("KEY: ", key)
    filename = keys[f"{key}"]["file"]
    if (key == "planet" or key == "satellogic"):
        data = pd.read_excel(f"./financial_data/{filename}","consolidated")
    else:
        data = pd.read_excel(f"./financial_data/{filename}","income")
        
    totalAssets = data["Total Assets"]
    totalLiabilities = data["Total Liabilities"]
    totalEquity = data["Total Equity"]

    # Transformed data
    diffAssets = np.diff(totalAssets)
    diffLiabilities = np.diff(totalLiabilities)
    diffEquity = np.diff(totalEquity)
    diff2Assets = np.diff(np.diff(totalAssets))
    diff2Liabilities = np.diff(np.diff(totalLiabilities))
    diff2Equity = np.diff(np.diff(totalEquity))
    lnAssets = np.log(totalAssets)
    lnLiabilities = np.log(totalLiabilities)
    lnEquity = np.log(totalEquity)

    try:
        p_value_Assets = adf_test(totalAssets)
        if p_value_Assets > 0.05:
            print(f'TotalAssets is non-stationary')
            p_value_diffAssets = adf_test(diffAssets)
            if p_value_diffAssets > 0.05:
                print(f'diffTotalAssets is non-stationary')
                p_value_diff2Assets = adf_test(diff2Assets)
                if p_value_diff2Assets > 0.05:
                    print('diff2TotalAssets is non-stationary')
                else:
                    print('diff2TotalAssets is stationary')
            else:
                print('diffTotal Assets is stationary')
        else:
            print('TotalAssets is stationary')
    except:
        print("Error")

    frame = np.column_stack((totalAssets,totalLiabilities))

    try:
        # Perform Johansen cointegration test
        johansen_result = coint_johansen(frame, 0, 1)
        print('Eigenvalues:', johansen_result.eig)
        print('Trace Statistic:', johansen_result.lr1)
        print('Critical Values:', johansen_result.cvt)

        # Determine the optimal lag length
        model = VAR(frame)
        lag_order = model.select_order()
        print(lag_order.summary())

        # Choose an available criterion, e.g., 'aic', 'bic', 'hqic'
        if 'aic' in lag_order.selected_orders:
            chosen_lag = lag_order.selected_orders['aic']
        elif 'bic' in lag_order.selected_orders:
            chosen_lag = lag_order.selected_orders['bic']
        elif 'hqic' in lag_order.selected_orders:
            chosen_lag = lag_order.selected_orders['hqic']
        else:
            raise ValueError("No valid criterion found in the selected orders.")

        print(f'Chosen lag length based on available criterion: {chosen_lag}')

        # coint_rank is number of non-zero eigenvalues minus 1
        vecm = VECM(frame, k_ar_diff=chosen_lag, coint_rank=1)
        vecm_fit = vecm.fit()
    except:
        print(f"skipping {key} vecm")
    # print(vecm_fit.summary())

    logAssets = np.diff(lnAssets)
    logLiabilities = np.diff(lnLiabilities)
    logEquity = np.diff(lnEquity)
    divAssets = []
    divLiabilities = []
    divEquity = []
    for j in range(1, len(lnAssets)):
        divAssets.append(((diffAssets[j-1]/totalAssets[j-1]) - 1)*100)
        divLiabilities.append(((diffLiabilities[j-1]/totalLiabilities[j-1]) - 1)*100)
        divEquity.append(((diffEquity[j-1]/totalEquity[j-1]) - 1)*100)

    companyColor = np.asarray(keys[key]["color"])/255
    ax1.plot(data["Quarter"][1:], divAssets, color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    ax2.plot(data["Quarter"][1:], divLiabilities, color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    ax3.plot(data["Quarter"][1:], divEquity, color=companyColor, linestyle=keys[key]["style"], label=key, linewidth=4)
    plot_acf(logAssets, lags=3, title=key, ax = axs[i//2, i%2], color = 'red')

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