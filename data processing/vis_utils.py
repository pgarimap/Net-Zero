import pandas as pd

import matplotlib.pyplot as plt


def plot_region(df, scenario, region, category_col, ax, x_col='Year', y_col='value', save_title=None, fig=None, ylabel=''):
    # get data for only that region
    if region is not None:
        df = df[df['region'] == region]
    df = df[df['scenario'] == scenario]

    # give subplot a title
    title_text = "" if not region else region + f" {scenario[5:9]}"
    ax.title.set_text(title_text)
    ax.grid('on')

    # for each category draw a line chart of different color
    with plt.style.context('Solarize_Light2'):
        if category_col is not None:
            categories = pd.unique(df[category_col])
            for cat in categories:
                sub_df = df[df[category_col] == cat]
                # plot data
                ax.plot(sub_df[x_col], sub_df[y_col], label=cat)
        else:
            ax.plot(df[x_col], df[y_col], label='')
        ax.set_xlabel('Year')
        ax.set_ylabel(ylabel)
    ax.legend(loc='upper right', bbox_to_anchor=(1.5, 1))
    if save_title:
        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1))
        fig.savefig(f'./out/{save_title}-{region}-{scenario[5:9]}.png',
                    # bbox_extra_artists=(lgd, text),
                    bbox_inches='tight')


def plot_query(df, scenario, category_col, x_col="Year", y_col="value", rows=5, cols=1, region_idx=None,
               save_title=None, ylabel=''):

    regions = pd.unique(df['region'])
    if region_idx is None and len(regions) > 1:
        # subplots for each region
        fig, subplots = plt.subplots(rows, cols, figsize=(1 * 10, 6 * 10))
        for i in range(rows):
            for j in range(cols):
                if cols != 1:
                    subplot = subplots[i][j]
                else:
                    subplot = subplots[i]

                region_idx = i * cols + j
                region = regions[region_idx]
                plot_region(df, scenario, region, category_col, subplot, save_title=save_title, fig=fig)
    else:
        fig = plt.figure(figsize=(10, 10))
        ax = plt.subplot(111)
        # plot for single region
        if region_idx is not None:
            region = regions[region_idx]
        else:
            region = None

        plot_region(df, scenario, region, category_col, ax, save_title=save_title, fig=fig, ylabel=ylabel)

    # adjust margins
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

    plt.show()
