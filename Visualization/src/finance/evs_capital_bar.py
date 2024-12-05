import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# Assuming we have the same data structure as before, with the data loaded into a DataFrame 'data'

data = pd.read_csv('/Users/pramish/Desktop/Codes/netzero/Visualization/preprocessed_data/finance/capital/ssp1_developing_capital_investment_evs.csv')

# First, we need to set the style for the plots
plt.style.use('seaborn-ticks')

# Define figure size and DPI as per Nature's guidelines
fig = plt.figure(figsize=(8.27, 11.69), dpi=300)  # A4 size paper as an example
gs = GridSpec(nrows=3, ncols=2, figure=fig, wspace=0.4, hspace=0.6)

# Subplot titles as per Nature's guidelines
subplot_titles = ['a', 'b', 'c', 'd', 'e']

# Assuming 'data' has the same structure as in the previous figure
# We will create a stacked bar plot for each region
for i, region in enumerate(data['region'].unique()):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    region_data = data[data['region'] == region]

    # Pivot the data for the stacked bar plot
    pivot_data = region_data.pivot_table(index='Year', columns='technology', values='value', fill_value=0)
    pivot_data.plot(kind='bar', stacked=True, ax=ax)

    # Set the title with the corresponding subplot label (a, b, c, d, e)
    ax.set_title(f'{subplot_titles[i]} {region}', loc='left', fontweight='bold')

    # Set the xlabel and ylabel
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')

    # Remove the legend for individual plots to place a combined legend later
    ax.get_legend().remove()

    # Customize the plot to adhere to Nature's guidelines
    ax.tick_params(axis='x', which='major', labelsize=8)
    ax.tick_params(axis='y', which='major', labelsize=8)

    # Set the xtick labels if they are specific
    ax.set_xticklabels(pivot_data.index, rotation=0)

# Create custom legends from the last ax used, assuming all have the same items
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=8)

# Save the figure in a high-quality format
# plt.savefig('/mnt/data/stacked_bar_chart.png', format='png', dpi=300, bbox_inches='tight')

# Display the figure
plt.show()
