from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.io import save

sys.path.append("../")
from constants import FIG_SINGLE_WIDTH, mm2inch
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
df_2050_ssp2 = pd.read_csv(file_2050_ssp2)
df_2020 = pd.read_csv(file_2020)

# aggregate value(sum) by fuel
fuel_by_value_2050 = pd.pivot_table(df_2050, index=['fuel'], values=['value'], aggfunc=np.sum)
# fuel_by_value_2050.drop(index='j traditional biomass', inplace=True)
fuel_by_value_2050_ssp2 = pd.pivot_table(df_2050_ssp2, index=['fuel'], values=['value'], aggfunc=np.sum)
# fuel_by_value_2050_ssp2.drop(index='j traditional biomass', inplace=True)
fuel_by_value_2020 = pd.pivot_table(df_2020, index=['fuel'], values=['value'], aggfunc=np.sum)
# fuel_by_value_2020.drop(index='j traditional biomass', inplace=True)

'''
Sample output: 
                   value
fuel                    
a oil          49.337288
b natural gas  42.532221
c coal         34.211609
d biomass      67.806330
e nuclear      28.004743
'''


def get_table():
    cols = ['Energy Source', '2050 % contrib', '2020 % contrib']
    df = pd.DataFrame(columns=cols)
    for i, fuel in enumerate(pd.unique(fuel_by_value_2050.index)):
        # find percentage by each fuel
        contrib_2050 = (fuel_by_value_2050.loc[fuel].value / fuel_by_value_2050['value'].sum()) * 100
        contrib_2020 = (fuel_by_value_2020.loc[fuel].value / fuel_by_value_2020['value'].sum()) * 100
        new_row = [fuel, contrib_2050, contrib_2020]
        df.loc[i] = new_row

    df.to_csv(join(table_out_path, 'energy_sources and their contrib in 2050, 2020.csv'))


def draw_sbs_barchart(fuel, v1, v2, v3, legends):
    # v1: 2020, v2: 2050 ssp1, v3: 2050 ssp2
    # Set the X axis
    x = np.arange(len(fuel))

    # Create the figure and axis
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(60)))
    ax = plt.subplot(111)
    # set color
    # TODO: make one for bar chart, option 4 looks good
    set_stacked_area_colors(ax, option_id=2)
    width = 0.25
    # Plot the first set of bars

    bars1 = ax.bar(x - width, v1, edgecolor='black', width=width, color='pink', linewidth=0.75)

    # Plot the second set of bars
    bars2 = ax.bar(x, v2, edgecolor='black', width=width, color='skyblue', linewidth=0.75)
    bars3 = ax.bar(x + width, v3, edgecolor='black', width=width, color='#9061BF', linewidth=0.75)

    colors = ['#ADD8E6', '#FFFFE0', '#27E630']  # light blue and light yellow

    ax.set_prop_cycle(color=colors)

    # Calculate the percentage difference between the two bars for each x label
    diff_percentages_ssp2 = []
    diff_percentages_ssp1 = []
    for i in range(len(fuel)):
        diff_ssp2 = ((v2[i] - v1[i]) / v1[i]) * 100
        diff_ssp1 = ((v3[i] - v1[i]) / v1[i]) * 100
        diff_percentages_ssp2.append(diff_ssp2)
        diff_percentages_ssp1.append(diff_ssp1)

    # Find the highest bar value between two for each x label
    highest_value_ssp2 = []
    highest_value_ssp1 = []
    for i in range(len(fuel)):
        highest_value_ssp2.append(max(v1[i], v2[i]))
        highest_value_ssp1.append(max(v1[i], v3[i]))

    # Add the percentage difference to the bar which is highest between two
    for i, (bar1, bar2, bar3) in enumerate(zip(bars1, bars2, bars3)):
        ax.text(bar2.get_x() + bar2.get_width() / 2 - width / 2, highest_value_ssp2[i] + 1,
                '{:.0f}%'.format(diff_percentages_ssp2[i]), ha='center', va='center', fontsize=4)

        ax.text(bar3.get_x() + bar2.get_width() / 2 + width / 2, v3[i] + 1,
                '{:.0f}%'.format(diff_percentages_ssp1[i]), ha='center', va='center', fontsize=4)

    # Add labels and titles
    # ax.set_xlabel('Fuel')
    ax.set_ylabel('Energy (EJ)')

    ax.set_xticks(x - 0.15)
    ax.set_xticklabels(fuel, rotation=90)
    ax.legend((bars1[0], bars2[0], bars3[0]), legends)

    # Show the chart
    plt.tight_layout()
    plt.show()


def draw_stacked_barchart(categories, values_list, labels):
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(60)))
    ax = plt.subplot(111)
    # set color
    # TODO: make one for bar chart, option 4 looks good
    def set_colors(colors, ax=None):
        ax.set_prop_cycle('color', colors)
    color_palette = sns.color_palette("Set3", 10)
    set_colors(color_palette, ax)


    width = 0.1

    # colors = ['#ADD8E6', '#FFFFE0', '#27E630']  # light blue and light yellow
    # ax.set_prop_cycle(color=colors)

    # Data for the bars
    # Create an array for the x positions of the bars
    x = [0.2, 0.4, 0.55]

    # Plot the bars
    bar_props = []
    bottom_value = np.zeros((3,))
    for i, value in enumerate(values_list):
        bars = plt.bar(x, value, bottom=bottom_value, width=width,edgecolor='black',linewidth=0.2, label=labels[i])
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
            height = rect.get_height()
            xpos = rect.get_x() + rect.get_width() / 2.0
            ypos = rect.get_y() + height / 2.0
            # ratio = abs(col1['values'][m] / sum_by_year1[m])
            if height > 12:
                ax.text(xpos, ypos - 1, '{:.1f}'.format(val), ha='center', va='center', color='black',
                        fontweight='normal', fontsize=5)

    # add 2050 label
    ax.text(0.475, -35, '2050', ha='center', va='center', color='black',
            fontweight='bold', fontsize=5)

    # add 2020 label
    ax.text(0.2, -35, '2020', ha='center', va='center', color='black',
            fontweight='bold', fontsize=5)

    # make 2020 bold
    # Get the xtick labels
    xtick_labels = plt.xticks()[1]
    # xtick_labels[0].set_weight('bold')

    # Add labels and title
    plt.ylabel('Energy consumption (EJ)')
    # Customize the x-axis tick labels
    plt.xticks(x, categories)

    # render reverse legend
    # Get the legend handles and labels
    handles, labels = ax.get_legend_handles_labels()

    # Reverse the order of handles and labels
    handles = handles[::-1]
    labels = labels[::-1]

    # Create the reversed legend
    plt.legend(handles, labels, bbox_to_anchor=(1.4, 0.5), loc='center right', ncol=1)

    plt.subplots_adjust(right=1 - 0.28)


def draw_figure():
    # Create a sample data
    fuels = pd.unique(fuel_by_value_2050.index)
    # fix labels

    fuels = [name[2:].title() for name in fuels]
    values1 = fuel_by_value_2020['value']
    values2 = fuel_by_value_2050_ssp2['value']
    values3 = fuel_by_value_2050['value']

    # draw_sbs_barchart(fuels, values1, values2, values3, legends=('2020', 'SSP2', 'SSP1'))
    categories = ['BAU', 'BAU', 'OS']
    values_list = np.vstack([values1, values2, values3]).T
    draw_stacked_barchart(categories, values_list, fuels)


# get_table()
draw_figure()
save('energy_n_emission')
plt.show()