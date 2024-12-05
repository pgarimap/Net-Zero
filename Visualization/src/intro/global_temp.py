from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from constants import FIG_SINGLE_WIDTH, mm2inch
from helpers.io import save

sys.path.append("../")

plt.style.use('./styles/plot.mplstyle')

# file paths
df_ssp1 = "./preprocessed_data/intro/global_mean_temp_ssp1.csv"
ssp2 = "./preprocessed_data/intro/global_mean_temp_ssp2.csv"

# columns : 'Units', 'region', 'fuel', 'value'

df_ssp1 = pd.read_csv(df_ssp1)
df_ssp2 = pd.read_csv(ssp2)

# aggregate value(sum) by fuel
df_ssp1 = pd.pivot_table(df_ssp1, index=['Year'], values=['value'], aggfunc=np.sum)
df_ssp2 = pd.pivot_table(df_ssp2, index=['Year'], values=['value'], aggfunc=np.sum)

# limit year to present
limit_year = 2020
df_limit = df_ssp2[df_ssp2.index <= limit_year]
lx, ly = df_limit.index.values, df_limit['value'].values

df_ssp1 = df_ssp1[df_ssp1.index >= limit_year]
df_ssp2 = df_ssp2[df_ssp2.index >= limit_year]
x1, y1 = df_ssp1.index.values, df_ssp1['value'].values
x2, y2 = df_ssp2.index.values, df_ssp2['value'].values


def plot():
    spreading_factor = 3
    # create a new figure
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(60)))

    # add a new subplot to the figure
    ax = fig.add_subplot(111)

    ax.axhline(y=1.8, color='gray', linestyle='--', linewidth=0.5)
    ax.plot(lx, ly, color='dimgrey')

    ax.plot(x2, y2, label='SSP2', color='darkorange')

    # ax.fill_between(x2, y2 - 100 * spreading_factor, y2 + 100 * spreading_factor,
    #                 color='orange', alpha=0.2, edgecolor='none')

    ax.plot(x1, y1, color='green', label='SSP1')
    # ax.fill_between(x1, y1 - 100 * spreading_factor, y1 + 100 * spreading_factor,
    #                 color='green', alpha=0.2, edgecolor='none')

    ax.set_xlabel('Year')
    ax.set_ylabel('Global Mean Temperature (in $^\circ$C)')

    plt.legend()
    plt.tight_layout()
    save('global_temperature')
    plt.show()


plot()
