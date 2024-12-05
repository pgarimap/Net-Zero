import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import colorcet as cc

# Load the data from CSV files
from matplotlib.lines import Line2D

from constants import FIG_SINGLE_WIDTH, FIG_DOUBLE_WIDTH
from helpers.io import save

plt.style.use('./styles/stacked_area.mplstyle')

file_spa1 = 'preprocessed_data/technology/h2_demand_by_sector_5_regions_spa1.csv'
file_ssp2 = 'preprocessed_data/technology/h2_demand_by_sector_5_regions_ssp2.csv'
df_spa1 = pd.read_csv(file_spa1)
df_ssp2 = pd.read_csv(file_ssp2)

# Rename 'Africa_Western' to 'Western Africa'
df_spa1['region'] = df_spa1['region'].replace('Africa_Western', 'Western Africa')
df_ssp2['region'] = df_ssp2['region'].replace('Africa_Western', 'Western Africa')


sectors = df_spa1['sector'].unique()
colors = sns.color_palette(cc.glasbey_light, n_colors=len(sectors))


# Define the plotting function
def plot_stacked_area(df, ax, title, set_axis_labels=True):
    # sectors = df['sector'].unique()
    years = sorted(set(df['Year']).union({2020}))  # Including 2020
    # colors = sns.color_palette("Paired", len(sectors))

    area_data = pd.DataFrame(index=years, columns=sectors)
    for sector in sectors:
        sector_data = df[df['sector'] == sector]
        if len(sector_data) > 1:
            for year in years:
                value = sector_data[sector_data['Year'] == year]['value']
                area_data.at[year, sector] = value.values[0] if not value.empty else 0

            area_data = area_data.apply(pd.to_numeric)

    ax.stackplot(years, area_data.values.T, labels=sectors, colors=colors,
                 alpha=0.7,
             edgecolor='black',
             linewidth=0.3)
    ax.set_title(title, color='black', fontsize=7, fontweight='bold')
    if set_axis_labels:
        # ax.set_xlabel('Year', color='black')
        ax.set_ylabel('Energy consumption (EJ)', color='black', fontweight='bold', fontsize=6)
    ax.tick_params(axis='x', direction='out', colors='black')
    ax.tick_params(axis='y', direction='out', colors='black')
    ax.grid(False)  # Removing grid lines


# Create the figure
fig, axs = plt.subplots(3, 4, figsize=(FIG_DOUBLE_WIDTH, FIG_DOUBLE_WIDTH * 0.9))
# Method 1: Remove the axes completely
axs[-1, -2].remove()  # Removes the second-to-last axis
axs[-1, -1].remove()  # Removes the last axis
# Plotting the data
for i, region in enumerate(df_spa1['region'].unique()):
    row = i // 2
    col = i % 2
    col = col * 2
    set_axis_labels = col == 0
    plot_stacked_area(df_spa1[df_spa1['region'] == region], axs[row, col], f'OS: {region}', set_axis_labels=set_axis_labels)
    plot_stacked_area(df_ssp2[df_ssp2['region'] == region], axs[row, col + 1], f'BAU: {region}', set_axis_labels=False)

# Adjusting the legend and placing it on the right side of the figure
handles, labels = axs[2, 0].get_legend_handles_labels()
# fix laels
for i, label in enumerate(labels):
    if label == "N fertilizer":
        labels[i] = "Fertilizer"
    labels[i] = labels[i].capitalize()

handles = handles[::-1]
labels = labels[::-1]

leg = fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(0.98, 0.05), frameon=False, fancybox=False,
                 ncol=2, handletextpad=1.5, fontsize=7)

for item in leg.legendHandles:
    item.set_width(10)  # Setting the legend marker width

# Get the bounds of the figure
fig_width, fig_height = fig.get_size_inches()*fig.dpi
#
# for i in range(2):  # Only two horizontal lines needed between three rows
#     # Get the position of the axes at the bottom of the row we want to draw a line under
#     pos = axs[i+1, 0].get_position()
#     # Draw a line at the bottom of this row of axes
#     line = Line2D([0, 1], [pos.y0,  pos.y0], transform=fig.transFigure, color='k', linestyle='--', linewidth=1)
#     fig.add_artist(line)
#
# for j in range(1, 4, 2):  # Only two vertical lines needed to separate the column pairs
#     # Get the position of the axes at the right of the column pair
#     pos = axs[0, j].get_position()
#     # Draw a line at the right of this column of axes
#     line = Line2D([pos.x1, pos.x1], [0, 1], transform=fig.transFigure, color='k', linestyle='--', linewidth=1)
#     fig.add_artist(line)

plt.tight_layout()

save('hydrogen_demand_by_region')
plt.show()
# Save the figure as a PNG file
# plt.savefig('hydrogen_demand_stacked_area_charts_complete.png', dpi=300, bbox_inches='tight')
