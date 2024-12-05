from os.path import join
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming the required modules and functions from constants and helpers.io are available
from constants import FIG_SINGLE_WIDTH, mm2inch
from helpers.io import save

sys.path.append("../")

plt.style.use('./styles/plot.mplstyle')

# File paths (assuming they exist in the specified directory)
rew_non_rew_spa1 = "./preprocessed_data/energy and emission/spa1_renewable_non_renewable_trend.csv"
rew_non_rew_ssp2 = "./preprocessed_data/energy and emission/ssp2_renewable_non_renewable_trend.csv"

df_spa1 = pd.read_csv(rew_non_rew_spa1, index_col=0)
df_spa1 = df_spa1[df_spa1['Year'] > 2000]
df_ssp2 = pd.read_csv(rew_non_rew_ssp2, index_col=0)
df_ssp2 = df_ssp2[df_ssp2['Year'] > 2000]


def plot():
    # Create a new figure
    fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(55)), dpi=600)

    renewable_color = '#D87700'
    non_renewable_color = '#659AB0'

    # renewable_color = '#B26200'
    # non_renewable_color = '#436775'

    # Add a new subplot to the figure
    ax = fig.add_subplot(111)
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    year = df_spa1['Year'].unique()
    line_ssp1_renewable, = ax.plot(year,
                                   df_spa1[(df_spa1['fuel'] == 'renewable')]['value'],
                                   color=renewable_color, linewidth=1)
    line_ssp1_nonrenewable, = ax.plot(year, df_spa1[(df_spa1['fuel'] == 'non-renewable')][
        'value'], label="SSP1 Non-Renewable", color=non_renewable_color, )

    # historic data
    ax.plot(year[year <= 2015], df_spa1[(df_spa1['fuel'] == 'renewable') & (df_spa1['Year'] <= 2015)]['value'],
            color='gray', linewidth=3, alpha=0.3)

    ax.plot(year[year <= 2015], df_spa1[(df_spa1['fuel'] == 'non-renewable') & (df_spa1['Year'] <= 2015)]['value'],
            color='gray', linewidth=3, alpha=0.3)

    ax.text(2010, 130, "Historical Fuel \nTrend", color="black", fontsize=4,
            ha="center")

    line_ssp2_renewable, = ax.plot(year[year >= 2015],
                                   df_ssp2[(df_ssp2['fuel'] == 'renewable') & (df_spa1['Year'] >= 2015)]['value'],
                                   color=renewable_color, linestyle='--')  # Making SSP2 line dotted

    line_ssp2_nonrenewable, = ax.plot(year[year >= 2015],
                                      df_ssp2[(df_ssp2['fuel'] == 'non-renewable') & (df_spa1['Year'] >= 2015)][
                                          'value'],
                                      label="SSP2 Non-Renewable", color=non_renewable_color, linestyle="--")

    # Adding the vertical lines at 2050 and 2085 showing the percentage difference
    value_2050_ssp1_renewable = df_spa1[(df_spa1['Year'] == 2050) & (df_spa1['fuel'] == 'renewable')]['value'].values[0]
    value_2050_ssp2_renewable = df_ssp2[(df_ssp2['Year'] == 2050) & (df_ssp2['fuel'] == 'renewable')]['value'].values[0]
    value_2085_ssp1_renewable = df_spa1[(df_spa1['Year'] == 2085) & (df_spa1['fuel'] == 'renewable')]['value'].values[0]
    value_2085_ssp2_renewable = df_ssp2[(df_ssp2['Year'] == 2085) & (df_ssp2['fuel'] == 'renewable')]['value'].values[0]

    value_2050_ssp1_non_renewable = \
    df_spa1[(df_spa1['Year'] == 2050) & (df_spa1['fuel'] == 'non-renewable')]['value'].values[0]
    value_2050_ssp2_non_renewable = \
    df_ssp2[(df_ssp2['Year'] == 2050) & (df_ssp2['fuel'] == 'non-renewable')]['value'].values[0]
    value_2085_ssp1_non_renewable = \
    df_spa1[(df_spa1['Year'] == 2085) & (df_spa1['fuel'] == 'non-renewable')]['value'].values[0]
    value_2085_ssp2_non_renewable = \
    df_ssp2[(df_ssp2['Year'] == 2085) & (df_ssp2['fuel'] == 'non-renewable')]['value'].values[0]

    # Calculating percentage differences
    diff_2050 = (value_2050_ssp1_renewable - value_2050_ssp2_renewable) / value_2050_ssp2_renewable * 100
    diff_2085 = (value_2085_ssp1_renewable - value_2085_ssp2_renewable) / value_2085_ssp2_renewable * 100

    diff_2050_non_renewable = (
                                          value_2050_ssp1_non_renewable - value_2050_ssp2_non_renewable) / value_2050_ssp2_non_renewable * 100
    diff_2085_non_renewable = (
                                          value_2085_ssp1_non_renewable - value_2085_ssp2_non_renewable) / value_2085_ssp2_non_renewable * 100

    # Draw the vertical lines at 2050 and 2085
    ax.axvline(x=2050, color='black', linestyle='--', alpha=0.8)
    ax.axvline(x=2085, color='black', linestyle='--', alpha=0.8)

    ax.text(2050 + 4, (value_2050_ssp2_renewable + (value_2050_ssp1_renewable - value_2050_ssp2_renewable) / 2),
            f"+{diff_2050:.2f}%", color="black", fontsize=4,
            ha="center")
    ax.text(2050 + 4,
            (value_2050_ssp2_non_renewable + (value_2050_ssp1_non_renewable - value_2050_ssp2_non_renewable) / 2),
            f"{diff_2050_non_renewable:.2f}%", color="black", fontsize=4,
            ha="center")
    ax.plot(2050, value_2050_ssp2_renewable, marker='o', color=renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2050, value_2050_ssp2_non_renewable, marker='o', color=non_renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2050, value_2050_ssp1_renewable, marker='o', color=renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2050, value_2050_ssp1_non_renewable, marker='o', color=non_renewable_color, markersize=2.0, alpha=0.8)

    # ax.plot([2085, 2085], [max(y_2085_ssp1, y_2085_ssp2), min(y_2085_ssp1, y_2085_ssp2)], color='black', linestyle='-',
    #         linewidth=0.5)
    ax.text(2085 + 4, (value_2085_ssp2_renewable + (value_2085_ssp1_renewable - value_2085_ssp2_renewable) / 2),
            f"+{diff_2085:.2f}%", color="black", fontsize=4,
            ha="center")
    ax.text(2085 + 4,
            (value_2085_ssp2_non_renewable + (value_2085_ssp1_non_renewable - value_2085_ssp2_non_renewable) / 2),
            f"{diff_2085_non_renewable:.2f}%", color="black", fontsize=4,
            ha="center")
    ax.plot(2085, value_2085_ssp2_renewable, marker='o', color=renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2085, value_2085_ssp2_non_renewable, marker='o', color=non_renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2085, value_2085_ssp1_renewable, marker='o', color=renewable_color, markersize=2.0, alpha=0.8)
    ax.plot(2085, value_2085_ssp1_non_renewable, marker='o', color=non_renewable_color, markersize=2.0, alpha=0.8)

    # x-axis labels to be 10-year intervals
    ax.set_xticks(np.arange(min(year), max(year) + 1, 10))

    # Legend modifications
    legend_handles = [
        plt.Line2D([0], [0], color='black'),  # Green for Renewable and bold for SSP1
        plt.Line2D([0], [0], color='black', linestyle='--', linewidth=0.5)  # Blue for Non-Renewable and dotted for SSP2
    ]
    legend_labels = ['OS', 'BAU']  # Update legend labels

    # Additional legends for renewable and non-renewable
    legend_handles.extend([
        plt.Line2D([0], [0], color=renewable_color),  # Green for Renewable
        plt.Line2D([0], [0], color=non_renewable_color)  # Blue for Non-Renewable
    ])
    legend_labels.extend(['Renewable', 'Non-Renewable'])  # Additional legend labels

    ax.legend(legend_handles, legend_labels, loc="upper left")

    # # Add text annotations for "Renewable" and "Non-Renewable"
    # ax.text(2020, 65, "Renewable", color="black", fontsize=4, ha="center", rotation=45)
    # ax.text(2020, 180, "Non-Renewable", color="black", fontsize=4, ha="center", rotation=45)

    plt.xlabel("Year")
    plt.ylabel("Energy (EJ)")

    plt.tight_layout()
    save('renewable_non-renewable_trend')
    plt.show()


plot()
