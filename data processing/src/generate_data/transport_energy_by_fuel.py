"""
To show present state of energy source and what's required.
Show energy sources in year 2050 in SPA1 and year 2023 SSP 2

"""
import os.path
from os.path import join
import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new

rename = {
    'H2 retail dispensing': "H2",
    'H2 retail production': "H2",
    'H2 wholesale dispensing': "H2",
    "elect_td_trn": "Electricity",
    "refined liquids enduse": "Refined Liquids",
    "delivered gas":  "Gas",
    "delivered coal": "Coal"

}

def get_transport_energy_by_fuel(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/transport_energy_by_fuel.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    # columns : 'Units', 'scenario', 'region', 'fuel', 'Year', 'value'
    # merge pakistan into south asia

    cat_col = 'input'
    on = ['Year', 'input', 'scenario', 'Units']
    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)

    # rename
    df['input'] = df['input'].replace(rename.keys(), rename.values())
    return df


df_1 = get_transport_energy_by_fuel(SPA1)
df_2 = get_transport_energy_by_fuel(SSP2)

write_csv(df_1, 'spa1_transport_energy_by_fuel', TOPICS.TECHNOLOGY)
write_csv(df_2, 'ssp2_transport_energy_by_fuel', TOPICS.TECHNOLOGY)
