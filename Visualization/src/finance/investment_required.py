import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming the required modules and functions from constants and helpers.io are available
from constants import FIG_SINGLE_WIDTH, mm2inch, FIG_SIZE_SINGLE, DISPLAY_DIP, DPI, FIG_DOUBLE_WIDTH
from helpers.io import save

sys.path.append("../")

plt.style.use('./styles/bar_chart_style.mplstyle')

# File paths (assuming they exist in the specified directory)
gdp_df = "./preprocessed_data/finance/gdp.csv"
policy_df = "./preprocessed_data/finance/policy_cost.csv"

gdp_df = pd.read_csv(gdp_df, index_col=0)
# gdp_df = gdp_df[gdp_df['Year'] > 2015]
policy_df = pd.read_csv(policy_df, index_col=0)

# replace 'Africa_Western' region name to 'Western Africa'
gdp_df['region'] = gdp_df['region'].replace('Africa_Western', 'Western Africa')
policy_df['region'] = policy_df['region'].replace('Africa_Western', 'Western Africa')


# Define the function to calculate the trapezoidal area
def calculate_investment(data, region, year_start, year_end):
    region_data = data[data['region'] == region]
    relevant_data = region_data[(region_data['Year'] >= year_start) & (region_data['Year'] <= year_end)]
    area = np.trapz(relevant_data['value'], relevant_data['Year'])
    return area

# Create the plot using the 'ax' object
fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, 1.2 * FIG_SINGLE_WIDTH), dpi=DPI)

ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

# choose color theme
sns.set_palette("muted")

def plot_bar(ax):
    # Calculate the investment required for each region for the years 2030, 2050, and 2085
    years = [2030, 2050, 2085]
    regions = policy_df['region'].unique()

    investment_data = []
    for region in regions:
        for year in years:
            investment = calculate_investment(policy_df, region, 2025, year)
            # if region == "Africa_Western":
            #     region = "Western Africa"
            investment_data.append({
                'Region': region,
                'Year': year,
                'Investment Required': (investment * 2.35) / 1e6  # 2023 trillion
            })

    # Convert the calculated data into a DataFrame
    investment_df = pd.DataFrame(investment_data)

    # sort investment_df by 'Investment Required' in 2085 descending order
    investment_df = investment_df.sort_values(by=['Investment Required'], ascending=False)

    bar_plot = sns.barplot(x='Investment Required', y='Region', hue='Year', data=investment_df, orient='h', ax=ax)

    # ax.set_title('Investment Required for Top 5 Regions in 2030, 2050, and 2085')
    ax.set_xlabel('Investment required (2023 Trillion $)', fontsize='medium')

    # don't show ylabel
    ax.set_ylabel('')

    ax.legend(title='')

    # Show values on the bars
    for p in bar_plot.patches:
        ax.text(p.get_width() + 0.2, p.get_y() + p.get_height() / 2.,
                '{:1.0f}'.format(p.get_width()) if p.get_width() > 1 else '{:1.3f}'.format(p.get_width()),
                ha='left', va='center', fontsize='4')

    # add `a` label
    ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize='medium', fontweight='bold', va='top')

    ax.tick_params(axis='x', which='major', length=1)
    ax.tick_params(axis='y', which='major', length=0)

    #increase legend handle length

    ax.legend(labelspacing=0.5, handlelength=1.5, fontsize='medium')

def plot_gdp(ax):
    # plot % of GDP trend from 2015 to 2100 for all regions
    gdp = (gdp_df[gdp_df['Year'] > 2015]).set_index(['region', 'Year'])
    policy = (policy_df[policy_df['Year'] > 2015]).set_index(['region', 'Year'])
    percentage = (policy['value'] / gdp['value']) * 100
    percentage = percentage.reset_index()
    lineplot = sns.lineplot(data=percentage, x='Year', y='value', hue='region')
    # lineplot.legend(title='', labelspacing=0.1)

    ax.set_xlabel('Year', fontsize='medium')
    ax.set_ylabel('Investment required (% of GDP)', fontsize='medium')

    # add `b` label
    ax.text(-0.15, 1.05, 'B', transform=ax.transAxes, fontsize='medium', fontweight='bold', va='top')

    ax.tick_params(axis='x', which='major', length=1)
    # ax.tick_params(axis='y', which='major', length=0)


    # arange legend
    # Get handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reorder handles and labels as needed
    order = [2, 1, 3, 4, 0]
    handles = [handles[i] for i in order]
    labels = [labels[i] for i in order]

    # Create new legend
    ax.legend(handles, labels, labelspacing=0.5, fontsize='medium')
    # ax.legend(labelspacing=0.5, fontsize='medium')


plot_bar(ax1)
plot_gdp(ax2)

# reduce legend margin
# plt.legend(labelspacing=0.09)

plt.tight_layout()

save('investment_required')
plt.show()
