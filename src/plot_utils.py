import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def plotGrowthRate(fig, ax, data, key, companyMetadata, company, ylabel):
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    company_color = np.array(companyMetadata[company]["color"]) / 255
    ax.plot(data["Quarter"][1:], data[key], color=company_color, linestyle=companyMetadata[company]["style"], label=company, linewidth=10)
    ax.legend(ncol=3, bbox_to_anchor=(0.9, -0.15), fancybox=True, title="Company", fontsize='16', frameon=True)
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
    fig.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    plt.rcParams['legend.title_fontsize'] = '16'
    return fig

def plotPredictions(fig, ax, time, prediction, companyMetadata, company):
    ax.set_title(company, fontsize=16, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel('Revenue ($ USD)', fontsize=16)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    company_color = np.array(companyMetadata[company]["color"]) / 255
    ax.plot(time, prediction, color=company_color, linestyle=companyMetadata[company]["style"], label=company, linewidth=10)
    fig.tight_layout()
    return fig