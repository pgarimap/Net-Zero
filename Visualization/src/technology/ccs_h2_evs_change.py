from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

from helpers.io import save

sys.path.append("../")
from constants import FIG_SINGLE_WIDTH, mm2inch, FIG_DOUBLE_WIDTH
from helpers.colors import set_stacked_area_colors, set_colors

import os

plt.style.use('./styles/bar_chart_style.mplstyle')

developing_ccs = 'preprocessed_data/technology/evs_ccs_h2_change/developing_spa1_ccs.csv'
df_developing_ccs = pd.read_csv(developing_ccs, index_col=0)
developing_ccs_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developing_ssp2_ccs.csv'
df_developing_ccs_ssp2 = pd.read_csv(developing_ccs_ssp2, index_col=0)

developed_ccs = 'preprocessed_data/technology/evs_ccs_h2_change/developed_spa1_ccs.csv'
df_developed_ccs = pd.read_csv(developed_ccs, index_col=0)
developed_ccs_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developed_ssp2_ccs.csv'
df_developed_ccs_ssp2 = pd.read_csv(developed_ccs_ssp2, index_col=0)

developing_h2 = 'preprocessed_data/technology/evs_ccs_h2_change/developing_spa1_h2.csv'
df_developing_h2 = pd.read_csv(developing_h2, index_col=0)
developing_h2_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developing_ssp2_h2.csv'
df_developing_h2_ssp2 = pd.read_csv(developing_h2_ssp2, index_col=0)

developed_h2 = 'preprocessed_data/technology/evs_ccs_h2_change/developed_spa1_h2.csv'
df_developed_h2 = pd.read_csv(developed_h2, index_col=0)
developed_h2_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developed_ssp2_h2.csv'
df_developed_h2_ssp2 = pd.read_csv(developed_h2_ssp2, index_col=0)

developing_evs = 'preprocessed_data/technology/evs_ccs_h2_change/developing_spa1_evs.csv'
df_developing_evs = pd.read_csv(developing_evs, index_col=0)
developing_evs_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developing_ssp2_evs.csv'
df_developing_evs_ssp2 = pd.read_csv(developing_evs_ssp2, index_col=0)

developed_evs = 'preprocessed_data/technology/evs_ccs_h2_change/developed_spa1_evs.csv'
df_developed_evs = pd.read_csv(developed_evs, index_col=0)
developed_evs_ssp2 = 'preprocessed_data/technology/evs_ccs_h2_change/developed_ssp2_evs.csv'
df_developed_evs_ssp2 = pd.read_csv(developed_evs_ssp2, index_col=0)

fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, FIG_DOUBLE_WIDTH * 0.65))
gs = GridSpec(nrows=3, ncols=2, figure=fig)
axs = []
# add subplots to get following layout:
#   |1|2|3|
#   | 4| 5|

ax1 = fig.add_subplot(gs[0, 0:1])
ax2 = fig.add_subplot(gs[0, 1:2])

ax3 = fig.add_subplot(gs[1, 0:1])
ax4 = fig.add_subplot(gs[1, 1:2])
ax5 = fig.add_subplot(gs[2, 0:1])
ax6 = fig.add_subplot(gs[2, 1:2])
axs.append(ax1)
axs.append(ax2)
axs.append(ax3)
axs.append(ax4)
axs.append(ax5)
axs.append(ax6)

xs = np.asarray([1, 2, 3, 4]) * 3
color_palette = sns.color_palette("Set2")[:2][::-1]

## plot a single unit
def plot_comparison(ax, df1, df2, x_positions, title, ylabel=None):
    '''plot a single unit
    @ax: axis
    @df1: dataframe 1
    @df2: dataframe 2
    @x: x axis positions
    '''
    set_colors(color_palette, ax)

    bars1 = ax.bar(x_positions, df1['value'], label='BAU')
    bars2 = ax.bar(x_positions + 1, df2['value'], label='OS')

    ax.set_xticks([])

    # set labels
    for i, year in enumerate(df1['Year']):
        # ax.text(x_positions[i] + 0.5, -80, year, ha='center', va='center', color='black',
        #         fontsize=5)
        ax.text(i/4 + 0.13, -0.05, year, ha='center', va='center', color='black', fontsize=5, transform=ax.transAxes)

    # set title
    ax.set_title(title, fontsize=6, fontweight='bold',)

    # add values at the bar top
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                '%d' % int(height) if height > 2 else '%.2f' % float(height),
                ha='center', va='bottom', fontsize=4)

    # add values at the bar top
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                '%d' % int(height) if height > 2 else '%.2f' % float(height),
                ha='center', va='bottom', fontsize=4)

    # set ylabel
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=6, fontweight='bold')


# plot ccs
plot_comparison(axs[0], df_developing_ccs_ssp2,
                df_developing_ccs, xs, title="Developing region  \n \n CCS", ylabel="Sequestration (MTC)")
plot_comparison(axs[1], df_developed_ccs_ssp2,
                df_developed_ccs, xs, title="Developed region \n \n CCS")

# set fig title as a
axs[0].text(-0.1, 1.1, 'a', transform=axs[0].transAxes, fontsize=7, fontweight='bold', va='top')

# plot evs
plot_comparison(axs[2], df_developing_evs_ssp2,
                df_developing_evs, xs, title="EVs", ylabel="Energy use (EJ)")
plot_comparison(axs[3], df_developed_evs_ssp2,
                df_developed_evs, xs, title="EVs")
# set fig title as b
axs[2].text(-0.1, 1.1, 'b', transform=axs[2].transAxes, fontsize=7, fontweight='bold', va='top')

# plot h2
plot_comparison(axs[4], df_developing_h2_ssp2,
                df_developing_h2, xs, title="Hydrogen", ylabel="Energy use (EJ)")
plot_comparison(axs[5], df_developed_h2_ssp2,
                df_developed_h2, xs, title="Hydrogen")

# set fig title as c
axs[4].text(-0.1, 1.1, 'c', transform=axs[4].transAxes, fontsize=7, fontweight='bold', va='top')

## handle legend
# Add custom legend
handles, labels = axs[0].get_legend_handles_labels()
# nlabels = list(range(0, len(handles)))

# handle legend
fig.legend(handles,
           labels,
           loc='lower center', ncol=2,
           bbox_to_anchor=(0.5, 0.008), fontsize=7)

# adjust margins
plt.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.9, wspace=0.2, hspace=0.4)
fig.subplots_adjust(bottom=0.1)

# plt.tight_layout()
save('ccs_h2_evs_change')
plt.show()
