'''
plot that is to be inclued in the tech section's intro
its purpose is to show the level of increment required for CCS, EVs and H2
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors

from constants import FIG_DOUBLE_WIDTH

from helpers.colors import set_colors
from helpers.io import save

plt.style.use('./styles/bar_stacked_sbs.mplstyle')


def sbysbar(categories, values, colors, ax):
    x = np.arange(len(categories))  # the label locations
    width = 0.35  # the width of the bars

    bars = []
    for value, color in zip(values, colors):
        bar = ax.bar(x - width / 2, values1, width, label='Series 1', color=color)
        bars.append(bar)
        # bars2 = ax.bar(x + width / 2, values2, width, label='Series 2', color='red')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Value axis')
    ax.set_title('Bar chart example')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Label with the actual value on top of each bar
    def autolabel(bars):
        """Attach a text label above each bar in *bars*, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    for bar in bars:
        autolabel(bar)



fig, ax = plt.subplots()

# Sample data
categories = ['Category A', 'Category B', 'Category C']
values1 = [3, 7, 2]
values2 = [4, 3, 6]

fig.tight_layout()

# Display the plot
plt.show()