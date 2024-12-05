import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import numpy as np
import seaborn as sns

import sys

from helpers.io import save

sys.path.append("../../")
from constants import FIG_SINGLE_WIDTH, mm2inch, FIG_DOUBLE_WIDTH
from helpers.colors import set_stacked_area_colors

plt.style.use('./styles/stacked_area.mplstyle')

file = "./preprocessed_data/technology/developing_spa1_electric_transport_energy_by_fuel_n_tech.csv"

df = pd.read_csv(file, index_col=0)
df = df.fillna(0)

df.loc[df['region'] == 'Africa_Western', 'region'] = 'Western Africa'
regions = df['region'].unique()

fig = plt.figure(figsize=(FIG_DOUBLE_WIDTH, FIG_DOUBLE_WIDTH * 0.65))
gs = GridSpec(nrows=2, ncols=3 * 2, figure=fig)
axs = []
# add subplots to get following layout:
#   |1|2|3|
#   | 4| 5|

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2:4])

ax3 = fig.add_subplot(gs[1, 0:2])
ax4 = fig.add_subplot(gs[1, 2:4])
ax5 = fig.add_subplot(gs[1, 4:6])
axs.append(ax1)
axs.append(ax2)
axs.append(ax3)
axs.append(ax4)
axs.append(ax5)

abcde = ['a', 'b',
         'c', 'd', 'e']

abcde = [i.capitalize() for i in abcde]

for i, region in enumerate(regions):
    ax = axs[i]
    set_stacked_area_colors(ax, option_id=2)

    df_regional = pd.pivot_table(df[df['region'] == region], index=['Year'], values='value', columns=['mode'], aggfunc= np.sum, fill_value=0).reset_index()
    cols = [df_regional[col_name] for col_name in df_regional.columns[1:]]

    ax.stackplot(df_regional['Year'], *cols,
                 labels=df_regional.columns[1:],
                 edgecolor='black', linewidth=0.3)

    # ax.set_xticks(np.arange(2005, 2100, 20))
    ax.set_title(region, fontsize=7, fontweight='bold')
    ax.set_xlabel('Year',  fontsize=6)
    ax.set_ylabel('Energy use (EJ)', fontsize=6)

    ax.text(-0.1, 1.1, abcde[i], transform=ax.transAxes, fontsize=7, fontweight='bold', va='top')

# Add custom legend
handles, labels = axs[0].get_legend_handles_labels()
nlabels = list(range(0, len(handles)))

# handle legend
fig.legend([handles[i] for i in nlabels][::-1],
           [labels[i].title() for i in nlabels][::-1],
           loc='center right', ncol=1,
           bbox_to_anchor=(0.82, 0.75), fontsize=7)

plt.tight_layout()
save('evs_mode_by_region')
plt.show()
