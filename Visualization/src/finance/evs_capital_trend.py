import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

from constants import FIG_SINGLE_WIDTH

plt.style.use('./styles/plot.mplstyle')

data = pd.read_csv(
    '/Users/pramish/Desktop/Codes/netzero/Visualization/preprocessed_data/finance/capital/ssp1_developing_capital_investment_evs.csv')

data.loc[data['region']=='Africa_Western', "region"] = "Western Africa"
data = pd.pivot_table(data, index=['Year', 'region'], values='value', aggfunc=np.sum).reset_index()
# First, we need to set the style for the plots

# Define figure size and DPI as per Nature's guidelines
fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, FIG_SINGLE_WIDTH * 0.6), dpi=300)  # A4 size paper as an example
# Plotting each region separately to show trends using line plot
# Plotting
sns.lineplot(data=data, x='Year', y='value', hue='region')

# Setting the spine visibility
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)



# Enhancing the plot
plt.title('Capital Investment for EVs')
plt.xlabel('Year')
plt.ylabel('Million US $ (1975)')
plt.legend(loc='upper left')
plt.tight_layout()

# Create custom legends from the last ax used, assuming all have the same items
# handles, labels = ax.get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=8)

# Save the figure in a high-quality format
# plt.savefig('/mnt/data/stacked_bar_chart.png', format='png', dpi=300, bbox_inches='tight')

# Display the figure
plt.show()
