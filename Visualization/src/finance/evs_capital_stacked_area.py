
import math

import numpy as np

import helpers  # sets gpu backend
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.transforms as transforms

# local imports
from helpers.colors import set_stacked_area_colors
from helpers.io import save
from constants import *

plt.style.use('./styles/stacked_area.mplstyle')

data = pd.read_csv(
    '/Users/pramish/Desktop/Codes/netzero/net-zero-codes/Visualization/preprocessed_data/finance/capital/ssp1_developing_capital_investment_evs.csv')

data = data[data['Year'] > 2000]
# factor inflation
data['value'] = data['value'] * 5.71

data.loc[data['region'] == 'Africa_Western', "region"] = "Western Africa"

data = pd.pivot_table(data, index=['Year'], values='value', columns=['region'], aggfunc=np.sum).reset_index()

df = data
cols = [df[col_name] for col_name in df.columns[1:]]
labels = df.columns[1:]

fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, 0.5 * FIG_SINGLE_WIDTH), dpi=600)
ax = plt.subplot(111)
# set color
set_stacked_area_colors(ax, option_id=2)

ax.stackplot(df['Year'], *cols,
             labels=labels,
             edgecolor='black',
             linewidth=0.3
             )
plt.xlabel('Year',  fontsize=5)
plt.ylabel('Investment required (2023 $/GJ)', fontsize=5)

# draw vertical lines
trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

# ax.set_ylim([0, 1400])
# ax.margins(x=0.08)
# ax.set_xlim(right=2025)

# Adjusting xtick and ytick font sizes
plt.xticks(fontsize=5)
plt.yticks(fontsize=5)

def annotate_change(year, prev_year):
    te1 = df[df["Year"] == prev_year].iloc[0][1:].sum()
    te2 = df[df["Year"] == year].iloc[0][1:].sum()
    interval = year - prev_year
    change = ((te2 - te1) / interval)
    ax.text(
        (year - interval / 2),
        0.82,
        f"{change:.02f}%/yr",
        ha="center",
        # va="top",
        transform=trans,
    )


def vertical_line(year, interval):
    ax.axvline(year, ymin=0, ymax=0.98,
               linewidth='0.4',
               ls="--",
               color='black', alpha=0.8)

    # total emission at top of vertical line
    ax.text(
        year,  # start position in year
        0.99,  # y control
        '$ ' + str(np.ceil(df.iloc[i][1:].sum()).astype(int)),
        ha="center",
        # va="top",
        transform=trans,
        fontsize=4
    )


def add_labels(year):
    col_names = df.columns[1:]
    total_y = 0
    for col in col_names:
        row = df[df["Year"] == year].iloc[0]
        y = row[col]
        percentage = (y / (row[1:].sum())) * 100
        percentage = math.ceil(percentage)
        total_y = total_y + y
        ax.text(
            year,  # start position in year
            total_y - y / 4,  # y control
            str(percentage) + "%",
            ha="left",
            va="top",
            fontsize=4,
        )


for i, year in enumerate(df['Year']):
    interval = 30  # in years
    if year % interval == 0:
        vertical_line(year, interval)
        if year > 2015:
            add_labels(year)
        # # %change
        # if i != 0:
        #     annotate_change(year, year - interval)

    if i == len(df) - 1 and year % interval != 0:
        vertical_line(year, interval)
        annotate_change(year, year - (year % interval))

# handle legend

# horizontal bottom legend
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + 0.05,
#                  box.width, box.height])
# ax.legend(loc='lower center',
#           bbox_to_anchor=(0.5, -0.2),
#           ncol=len(cols)
#           )

# vertical right legend
handles, labels = ax.get_legend_handles_labels()

x, y = trans.transform([2105, 50])
boxx, boxy = ax.transAxes.inverted().transform([x, y])
# reverse the legend order and adjust position of legend
ax.legend(handles[::-1], labels[::-1],
          loc='center left',
          bbox_to_anchor=(boxx, 0.5),
          ncol=1,
          fontsize=5,
          )

plt.subplots_adjust(top=0.9)
plt.tight_layout()
save('evs_investment')
plt.show()
