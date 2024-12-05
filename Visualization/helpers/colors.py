import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import seaborn as sns
import palettable

import numpy as np


def set_colors(colors, ax=None):
    if ax is None:
        mpl.rcParams['axes.prop_cycle'] = cycler('color', colors)
    else:
        ax.set_prop_cycle('color', colors)


def set_stacked_area_colors(ax: plt.axes, option_id=0):
    option1 = palettable.scientific.diverging.Berlin_10.mpl_colors
    option2 = sns.color_palette("cubehelix")
    option3 = sns.color_palette("Set2")
    option4 = sns.cubehelix_palette(start=.5, rot=-.5)
    option5 = palettable.colorbrewer.qualitative.Dark2_7.mpl_colors

    # final choice
    options = [
        option1, option2, option3, option4, option5
    ]
    assert option_id < len(options)
    option = options[option_id]
    set_colors(option, ax=ax)
