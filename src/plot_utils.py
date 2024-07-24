import matplotlib.pyplot as plt
import numpy as np

def plot_growth_rate(fig, ax, data, key, company_metadata, company, ylabel):
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    company_color = np.array(company_metadata[company]["color"]) / 255
    ax.plot(data["Quarter"].values[1:], data[key], color=company_color, linestyle=company_metadata[company]["style"], label=company, linewidth=10)
    ax.legend(ncol=4, bbox_to_anchor=(.95, -0.15), fancybox=True, title="Company", fontsize='16', frameon=True)
    fig.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    plt.rcParams['legend.title_fontsize'] = '16'
    return fig
    
def plot_kpis(fig, ax, data, key, company_metadata, company, ylabel):
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    company_color = np.array(company_metadata[company]["color"]) / 255
    ax.plot(data["Quarter"].values[:], data[key], color=company_color, linestyle=company_metadata[company]["style"], label=company, linewidth=10)
    ax.legend(ncol=4, bbox_to_anchor=(0.8, -0.15), fancybox=True, title="Company", fontsize='16', frameon=True)
    fig.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    plt.rcParams['legend.title_fontsize'] = '16'
    return fig