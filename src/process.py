import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from utils import *
from plot_utils import *

def transform_financial_metrics(company, filtered_data):

    diffAssets = np.diff(filtered_data["Total Assets"])
    diffLiabilities = np.diff(filtered_data["Total Liabilities"])
    diffEquity = np.diff(filtered_data["Total Equity"])

    diff2Assets = np.diff(diffAssets)
    diff2Liabilities = np.diff(diffLiabilities)
    diff2Equity = np.diff(diffEquity)

    lnAssets = np.log(filtered_data["Total Assets"])
    lnLiabilities = np.log(filtered_data["Total Liabilities"])
    lnEquity = np.log(filtered_data["Total Equity"])

    growthAssets = (np.diff(filtered_data["Total Assets"]) / filtered_data["Total Assets"][1:]) * 100
    growthLiabilities = (np.diff(filtered_data["Total Liabilities"]) / filtered_data["Total Liabilities"][1:]) * 100
    growthEquity = (np.diff(filtered_data["Total Equity"]) / filtered_data["Total Equity"][1:]) * 100

    diffLogAssets = np.diff(np.log(filtered_data["Total Assets"]))
    diffLogLiabilities = np.diff(np.log(filtered_data["Total Liabilities"]))
    diffLogEquity = np.diff(np.log(filtered_data["Total Equity"]))

    data = {
        "Quarter": filtered_data["Quarter"],
        "totalAssets": filtered_data["Total Assets"],
        "totalLiabilities": filtered_data["Total Liabilities"],
        "totalEquity": filtered_data["Total Equity"],
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
        "diffLogEquity": diffLogEquity
    }
    if company == "synspective":
            print("Not enough revenue data")
    else:
        revenue = filtered_data["Revenue"].values.astype(int)
        data["Revenue"] = revenue
        data["lnRevenue"] = np.log(revenue)
        data["diffRevenue"] = np.diff(revenue)
        data["diff2Revenue"] = np.diff(np.diff(revenue))
        data["growthRevenue"] = (np.diff(revenue) / revenue[1:]) * 100
        data["financialLeverage"] = data["totalAssets"]/data["totalEquity"]
        data["assetTurnover"] = data["Revenue"]/data["totalAssets"]
        data["netProfitMargin"] = filtered_data["Net loss"]/data["Revenue"] 
        data["ROE"] = data["netProfitMargin"]*data["assetTurnover"]*data["financialLeverage"]
        if company == "iQPS":
            # Merge filtered_data with exchange_rate_data based on dates
            merged_data = pd.merge(filtered_data, exchange_rate, left_on='Quarter', right_on='Date', how='left')
            merged_data['Revenue_USD'] = merged_data['Revenue'] / merged_data['Value']
            data["Revenue_USD"] = merged_data['Revenue_USD'].fillna(method='ffill')  # Handle missing values

    return data

# Lookup company-specific parameters from dictionary (plotting style, name, filename)
metadata_json_path = './financial_data/company_metadata.json'
company_metadata = json.load(open(metadata_json_path))
exchange_rate_file = './financial_data/dollar-yen-exchange-rate-history.csv'
exchange_rate = pd.read_csv(exchange_rate_file, header=None, names=['Date', 'Value'])
exchange_rate['Date'] = pd.to_datetime(exchange_rate['Date'])

fig1, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=300)
fig3, ax3 = plt.subplots(figsize=(10, 6), dpi=300)
fig4, ax4 = plt.subplots(figsize=(10, 6), dpi=300)
fig5, ax5 = plt.subplots(figsize=(10, 6), dpi=300)
fig6, ax6 = plt.subplots(figsize=(10, 6), dpi=300)
fig7, ax7 = plt.subplots(figsize=(10, 6), dpi=300)

for i, company in enumerate(company_metadata):
    print("COMPANY: ", company)

    filename = company_metadata[f"{company}"]["file"]
    data = pd.read_excel(f"./financial_data/{filename}","consolidated")

    start_date = pd.to_datetime(company_metadata[f"{company}"]["start_date"])
    end_date = pd.to_datetime(company_metadata[f"{company}"]["end_date"])
    data['Quarter'] = pd.to_datetime(data['Quarter'])

    filtered_data = data[data['Quarter'].between(start_date, end_date)]
    # Convert all columns to type int except time
    cols_to_convert = [col for col in filtered_data.columns if col and col != 'Quarter']
    filtered_data[cols_to_convert] = filtered_data[cols_to_convert].astype(int)

    transformed_data = transform_financial_metrics(company, filtered_data)
    company_color = np.asarray(company_metadata[company]["color"]) / 255 # normalized color coordinates
    fig1 = plot_growth_rate(fig1, ax1, transformed_data, "growthAssets", company_metadata, company, 'Total Asset Growth Rate (%)')
    fig2 = plot_growth_rate(fig2, ax2, transformed_data, "growthLiabilities", company_metadata, company, 'Total Liabilities Growth Rate (%)')
    fig3 = plot_growth_rate(fig3, ax3, transformed_data, "growthEquity", company_metadata, company, 'Total Equity Growth Rate (%)')

    if company == "synspective":
        continue
    else:
        fig4 = plot_kpis(fig4, ax4, transformed_data, "financialLeverage", company_metadata, company, 'Financial Leverage')
        fig5 = plot_kpis(fig5, ax5, transformed_data, "ROE", company_metadata, company, 'Return on Equity')
        fig6 = plot_kpis(fig6, ax6, transformed_data, "netProfitMargin", company_metadata, company, 'Net Profit Margin')
        fig7 = plot_kpis(fig7, ax7, transformed_data, "assetTurnover", company_metadata, company, 'Asset Turnover')

fig1.savefig(f"./images/total_asset_growth_rate.png")
fig2.savefig(f"./images/total_liabilities_growth_rate.png")
fig3.savefig(f"./images/total_equity_growth_rate.png")
fig4.savefig(f"./images/financial_leverage.png")
fig5.savefig(f"./images/roe.png")
fig6.savefig(f"./images/npm.png")
fig7.savefig(f"./images/asset_turnover.png")