import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

def plotGrowthRate(fig, ax, data, key, companyMetadata, company, ylabel):
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    company_color = np.array(companyMetadata[company]["color"]) / 255
    ax.plot(data["Quarter"][1:], data[key], color=company_color, linestyle=companyMetadata[company]["style"], label=company, linewidth=10)
    ax.legend(ncol=3, bbox_to_anchor=(0.9, -0.15), fancybox=True, title="Company", fontsize='16', frameon=True)
    ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
    fig.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    plt.rcParams['legend.title_fontsize'] = '16'
    return fig
    
def plotKPIs(fig, ax, data, key, companyMetadata, company, ylabel):
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    company_color = np.array(companyMetadata[company]["color"]) / 255
    ax.plot(data["Quarter"], data[key], color=company_color, linestyle=companyMetadata[company]["style"], label=company, linewidth=10)
    ax.legend(ncol=3, bbox_to_anchor=(0.9, -0.15), fancybox=True, title="Company", fontsize='16', frameon=True)
    ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
    if ylabel=="Revenue ($USD)":
        ax.set_yscale('log')
        ax.set_ylim([1, 10**9])
    fig.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    plt.rcParams['legend.title_fontsize'] = '16'
    return fig

def plotPredictions(fig, ax, company, companyMetadata, time=None, inSamplePrediction=None, outSamplePrediction=None, ground_truth=None, ylabel=None, split=None, plotEverything=False):
    size = 22
    if company != "Synspective" and not plotEverything:
        company_color = np.array(companyMetadata[company]["color"]) / 255
        ax.set_title(company, fontsize=16, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.set_xlabel('Year', fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
        ax.plot(time[:-split], inSamplePrediction, color=company_color, linestyle="dotted", label="In-Sample Prediction", linewidth=10)
        ax.plot(time[-split:], outSamplePrediction, color=company_color, alpha=0.5, linestyle="dashed", label="Out-of-Sample Prediction", linewidth=10)
        ax.plot(time, ground_truth, color=company_color, linestyle="solid", label="Ground Truth", linewidth=10)
        ax.legend(ncol=3, bbox_to_anchor=(1.0, -0.15), fancybox=True, fontsize='14', frameon=True)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    elif company!= "Synspective" and plotEverything:
        company_color = np.array(companyMetadata[company]["color"]) / 255
        ax.set_title(company, fontsize=size, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_xlabel('Year', fontsize=size)
        ax.set_ylabel('Revenue ($ USD)', fontsize=size)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.set_yscale('log')
        ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
        ax.set_ylim([1, 10**9])
        ax.plot(time[:-split], inSamplePrediction, color=company_color, linestyle="dotted", linewidth=12)
        ax.plot(time[-split:], outSamplePrediction, color=company_color, alpha=0.5, linestyle="dashed", linewidth=12)
        ax.plot(time, ground_truth, color=company_color, linestyle="solid", linewidth=12)
    elif company == "Synspective" and plotEverything:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(company, fontsize=size, fontweight='bold')
        ax.text(0.5, 0.5, 'Data not available', horizontalalignment='center',
        verticalalignment='center', fontsize=size, color='black',
        transform=ax.transAxes)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        line1, = ax.plot([], [], color='k', linestyle="dotted", linewidth=12, label='In-Sample Prediction')
        line2, = ax.plot([], [], color='k', linestyle="dashed", alpha=0.5, linewidth=12, label='Out-of-Sample Prediction')
        line3, = ax.plot([], [], color='k', linestyle="solid", linewidth=12, label='Ground Truth Data')
        # Add the legend with specified labels
        fig.legend([line1, line2, line3], ['In-Sample Prediction', 'Out-of-Sample Prediction', 'Ground Truth Data'],
           loc='upper center', bbox_to_anchor=(0.5, 0.08), ncol=3, prop={'size': size})
    return fig