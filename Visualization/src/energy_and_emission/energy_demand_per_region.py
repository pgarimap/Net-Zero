from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.io import save

sys.path.append("../")
from constants import FIG_SINGLE_WIDTH, mm2inch, FIG_DOUBLE_WIDTH
from helpers.colors import set_stacked_area_colors

import os

plt.style.use('./styles/bar_chart_style.mplstyle')

# out paths
table_out_path = "./results/tables"
if not os.path.exists(table_out_path):
    os.makedirs(table_out_path)

# file paths
file_2050 = "./preprocessed_data/df2050_ene.csv"
file_2050_ssp2 = "./preprocessed_data/df2050_ssp2_ene.csv"
file_2020 = "./preprocessed_data/df2020_ene.csv"

# columns : 'Units', 'region', 'fuel', 'value'

df_2050 = pd.read_csv(file_2050)
df_2050 = df_2050[df_2050['fuel'] != 'j traditional biomass']

df_2050_ssp2 = pd.read_csv(file_2050_ssp2)
df_2050_ssp2 = df_2050_ssp2[df_2050_ssp2['fuel'] != 'j traditional biomass']

df_2020 = pd.read_csv(file_2020)
df_2020 = df_2020[df_2020['fuel'] != 'j traditional biomass']


subplot_title = ['a', 'b', 'c', 'd', 'e']
subplot_title = [i.capitalize() for i in subplot_title]
x = [0.2, 0.3, 0.36]


def draw_stacked_barchart(categories, values_list, labels, ax, region):
    # set color
    # TODO: make one for bar chart, option 4 looks good
    def set_colors(colors, ax=None):
        ax.set_prop_cycle('color', colors)

    color_palette = sns.color_palette("Set3", 10)
    set_colors(color_palette, ax)

    width = 0.05

    # colors = ['#ADD8E6', '#FFFFE0', '#27E630']  # light blue and light yellow
    # ax.set_prop_cycle(color=colors)

    # Data for the bars
    # Create an array for the x positions of the bars

    # Plot the bars
    bar_props = []
    bottom_value = np.zeros((3,))
    for i, value in enumerate(values_list):
        bars = ax.bar(x, value, bottom=bottom_value, width=width, edgecolor='black', linewidth=0.2, label=labels[i])
        bottom_value += value
        bar_props.append(bars)
        for bar in bars:
            # add edge to bar
            pass

    # Add percentage labels
    for i, bar in enumerate(bar_props):
        col_val = values_list[i]
        col_sum = col_val.sum()
        for m, rect in enumerate(bar):
            val = col_val[m]
            rect_height = rect.get_height()
            # Get the height of the bar relative to the plot
            abs_height = ax.transData.transform((0, rect.get_height()))[1]
            # abs_height = rect.get_window_extent().height

            xpos = rect.get_x() + rect.get_width() / 2.0
            ypos = rect.get_y() + rect_height / 2.0
            # ratio = abs(col1['values'][m] / sum_by_year1[m])
            if region == "China":
                abs_height = abs_height / 5
            if region == "South Asia":
                abs_height = abs_height * 1.2
            if abs_height > 1800:
                ax.text(xpos, ypos, '{:.1f}'.format(val), ha='center', va='center', color='black',
                        fontweight='normal', fontsize=5)

    # add 2050 label
    ax.text(0.70, -0.09, '2050', ha='center', va='center', color='black',
            fontweight='bold', fontsize=5, transform=ax.transAxes)

    # add 2020 label
    ax.text(0.15, -0.09, '2020', ha='center', va='center', color='black',
            fontweight='bold', fontsize=5, transform=ax.transAxes)

    xtick_labels = ax.get_xticklabels()
    # xtick_labels[0].set_weight('bold')


def draw_figure():
    # Create a sample data
    fuels = pd.unique(df_2050['fuel'].unique())
    # fix labels

    fuels = [name[2:].title() for name in fuels]


    # draw_sbs_barchart(fuels, values1, values2, values3, legends=('2020', 'SSP2', 'SSP1'))
    categories = ['BAU', 'BAU', 'OS']

    # plot subplot for energy demand in each region
    # fig.suptitle('CO2 Emissions by Region and Year', fontsize=16)
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(FIG_DOUBLE_WIDTH, FIG_DOUBLE_WIDTH * 0.65), dpi=600)
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

    for i, region in enumerate(df_2050['region'].unique()):
        ax = axs[i]

        df_2050_local = df_2050[df_2050['region'] == region]
        df_2050_ssp2_local = df_2050_ssp2[df_2050_ssp2['region'] == region]
        df_2020_local = df_2020[df_2020['region'] == region]
        # aggregate value(sum) by fuel
        fuel_by_value_2050 = pd.pivot_table(df_2050_local, index=['fuel'], values=['value'], aggfunc=np.sum)
        fuel_by_value_2050_ssp2 = pd.pivot_table(df_2050_ssp2_local, index=['fuel'], values=['value'], aggfunc=np.sum)
        fuel_by_value_2020 = pd.pivot_table(df_2020_local, index=['fuel'], values=['value'], aggfunc=np.sum)

        values1 = fuel_by_value_2020['value']
        values2 = fuel_by_value_2050_ssp2['value']
        values3 = fuel_by_value_2050['value']

        values_list = np.vstack([values1, values2, values3]).T

        draw_stacked_barchart(categories, values_list, fuels, ax, region)

        # Add labels and title
        ax.set_ylabel('Energy consumption (EJ)')
        # Customize the x-axis tick labels
        ax.set_xticks(x, categories)


        # set region as title
        region = region if region != "Africa_Western" else "Western Africa"
        ax.set_title(region, fontsize=6)

        # set a,b,c,d,e
        # give subplot a,b, c, d labels
        title = subplot_title[i]
        ax.text(-0.1, 1.1, title, transform=ax.transAxes, fontsize=7, fontweight='bold', va='top')

    # Add custom legend
    handles, labels = axs[0].get_legend_handles_labels()
    nlabels = list(range(0, len(handles)))

    # handle legend
    fig.legend([handles[i] for i in nlabels][::-1],
               [labels[i].title() for i in nlabels][::-1],
               loc='center right', ncol=2,
               bbox_to_anchor=(0.92, 0.75), fontsize=7)

    plt.tight_layout()
    save('energy_demand_by_region')
    plt.show()


# get_table()
draw_figure()
