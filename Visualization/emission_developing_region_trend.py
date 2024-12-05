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


def get_data():
    df = pd.read_csv("./preprocessed_data/energy and emission/co2_by_region.csv", index_col=0)
    df.loc[df['region']=='Africa_Western', 'region'] = 'Western Africa'
    data = pd.pivot_table(df, index='Year', values='value', columns=['region'], aggfunc=np.sum)
    data.reset_index(inplace=True)
    data = data[data['Year'] <= 2015]
    return data


df = get_data()
cols = [df[col_name] for col_name in df.columns[1:]]
labels = df.columns[1:]

fig = plt.figure(figsize=(FIG_SINGLE_WIDTH, FIG_SINGLE_WIDTH * 0.7), dpi=600)
ax = plt.subplot(111)
# set color
set_stacked_area_colors(ax, option_id=2)

ax.stackplot(df['Year'], *cols,
             labels=labels,
             edgecolor='black',
             linewidth=0.5
             )
plt.xlabel('Year')
plt.ylabel('Emissions (MTC)')

# draw vertical lines
trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

# ax.set_ylim([0, 70])
# ax.margins(x=0.08)
ax.set_xticks(df['Year'])


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
    ax.axvline(year, ymin=0, ymax=0.97,
               linewidth='0.5',
               ls="--",
               color='black')

    # total emission at top of vertical line
    ax.text(
        year,  # start position in year
        0.98,  # y control
        str(np.ceil(df.iloc[i][1:].sum()).astype(int)) + " MTC",
        ha="center",
        # va="top",
        transform=trans,
        fontsize=6
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
            va="top"
        )


for i, year in enumerate(df['Year']):
    interval = 10  # in years
    if i == 2 or i == 1:
        vertical_line(year, interval)
        # add_labels(year)
        # # %change
        # if i == 2:
        #     annotate_change(year, df['Year'][i - 1])
        #     pass

    if i == len(df) - 1 and year % interval != 0:
        vertical_line(year, interval)
        # annotate_change(year, year - (year % interval))

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

x, y = trans.transform([2015, 50])
boxx, boxy = ax.transAxes.inverted().transform([x, y])
# reverse the legend order and adjust position of legend
ax.legend(handles[::-1], labels[::-1],
          loc='center left',
          bbox_to_anchor=(boxx, 0.5),
          ncol=1,
          fontsize=7,
          )

plt.tight_layout()
save('emission_developing_region_trend')
plt.show()
