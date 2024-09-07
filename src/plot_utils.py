# /usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import SymmetricalLogLocator as symlog
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
    size = 32
    if not plotEverything:
        company_color = np.array(companyMetadata[company]["color"]) / 255
        ax.set_title(company, fontsize=16, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.set_xlabel('Year', fontsize=16)
        ax.set_ylabel(ylabel, fontsize=16)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
        ax.plot(time[:-split], inSamplePrediction, color=company_color, linestyle="", marker=".", markersize=18, label="In-Sample Prediction")
        ax.plot(time[-split:], outSamplePrediction, color=company_color, marker="*", markersize=18, linestyle="", label="Out-of-Sample Forecast")
        ax.plot(time, ground_truth, color=company_color, linestyle="solid", label="Ground Truth", linewidth=10)
        ax.legend(ncol=3, bbox_to_anchor=(1.0, -0.15), fancybox=True, fontsize='14', frameon=True)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    elif plotEverything:
        company_color = np.array(companyMetadata[company]["color"]) / 255
        ax.set_title(company, fontsize=40, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=size)
        ax.set_xlabel('Year', fontsize=size)
        ax.set_ylabel(ylabel, fontsize=size)
        ax.set_yscale('symlog')
        if ylabel=="Revenue $ (USD)":
            vmin, vmax = 0, 10**9
        else:
            vmin, vmax = -10**9, 10**9
        ax.set_yticks(tick_values(vmin, vmax, 7))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        ax.set_ylim([vmin, vmax])
        ax.set_xlim([pd.to_datetime('2018-06-01'), pd.to_datetime('2024-12-31')])
        ax.plot(time[:-split], inSamplePrediction, color=company_color, alpha=0.7, linestyle="", marker="s", markersize=40)
        ax.plot(time[-split:], outSamplePrediction, color=company_color, alpha=0.7, marker="*", markersize=40, linestyle="")
        ax.plot(time, ground_truth, color=company_color, linestyle="solid", linewidth=20)
    if ylabel=="Revenue $ (USD)":
        line1, = ax.plot([], [], color='k', linestyle="", alpha=0.7, marker="s", markersize=40, label='In-Sample Prediction')
        line2, = ax.plot([], [], color='k', marker="*", alpha=0.7, markersize=40, linestyle="", label='Out-of-Sample Forecast')
        line3, = ax.plot([], [], color='k', linestyle="solid", linewidth=20, label='Ground Truth Data')
        # Add the legend with specified labels
        fig.legend([line1, line2, line3], ['In-Sample Prediction', 'Out-of-Sample Forecast', 'Ground Truth Data'],
            loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=3, prop={'size': size}, fontsize=size)
    return fig

# Fixes setting number of ticks on a symlog scale, copied from:
# https://github.com/matplotlib/matplotlib/issues/17402
def tick_values(vmin, vmax, numticks):
    base = 10
    linthresh = 10

    if vmax < vmin:
        vmin, vmax = vmax, vmin

    # "simple" mode is when the range falls entirely within (-t,
    # t) -- it should just display (vmin, 0, vmax)
    if -linthresh < vmin < vmax < linthresh:
        # only the linear range is present
        return [vmin, vmax]

    # Lower log range is present
    has_a = (vmin < -linthresh)
    # Upper log range is present
    has_c = (vmax > linthresh)

    # Check if linear range is present
    has_b = (has_a and vmax > -linthresh) or (has_c and vmin < linthresh)

    def get_log_range(lo, hi):
        lo = np.floor(np.log(lo) / np.log(base))
        hi = np.ceil(np.log(hi) / np.log(base))
        return lo, hi

    # Calculate all the ranges, so we can determine striding
    a_lo, a_hi = (0, 0)
    if has_a:
        a_upper_lim = min(-linthresh, vmax)
        a_lo, a_hi = get_log_range(abs(a_upper_lim), abs(vmin) + 1)

    c_lo, c_hi = (0, 0)
    if has_c:
        c_lower_lim = max(linthresh, vmin)
        c_lo, c_hi = get_log_range(c_lower_lim, vmax + 1)

    # Calculate the total number of integer exponents in a and c ranges
    total_ticks = (a_hi - a_lo) + (c_hi - c_lo)
    if has_b:
        total_ticks += 1
    stride = max(total_ticks // (numticks - 1), 1)

    decades = []
    if has_a:
        decades.extend(-1 * (base ** (np.arange(a_lo, a_hi, stride)[::-1])))

    if has_b:
        decades.append(0.0)

    if has_c:
        decades.extend(base ** (np.arange(c_lo, c_hi, stride)))

    subs = np.arange(1.0, base)

    if len(subs) > 1 or subs[0] != 1.0:
        ticklocs = []
        for decade in decades:
            if decade == 0:
                ticklocs.append(decade)
            else:
                ticklocs.extend(subs * decade)
    else:
        ticklocs = decades
        # if there is not enough ticks to show on the graph
        if len(ticklocs) <= 3:
            ticklocs.extend(subs)
            subs= np.linspace(vmin, vmax, 10) # 7 can be changed, it will just change the number of value displayed
    
    return np.array(ticklocs)