import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np
import json
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from utils import *
from plot_utils import *
pd.options.mode.chained_assignment = None
plt.rcParams['figure.max_open_warning'] = 50

def transformFinancialMetrics(company, filteredData):

    growthAssets = (np.diff(filteredData["Total Assets"]) / filteredData["Total Assets"][1:]) * 100
    growthLiabilities = (np.diff(filteredData["Total Liabilities"]) / filteredData["Total Liabilities"][1:]) * 100
    growthEquity = (np.diff(filteredData["Total Equity"]) / filteredData["Total Equity"][1:]) * 100

    totalSats = filteredData["Total Launched Satellites"].copy().iloc[-1]
    data = {
        "Quarter": pd.Series(filteredData["Quarter"].copy()).reset_index(drop=True),
        "totalAssets": pd.Series(filteredData["Total Assets"].copy().values.astype(int)).reset_index(drop=True),
        "totalLiabilities": pd.Series(filteredData["Total Liabilities"].values.astype(int)).reset_index(drop=True),
        "totalEquity": pd.Series(filteredData["Total Equity"].values.astype(int)).reset_index(drop=True),
        "growthAssets": pd.Series(growthAssets).reset_index(drop=True),
        "growthLiabilities": pd.Series(growthLiabilities).reset_index(drop=True),
        "growthEquity": pd.Series(growthEquity).reset_index(drop=True),
        "totalSatellites": pd.Series(filteredData["Total Launched Satellites"].copy()).reset_index(drop=True),
        "fractionConstellation": pd.Series(filteredData["Total Launched Satellites"].copy()/totalSats).reset_index(drop=True)
    }
    if company == "Synspective":
        # Merge filteredData with exchangeRateData_data based on dates
        merged_data = pd.merge(filteredData, yenExchangeRateData, left_on='Quarter', right_on='Date', how='left')
        merged_data['Total_Assets_USD'] = merged_data['Total Assets'] / merged_data['Value']
        merged_data['Total_Liabilities_USD'] = merged_data['Total Liabilities'] / merged_data['Value']
        merged_data['Total_Equity_USD'] = merged_data['Total Equity'] / merged_data['Value']
        # Handle missing values
        data["Total_Assets_USD"] = merged_data['Total_Assets_USD'].fillna(method='ffill').reset_index(drop=True)
        data["Total_Liabilities_USD"] = merged_data['Total_Liabilities_USD'].fillna(method='ffill').reset_index(drop=True)
        data["Total_Equity_USD"] = merged_data['Total_Equity_USD'].fillna(method='ffill').reset_index(drop=True)
        print("Not enough revenue data")
    else:
        revenue = filteredData["Revenue"]
        data["Revenue"] = pd.Series(revenue).reset_index(drop=True)
        data["EBITDA"] = pd.Series(filteredData["EBITDA"]).reset_index(drop=True)
        data["financialLeverage"] = (data["totalAssets"]/data["totalEquity"]).reset_index(drop=True)
        data["assetTurnover"] = (data["Revenue"]/data["totalAssets"]).reset_index(drop=True)
        data["netProfitMargin"] = (filteredData["Net Loss"].reset_index(drop=True)/data["Revenue"])
        data["ROE"] = (data["netProfitMargin"]*data["assetTurnover"]*data["financialLeverage"]).reset_index(drop=True)
        if company == "iQPS":
            # Merge filteredData with exchangeRateData_data based on dates
            merged_data = pd.merge(filteredData, yenExchangeRateData, left_on='Quarter', right_on='Date', how='left')
            merged_data['Revenue_USD'] = merged_data['Revenue'] / merged_data['Value']
            merged_data['EBITDA_USD'] = merged_data['EBITDA'] / merged_data['Value']
            merged_data['Total_Assets_USD'] = merged_data['Total Assets'] / merged_data['Value']
            merged_data['Total_Liabilities_USD'] = merged_data['Total Liabilities'] / merged_data['Value']
            merged_data['Total_Equity_USD'] = merged_data['Total Equity'] / merged_data['Value']
            # Handle missing values
            data["Revenue_USD"] = merged_data['Revenue_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["EBITDA_USD"] = merged_data['EBITDA_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Assets_USD"] = merged_data['Total_Assets_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Liabilities_USD"] = merged_data['Total_Liabilities_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Equity_USD"] = merged_data['Total_Equity_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
        elif company == "GomSpace":
            # Merge filteredData with exchangeRateData_data based on dates
            merged_data = pd.merge(filteredData, sekExchangeRateData, left_on='Quarter', right_on='Date', how='left')
            merged_data['Revenue_USD'] = merged_data['Revenue'] / merged_data['Value']
            merged_data['EBITDA_USD'] = merged_data['EBITDA'] / merged_data['Value']
            merged_data['Total_Assets_USD'] = merged_data['Total Assets'] / merged_data['Value']
            merged_data['Total_Liabilities_USD'] = merged_data['Total Liabilities'] / merged_data['Value']
            merged_data['Total_Equity_USD'] = merged_data['Total Equity'] / merged_data['Value']
            # Handle missing values
            data["Revenue_USD"] = merged_data['Revenue_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["EBITDA_USD"] = merged_data['EBITDA_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Assets_USD"] = merged_data['Total_Assets_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Liabilities_USD"] = merged_data['Total_Liabilities_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Equity_USD"] = merged_data['Total_Equity_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
        elif company == "Kleos Space":
            # Merge filteredData with exchangeRateData_data based on dates
            merged_data = pd.merge(filteredData, eurExchangeRateData, left_on='Quarter', right_on='Date', how='left')
            merged_data['Revenue_USD'] = merged_data['Revenue'] / merged_data['Value']
            merged_data['EBITDA_USD'] = merged_data['EBITDA'] / merged_data['Value']
            merged_data['Total_Assets_USD'] = merged_data['Total Assets'] / merged_data['Value']
            merged_data['Total_Liabilities_USD'] = merged_data['Total Liabilities'] / merged_data['Value']
            merged_data['Total_Equity_USD'] = merged_data['Total Equity'] / merged_data['Value']
            # Handle missing values
            data["Revenue_USD"] = merged_data['Revenue_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["EBITDA_USD"] = merged_data['EBITDA_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Assets_USD"] = merged_data['Total_Assets_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Liabilities_USD"] = merged_data['Total_Liabilities_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Equity_USD"] = merged_data['Total_Equity_USD'].fillna(method='ffill').astype(int).reset_index(drop=True)
        elif company == "Planet Labs" or "Satellogic":
            data["Revenue_USD"] = filteredData['Revenue'].reset_index(drop=True)
            data["EBITDA_USD"] = filteredData['EBITDA'].fillna(method='ffill').astype(int).reset_index(drop=True)
            data["Total_Assets_USD"] = filteredData['Total Assets'].reset_index(drop=True)
            data["Total_Liabilities_USD"] = filteredData['Total Liabilities'].reset_index(drop=True)
            data["Total_Equity_USD"] = filteredData['Total Equity'].reset_index(drop=True)

    return data

# Function to generate the next n quarters after a given start date
def generate_next_quarters(start_date, n):
    quarters = []
    current_date = start_date
    for _ in range(n):
        current_date = (current_date + DateOffset(months=3)).replace(day=1) - pd.DateOffset(days=1)
        quarters.append(current_date)
        current_date = current_date + pd.DateOffset(months=3)
    return quarters

# Lookup company-specific parameters from dictionary (plotting style, name, filename)
metadataPath = './config/company_metadata.json'
companyMetadata = json.load(open(metadataPath))
yenExchangeRatePath = './config/usd-yen-exchange-rate-history.csv'
yenExchangeRateData = pd.read_csv(yenExchangeRatePath, header=None, names=['Date', 'Value'])
yenExchangeRateData['Date'] = pd.to_datetime(yenExchangeRateData['Date'])
sekExchangeRatePath = './config/usd-sek-exchange-rate-history.csv'
sekExchangeRateData = pd.read_csv(sekExchangeRatePath, header=None, names=['Date', 'Value'])
sekExchangeRateData['Date'] = pd.to_datetime(sekExchangeRateData['Date'])
eurExchangeRatePath = './config/usd-eur-exchange-rate-history.csv'
eurExchangeRateData = pd.read_csv(eurExchangeRatePath, header=None, names=['Date', 'Value'])
eurExchangeRateData['Date'] = pd.to_datetime(eurExchangeRateData['Date'])

# ACF/PACF Plots
fig21, ax21 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig21.suptitle("ACF: Assets", fontsize=20)
fig22, ax22 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig22.suptitle("PACF: Assets", fontsize=20)
fig23, ax23 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig23.suptitle("ACF: Liabilities", fontsize=20)
fig24, ax24 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig24.suptitle("PACF: Liabilities", fontsize=20)
fig25, ax25 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig25.suptitle("ACF: Equity", fontsize=20)
fig26, ax26 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig26.suptitle("PACF: Equity", fontsize=20)
fig27, ax27 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig27.suptitle("ACF: Revenue", fontsize=20)
fig28, ax28 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig28.suptitle("PACF: Revenue", fontsize=20)
fig29, ax29 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig29.suptitle("ACF: EBITDA", fontsize=20)
fig30, ax30 = plt.subplots(2, 3, figsize=(12, 10), dpi=300)
fig30.suptitle("PACF: EBITDA", fontsize=20)
acf_list = [fig21, fig22, fig23, fig24, fig25, fig26, fig27, fig28, fig29, fig30]

# KPI Plots
fig1, ax1 = plt.subplots(figsize=(10, 7), dpi=300)
fig2, ax2 = plt.subplots(figsize=(10, 7), dpi=300)
fig3, ax3 = plt.subplots(figsize=(10, 7), dpi=300)
fig4, ax4 = plt.subplots(figsize=(10, 7), dpi=300)
fig5, ax5 = plt.subplots(figsize=(10, 7), dpi=300)
fig6, ax6 = plt.subplots(figsize=(10, 7), dpi=300)
fig7, ax7 = plt.subplots(figsize=(10, 7), dpi=300)
fig8, ax8 = plt.subplots(figsize=(10, 7), dpi=300)
fig9, ax9 = plt.subplots(figsize=(10, 7), dpi=300)
fig10, ax10 = plt.subplots(figsize=(10, 7), dpi=300)
fig11, ax11 = plt.subplots(figsize=(10, 7), dpi=300)
fig12, ax12 = plt.subplots(figsize=(10, 7), dpi=300)
fig13, ax13 = plt.subplots(figsize=(10, 7), dpi=300)
fig14, ax14 = plt.subplots(figsize=(10, 7), dpi=300)
fig15, ax15 = plt.subplots(figsize=(10, 7), dpi=300)
fig16, ax16 = plt.subplots(figsize=(10, 7), dpi=300)
fig17, ax17 = plt.subplots(2, 3, figsize=(30, 20), dpi=300)
fig18, ax18 = plt.subplots(2, 3, figsize=(30, 20), dpi=300)

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

    # Use 90% of the data for in-sample training and 10% for out-of-sample evaluation
    split = int(np.ceil(0.2*len(transformedData['Quarter'])))
    if company != "Synspective":
        filtered_quarters = pd.to_datetime(transformedData['Quarter'])

        # Determine the last quarter
        last_quarter = filtered_quarters.max()
        trainingFrame1 = np.column_stack((transformedData["Total_Assets_USD"][:-split], transformedData["Total_Equity_USD"][:-split], transformedData["Total_Liabilities_USD"][:-split], transformedData["totalSatellites"][:-split]))
        testingFrame1 = np.column_stack((transformedData["Total_Assets_USD"][-split:], transformedData["Total_Equity_USD"][-split:], transformedData["Total_Liabilities_USD"][-split:], transformedData["totalSatellites"][-split:]))
        ardl1_fit = ardl_model(transformedData["Revenue_USD"][:-split], trainingFrame1, 10)
        trainingFrame2 = np.column_stack((trainingFrame1, transformedData["Revenue_USD"][:-split]))
        testingFrame2 = np.column_stack((testingFrame1, transformedData["Revenue_USD"][-split:]))
        ardl2_fit = ardl_model(transformedData["EBITDA_USD"][:-split], trainingFrame2, 10)
        
        # In-Sample Prediction: Use the model to predict the underlying data
        inSamplePredictions1 = ardl1_fit.predict(start=0, end=len(trainingFrame1)-1)
        inSamplePredictions2 = ardl2_fit.predict(start=0, end=len(trainingFrame2)-1)
        # Out-of-Sample Forecasting: Use the model to forecast on unseen data
        # Note, ardl_fit.predict will output same amount of data it was trained on, hence indexing up to [:split]
        outSamplePredictions1 = ardl1_fit.predict(exog_oos=testingFrame1)[:split]
        outSamplePredictions2 = ardl2_fit.predict(exog_oos=testingFrame2)[:split]

        # print(filteredData["Quarter"])
        if company == "iQPS":
            plotPredictions(fig10, ax10, company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue ($ USD)", split)
        elif company == "GOMSpace":
            plotPredictions(fig11, ax11, company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue ($ USD)", split)
        elif company == "Kleos Space":
            plotPredictions(fig12, ax12, company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue ($ USD)", split)
        elif company == "Planet Labs":
            plotPredictions(fig13, ax13, company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue ($ USD)", split)
        elif company == "Satellogic":
            plotPredictions(fig14, ax14, company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue ($ USD)", split)

        fig4 = plotKPIs(fig4, ax4, transformedData, "financialLeverage", companyMetadata, company, 'Financial Leverage')
        fig5 = plotKPIs(fig5, ax5, transformedData, "ROE", companyMetadata, company, 'Return on Equity')
        fig6 = plotKPIs(fig6, ax6, transformedData, "netProfitMargin", companyMetadata, company, 'Net Profit Margin')
        fig7 = plotKPIs(fig7, ax7, transformedData, "assetTurnover", companyMetadata, company, 'Asset Turnover')
        fig15 = plotKPIs(fig15, ax15, transformedData, "Revenue_USD", companyMetadata, company, 'Revenue ($USD)')
        fig16 = plotKPIs(fig16, ax16, transformedData, "EBITDA_USD", companyMetadata, company, 'EBITDA ($USD)')
        plot_acf(transformedData["Revenue_USD"], lags=3, title=company, ax = ax27[i//3, i%3], color = 'red')
        plot_pacf(transformedData["Revenue_USD"], lags=2, title=company, ax = ax28[i//3, i%3], color = 'red')
        plot_acf(transformedData["EBITDA_USD"], lags=3, title=company, ax = ax29[i//3, i%3], color = 'red')
        plot_pacf(transformedData["EBITDA_USD"], lags=2, title=company, ax = ax30[i//3, i%3], color = 'red')
        plotPredictions(fig17, ax17[i//3, i%3], company, companyMetadata, filteredData["Quarter"], inSamplePredictions1, outSamplePredictions1, transformedData["Revenue_USD"], "Revenue $ (USD)", split, plotEverything=True)
        plotPredictions(fig18, ax18[i//3, i%3], company, companyMetadata, filteredData["Quarter"], inSamplePredictions2, outSamplePredictions2, transformedData["EBITDA_USD"], "EBITDA $ (USD)", split, plotEverything=True)
    else:
        plotPredictions(fig17, ax17[i//3, i%3], company, companyMetadata, plotEverything=True)
        plotPredictions(fig18, ax18[i//3, i%3], company, companyMetadata, plotEverything=True)

    plot_acf(transformedData["Total_Assets_USD"], lags=3, title=company, ax = ax21[i//3, i%3], color = 'red')
    plot_pacf(transformedData["Total_Assets_USD"], lags=2, title=company, ax = ax22[i//3, i%3], color = 'red')
    plot_acf(transformedData["Total_Liabilities_USD"], lags=3, title=company, ax = ax23[i//3, i%3], color = 'red')
    plot_pacf(transformedData["Total_Liabilities_USD"], lags=3, title=company, ax = ax24[i//3, i%3], color = 'red')
    plot_acf(transformedData["Total_Equity_USD"], lags=3, title=company, ax = ax25[i//3, i%3], color = 'red')
    plot_pacf(transformedData["Total_Equity_USD"], lags=3, title=company, ax = ax26[i//3, i%3], color = 'red')

    fig1 = plotGrowthRate(fig1, ax1, transformedData, "growthAssets", companyMetadata, company, 'Total Asset Growth Rate (%)')
    fig2 = plotGrowthRate(fig2, ax2, transformedData, "growthLiabilities", companyMetadata, company, 'Total Liabilities Growth Rate (%)')
    fig3 = plotGrowthRate(fig3, ax3, transformedData, "growthEquity", companyMetadata, company, 'Total Equity Growth Rate (%)')
    fig8 = plotKPIs(fig8, ax8, transformedData, "totalSatellites", companyMetadata, company, 'Total Launched Satellites')
    fig9 = plotKPIs(fig9, ax9, transformedData, "fractionConstellation", companyMetadata, company, 'Fraction of Constellation Launched')

for fig in acf_list:
    fig.tight_layout()
fig21.savefig(f"./images/acf_analysis/Assets_acf.png", bbox_inches='tight')
fig22.savefig(f"./images/acf_analysis/Assets_pacf.png", bbox_inches='tight')
fig23.savefig(f"./images/acf_analysis/Liabilities_acf.png", bbox_inches='tight')
fig24.savefig(f"./images/acf_analysis/Liabilities_pacf.png", bbox_inches='tight')
fig25.savefig(f"./images/acf_analysis/Equity_acf.png", bbox_inches='tight')
fig26.savefig(f"./images/acf_analysis/Equity_pacf.png", bbox_inches='tight')
fig27.savefig(f"./images/acf_analysis/Revenue_acf.png", bbox_inches='tight')
fig28.savefig(f"./images/acf_analysis/Revenue_pacf.png", bbox_inches='tight')
fig29.savefig(f"./images/acf_analysis/EBITDA_acf.png", bbox_inches='tight')
fig30.savefig(f"./images/acf_analysis/EBITDA_pacf.png", bbox_inches='tight')
fig1.savefig(f"./images/total_asset_growth_rate.png", bbox_inches='tight')
fig2.savefig(f"./images/total_liabilities_growth_rate.png", bbox_inches='tight')
fig3.savefig(f"./images/total_equity_growth_rate.png", bbox_inches='tight')
fig4.savefig(f"./images/financial_leverage.png", bbox_inches='tight')
fig5.savefig(f"./images/roe.png", bbox_inches='tight')
fig6.savefig(f"./images/npm.png", bbox_inches='tight')
fig7.savefig(f"./images/asset_turnover.png", bbox_inches='tight')
fig8.savefig(f'./images/total_satellites.png', bbox_inches='tight')
fig9.savefig(f'./images/fraction_constellation.png', bbox_inches='tight')
fig10.savefig(f'./images/iqps_isp.png', bbox_inches='tight')
fig11.savefig(f'./images/gom_isp.png', bbox_inches='tight')
fig12.savefig(f'./images/kleos_isp.png', bbox_inches='tight')
fig13.savefig(f'./images/planet_isp.png', bbox_inches='tight')
fig14.savefig(f'./images/satellogic_isp.png', bbox_inches='tight')
fig15.savefig(f'./images/revenue.png', bbox_inches='tight')
fig16.savefig(f'./images/ebitda.png', bbox_inches='tight')
fig17.savefig(f'./images/revenue_separate.png', bbox_inches='tight')
fig18.savefig(f'./images/ebitda_separate.png', bbox_inches='tight')