
import os.path
from os.path import join
import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, write_csv, merge_pak2south_asia_new, DEVELOPED_REGIONS, REGIONS

def get_aviation_energy_by_fuel(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/src/generate_data/transport/queries/mode_price.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)

    # rename

    # df['technology'] = df['technology'].replace(['LA-BEV'], ['BEV'])
    aviation_df = df[df['mode'].str.contains("Domestic Aviation")]
    tech_df = pd.pivot_table(aviation_df, index=['Year', 'region', 'technology'], values='value', aggfunc=np.sum).reset_index()
    f = pd.pivot_table(aviation_df, index=['Year', 'region', 'mode', 'technology'], values='value', aggfunc=np.sum).reset_index()

    return f


df_ssp1 = get_aviation_energy_by_fuel(SSP2, regions=REGIONS)
