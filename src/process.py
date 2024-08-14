import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from utils import *
from plot_utils import *
pd.options.mode.chained_assignment = None
plt.rcParams['figure.max_open_warning'] = 50

def transformFinancialMetrics(company, filteredData):

    diffAssets = np.diff(filteredData["Total Assets"])
    diffLiabilities = np.diff(filteredData["Total Liabilities"])
    diffEquity = np.diff(filteredData["Total Equity"])

    diff2Assets = np.diff(diffAssets)
    diff2Liabilities = np.diff(diffLiabilities)
    diff2Equity = np.diff(diffEquity)

    lnAssets = np.log(filteredData["Total Assets"])
    lnLiabilities = np.log(filteredData["Total Liabilities"])
    lnEquity = np.log(filteredData["Total Equity"])

    growthAssets = (np.diff(filteredData["Total Assets"]) / filteredData["Total Assets"][1:]) * 100
    growthLiabilities = (np.diff(filteredData["Total Liabilities"]) / filteredData["Total Liabilities"][1:]) * 100
    growthEquity = (np.diff(filteredData["Total Equity"]) / filteredData["Total Equity"][1:]) * 100

    diffLogAssets = np.diff(np.log(filteredData["Total Assets"]))
    diffLogLiabilities = np.diff(np.log(filteredData["Total Liabilities"]))
    diffLogEquity = np.diff(np.log(filteredData["Total Equity"]))

    totalSats = filteredData["Total Launched Satellites"].copy().iloc[-1]
    data = {
        "Quarter": filteredData["Quarter"],
        "totalAssets": filteredData["Total Assets"].values.astype(int),
        "totalLiabilities": filteredData["Total Liabilities"].values.astype(int),
        "totalEquity": filteredData["Total Equity"].values.astype(int),
        "diffAssets": diffAssets,
        "diffLiabilities": diffLiabilities,
        "diffEquity": diffEquity,
        "diff2Assets": diff2Assets,
        "diff2Liabilities": diff2Liabilities,
        "diff2Equity": diff2Equity,
        "lnAssets": lnAssets,
        "lnLiabilities": lnLiabilities,
        "lnEquity": lnEquity,
        "growthAssets": growthAssets,
        "growthLiabilities": growthLiabilities,
        "growthEquity": growthEquity,
        "diffLogAssets": diffLogAssets,
        "diffLogLiabilities": diffLogLiabilities,
        "diffLogEquity": diffLogEquity,
        "totalSatellites": filteredData["Total Launched Satellites"],
        "fractionConstellation": filteredData["Total Launched Satellites"]/totalSats
    }
    if company == "Synspective":
            print("Not enough revenue data")
    else:
        revenue = filteredData["Revenue"].values.astype(int)
        data["Revenue"] = revenue
        data["lnRevenue"] = np.log(revenue)
        data["diffRevenue"] = np.diff(revenue)
        data["diff2Revenue"] = np.diff(np.diff(revenue))
        data["growthRevenue"] = (np.diff(revenue) / revenue[1:]) * 100
        data["financialLeverage"] = data["totalAssets"]/data["totalEquity"]
        data["assetTurnover"] = data["Revenue"]/data["totalAssets"]
        data["netProfitMargin"] = filteredData["Net loss"]/data["Revenue"] 
        data["ROE"] = data["netProfitMargin"]*data["assetTurnover"]*data["financialLeverage"]
        if company == "iQPS":
            # Merge filteredData with exchangeRateData_data based on dates
            merged_data = pd.merge(filteredData, exchangeRateData, left_on='Quarter', right_on='Date', how='left')
            merged_data['Revenue_USD'] = merged_data['Revenue'] / merged_data['Value']
            data["Revenue_USD"] = merged_data['Revenue_USD'].fillna(method='ffill')  # Handle missing values

    return data

# Lookup company-specific parameters from dictionary (plotting style, name, filename)
metadataPath = './financial_data/company_metadata.json'
companyMetadata = json.load(open(metadataPath))
exchangeRatePath = './financial_data/dollar-yen-exchange-rate-history.csv'
exchangeRateData = pd.read_csv(exchangeRatePath, header=None, names=['Date', 'Value'])
exchangeRateData['Date'] = pd.to_datetime(exchangeRateData['Date'])

