import numpy as np

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import palettable
from matplotlib.colors import ListedColormap

from constants import *
from helpers.io import save

plt.style.use('./styles/choropleth.mplstyle')


def read_data():
    df = pd.read_csv('data/emission_by_countries.csv')
    # add columns
    df['value1'] = df['value']
    df['value2'] = df['value']
    select_first = lambda x: x.iloc[0]

    def agg(min, max):
        def decade_agg(series):
            sub_df = df.loc[series.index]
            return sub_df[np.logical_and(sub_df['year'] > min, sub_df['year'] <= max)]['value'].mean()

        return decade_agg

    df_pivot = pd.pivot_table(df, index=['ISO'], values=['country', 'value1', 'value2', ],
                              aggfunc={'value1': agg(1999, 2009), 'value2': agg(2009, 2019), 'country': select_first})
    # df_pivot['value'] = df_pivot['value2'] - df_pivot['value1']
    df_pivot['value'] = df_pivot['value2']
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.set_index('iso_a3', inplace=True)
    world = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")]

    world = world.to_crs("EPSG:3857")  # world.to_crs(epsg=3395) would also work
    cross = world.join(df_pivot)
    cross = cross[pd.notna(cross['value'])]
    return cross


cross = read_data()

# plot
fig = plt.figure(figsize=FIG_SIZE_SINGLE, dpi=DISPLAY_DIP)
ax = plt.subplot(111)
ax.margins(0.1)
ax.set_ylim([-10073679.877525851 * 1.5, 21032155.87444515])
# box = ax.get_position()
# ax.set_position([box.x0, box.y0,
#                  box.width, box.height + 0.2])
# legend
from mpl_toolkits.axes_grid1 import make_axes_locatable

# fix size for vertical right legend
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.1)

# custom colors
cmap = ListedColormap(palettable.cmocean.sequential.Amp_12.mpl_colors)  # Deep_5, Dense_5, Amp_5
from mapclassify import NaturalBreaks

labels = NaturalBreaks(cross['value'], k=6)
labels = labels.get_legend_classes(fmt="{:.0f} Gt Co2")
cross.plot(column='value', ax=ax,
           legend=True,
           cmap=cmap,
           # cax=cax,
           scheme="natural_breaks",
           classification_kwds={'k': 6},
           legend_kwds={
               'loc': 'lower center',
               'bbox_to_anchor': (0.5, 0.0),
               'ncol': 2,
               'labels': labels

           },
           # missing_kwds={
           #     "color": "lightgrey",
           #     "edgecolor": "red",
           #     "hatch": "///",
           #     "label": "Missing values",
           # },
           )

# add legend
handles, labels = ax.get_legend_handles_labels()

# # reverse the legend order and adjust position of legend
# ax.legend(prop={'size': 12},
#           bbox_to_anchor=(1.0, 0.5),
#           )
# ax.legend(bbox_to_anchor=(1.0, .5), prop={'size': 12})
ax.set(title='2009 To 2019 Total Co2 Contribution By Countries')
save('choropleth total co2 by countries')
plt.show()
