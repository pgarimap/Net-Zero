import os.path
from os.path import join
import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, write_csv, merge_pak2south_asia_new, DEVELOPED_REGIONS, REGIONS


def get_transport_energy_by_fuel(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/technology/transport_energy_by_fuel_n_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)

    mode_rename = {
        '2W and 3W': "2W and 3W",
        'Bus': "4W",
        'Car': "4W",
        # 'Heavy truck': "4W",
        # 'Light truck': "Light truck",
        'Mini Car': "4W"
    }
    # rename
    df['mode'] = df['mode'].replace(mode_rename.keys(), mode_rename.values())
    wheelers_df = df[df['mode'].str.contains("W")]

    # df['technology'] = df['technology'].replace(['LA-BEV'], ['BEV'])
    # aviation_df = df[df['mode'].str.contains("Aviation")]
    # tech_df = pd.pivot_table(df, index=['Year', 'region', 'technology'], values='value', aggfunc=np.sum).reset_index()
    f = pd.pivot_table(wheelers_df, index=['Year', 'region', 'mode', 'technology'], values='value', aggfunc=np.sum).reset_index()

    import matplotlib.pyplot as plt
    for tech in f['technology'].unique():
        for region in f['region'].unique():
            tech_data_23W = f[(f['technology'] == tech)& (f['region'] == region)& (f['mode'] == "2W and 3W")]
            tech_data_4W = f[(f['technology'] == tech)& (f['region'] == region)& (f['mode'] == "4W")]
            plt.plot(tech_data_23W['Year'], tech_data_23W['value'], label=f"{region}-{tech}-23W")
            plt.plot(tech_data_4W['Year'], tech_data_4W['value'], label=f"{region}-{tech}-4W")
        plt.legend()
        plt.ylabel('EJ')
        plt.show()
    return f


df_1_developing = get_transport_energy_by_fuel(SPA1, regions=REGIONS)