fig1, ax1 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig1.suptitle("ACF: lnAssets", fontsize=20)
fig2, ax2 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig2.suptitle("PACF: lnAssets", fontsize=20)
fig21, ax21 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig21.suptitle("ACF: lnLiabilities", fontsize=20)
fig22, ax22 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig22.suptitle("PACF: lnLiabilities", fontsize=20)
fig23, ax23 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig23.suptitle("ACF: lnEquity", fontsize=20)
fig24, ax24 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig24.suptitle("PACF: lnEquity", fontsize=20)
fig25, ax25 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig25.suptitle("ACF: diffAssets", fontsize=20)
fig26, ax26 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig26.suptitle("PACF: diffAssets", fontsize=20)
fig27, ax27 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig27.suptitle("ACF: diffLiabilities", fontsize=20)
fig28, ax28 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig28.suptitle("PACF: diffLiabilities", fontsize=20)
fig29, ax29 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig29.suptitle("ACF: diffEquity", fontsize=20)
fig30, ax30 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig30.suptitle("PACF: diffEquity", fontsize=20)
acf_list = [fig1, fig2, fig21, fig22, fig23, fig24, fig25, fig26, fig27, fig28, fig29, fig30]

fig3, ax3 = plt.subplots(figsize=(10, 7), dpi=300)
fig4, ax4 = plt.subplots(figsize=(10, 7), dpi=300)
fig5, ax5 = plt.subplots(figsize=(10, 7), dpi=300)
fig6, ax6 = plt.subplots(figsize=(10, 7), dpi=300)
fig7, ax7 = plt.subplots(figsize=(10, 7), dpi=300)
fig8, ax8 = plt.subplots(figsize=(10, 7), dpi=300)
fig9, ax9 = plt.subplots(figsize=(10, 7), dpi=300)
fig10, ax10 = plt.subplots(figsize=(10, 7), dpi=300)
fig11, ax11 = plt.subplots(figsize=(10, 7), dpi=300)

