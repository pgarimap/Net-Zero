"""
To show present state of energy source and what's required.
Show energy sources in year 2050 in SPA1 and year 2023 SSP 2

"""
import os.path
from os.path import join
import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, write_csv, merge_pak2south_asia_new, DEVELOPED_REGIONS, REGIONS


def get_transport_energy_by_fuel(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/technology/total_consumption_by_sector_n_fuel.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)

    # h2_df = df[df['technology'] == 'Hydrogen']
    # h2_df = df[df['mode'] == 'Car']
    df_h2_trans = df[(df['input'] == 'hydrogen') & (df['sector'].str.contains('trn_'))]
    p_h2_trn = pd.pivot_table(df_h2_trans, index=['Year', 'region'], values='value', aggfunc=np.sum).reset_index()
    df_trn = df[df['sector'].str.contains('trn_')]
    p_trn = pd.pivot_table(df_trn, index=['Year', 'region'], values='value', aggfunc=np.sum).reset_index()

    # get percentage of h2 in transport
    # select year, region as index from p_h2_trn and add a new column in p_h2_trn that shows percentage of h2 in transport

    p_h2_trn = p_h2_trn.set_index(['Year', 'region'])
    p_trn = p_trn.set_index(['Year', 'region'])
    p_h2_trn['h2_trn %'] = (p_h2_trn['value'] / p_trn['value']) * 100
    return p_h2_trn, p_trn


df_1_developing = get_transport_energy_by_fuel(SPA1, regions=REGIONS)
df_2_developing = get_transport_energy_by_fuel(SSP2, regions=REGIONS)

# write_csv(df_1_developing, 'developing_spa1_electric_transport_energy_by_fuel_n_tech', TOPICS.TECHNOLOGY)
# write_csv(df_2_developing, 'developing_ssp2_electric_transport_energy_by_fuel', TOPICS.TECHNOLOGY)