for i, company in enumerate(companyMetadata):
    print("COMPANY: ", company)

    filename = companyMetadata[f"{company}"]["file"]
    data = pd.read_excel(f"./financial_data/{filename}","consolidated")

    startDate = pd.to_datetime(companyMetadata[f"{company}"]["startDate"])
    endDate = pd.to_datetime(companyMetadata[f"{company}"]["endDate"])
    data['Quarter'] = pd.to_datetime(data['Quarter'])

    filteredData = data[data['Quarter'].between(startDate, endDate)]
    # Convert all columns to type int except time
    colsToConvert = [col for col in filteredData.columns if col and col != 'Quarter']
    filteredData[colsToConvert] = filteredData[colsToConvert].astype(int)

    transformedData = transformFinancialMetrics(company, filteredData)
    stat, nonstat, error = getStationaryVariables(transformedData)
    # print("Stationary: ", stat)
    # print("Nonstationary: ", nonstat)
    if company != "Synspective":
        dateRange = filteredData["Quarter"]
        frame = np.column_stack((transformedData["totalAssets"], transformedData["totalEquity"], transformedData["totalLiabilities"], transformedData["totalSatellites"]))
        ardl_fit = ardl_model(transformedData["Revenue"], frame, 10)

        # Forecast future values
        # In-Sample Prediction: Use the model to predict the underlying data
        forecast = ardl_fit.predict(start=0, end=len(frame) - 1)

    company_color = np.asarray(companyMetadata[company]["color"]) / 255 # normalized color coordinates

    plot_acf(transformedData["lnAssets"], lags=3, title=company, ax = ax1[i//3, i%3], color = 'red')
    plot_pacf(transformedData["lnAssets"], lags=2, title=company, ax = ax2[i//3, i%3], color = 'red')
    plot_acf(transformedData["lnLiabilities"], lags=3, title=company, ax = ax21[i//3, i%3], color = 'red')
    plot_pacf(transformedData["lnLiabilities"], lags=3, title=company, ax = ax22[i//3, i%3], color = 'red')
    plot_acf(transformedData["lnEquity"], lags=3, title=company, ax = ax23[i//3, i%3], color = 'red')
    plot_pacf(transformedData["lnEquity"], lags=3, title=company, ax = ax24[i//3, i%3], color = 'red')
    plot_acf(transformedData["diffAssets"], lags=3, title=company, ax = ax25[i//3, i%3], color = 'red')
    plot_pacf(transformedData["diffAssets"], lags=2, title=company, ax = ax26[i//3, i%3], color = 'red')
    plot_acf(transformedData["diffLiabilities"], lags=3, title=company, ax = ax27[i//3, i%3], color = 'red')
    plot_pacf(transformedData["diffLiabilities"], lags=2, title=company, ax = ax28[i//3, i%3], color = 'red')
    plot_acf(transformedData["diffEquity"], lags=3, title=company, ax = ax29[i//3, i%3], color = 'red')
    plot_pacf(transformedData["diffEquity"], lags=2, title=company, ax = ax30[i//3, i%3], color = 'red')

    fig3 = plotGrowthRate(fig3, ax3, transformedData, "growthAssets", companyMetadata, company, 'Total Asset Growth Rate (%)')
    fig4 = plotGrowthRate(fig4, ax4, transformedData, "growthLiabilities", companyMetadata, company, 'Total Liabilities Growth Rate (%)')
    fig5 = plotGrowthRate(fig5, ax5, transformedData, "growthEquity", companyMetadata, company, 'Total Equity Growth Rate (%)')
    fig10 = plotKPIs(fig10, ax10, transformedData, "totalSatellites", companyMetadata, company, 'Total Launched Satellites')
    fig11 = plotKPIs(fig11, ax11, transformedData, "fractionConstellation", companyMetadata, company, 'Fraction of Constellation Launched')

    if company == "Synspective":
        continue
    else:
        fig6 = plotKPIs(fig6, ax6, transformedData, "financialLeverage", companyMetadata, company, 'Financial Leverage')
        fig7 = plotKPIs(fig7, ax7, transformedData, "ROE", companyMetadata, company, 'Return on Equity')
        fig8 = plotKPIs(fig8, ax8, transformedData, "netProfitMargin", companyMetadata, company, 'Net Profit Margin')
        fig9 = plotKPIs(fig9, ax9, transformedData, "assetTurnover", companyMetadata, company, 'Asset Turnover')

for fig in acf_list:
    fig.tight_layout()
fig1.savefig(f"./images/acf_analysis/lnAssets_acf.png")
fig2.savefig(f"./images/acf_analysis/lnAssets_pacf.png")
fig21.savefig(f"./images/acf_analysis/lnLiabilities_acf.png")
fig22.savefig(f"./images/acf_analysis/lnLiabilities_pacf.png")
fig23.savefig(f"./images/acf_analysis/lnEquity_acf.png")
fig24.savefig(f"./images/acf_analysis/lnEquity_pacf.png")
fig25.savefig(f"./images/acf_analysis/diffAssets_acf.png")
fig26.savefig(f"./images/acf_analysis/diffAssets_pacf.png")
fig27.savefig(f"./images/acf_analysis/diffLiabilities_acf.png")
fig28.savefig(f"./images/acf_analysis/diffLiabilities_pacf.png")
fig29.savefig(f"./images/acf_analysis/diffEquity_acf.png")
fig30.savefig(f"./images/acf_analysis/diffEquity_pacf.png")
fig3.savefig(f"./images/total_asset_growth_rate.png")
fig4.savefig(f"./images/total_liabilities_growth_rate.png")
fig5.savefig(f"./images/total_equity_growth_rate.png")
fig6.savefig(f"./images/financial_leverage.png")
fig7.savefig(f"./images/roe.png")
fig8.savefig(f"./images/npm.png")
fig9.savefig(f"./images/asset_turnover.png")
fig10.savefig(f'./images/total_satellites.png')
fig11.savefig(f'./images/fraction_constellation.png')
