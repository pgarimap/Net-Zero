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

rename = {
    'H2 retail dispensing': "H2",
    'H2 retail production': "H2",
    'H2 wholesale dispensing': "H2",
    "elect_td_trn": "Electricity",
    "refined liquids enduse": "Refined Liquids",
    "delivered gas": "Gas",
    "delivered coal": "Coal"

}

mode_rename = {
    '2W and 3W': 'road'
    , 'Bus': 'road',
    'Car': 'road', 'Domestic Aviation': "aviation", 'Domestic Ship': "shipping",
    'Freight Rail': 'rail'
    , 'Heavy truck': 'road', 'International Aviation': 'aviation', 'International Ship': 'shipping',
    'Large Car and Truck': 'road', 'Light truck': 'road', 'Medium truck': 'road',
    'Mini Car': 'road', 'Passenger Rail': 'rail', 'HSR': 'rail'
}


def get_transport_energy_by_fuel(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/transport_energy_by_fuel_n_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)

    # rename
    # df['input'] = df['input'].replace(rename.keys(), rename.values())
    df['mode'] = df['mode'].replace(mode_rename.keys(), mode_rename.values())
    df['technology'] = df['technology'].replace(['LA-BEV'], ['BEV'])

    f = pd.pivot_table(df, index=['Year', 'region', 'mode', 'technology'], values='value', aggfunc=np.sum).reset_index()
    f = f[f['technology'].isin(['Electric', 'BEV', 'FCEV'])]
    return f


df_1_developing = get_transport_energy_by_fuel(SPA1, regions=REGIONS)
df_2_developing = get_transport_energy_by_fuel(SSP2, regions=REGIONS)

df_1_developed = get_transport_energy_by_fuel(SPA1, regions=DEVELOPED_REGIONS)
df_2_developed = get_transport_energy_by_fuel(SSP2, regions=DEVELOPED_REGIONS)

write_csv(df_1_developed, 'developed_spa1_electric_transport_energy_by_fuel_n_tech', TOPICS.TECHNOLOGY)
write_csv(df_2_developed, 'developed_ssp2_electric_transport_energy_by_fuel', TOPICS.TECHNOLOGY)

write_csv(df_1_developing, 'developing_spa1_electric_transport_energy_by_fuel_n_tech', TOPICS.TECHNOLOGY)
write_csv(df_2_developing, 'developing_ssp2_electric_transport_energy_by_fuel', TOPICS.TECHNOLOGY)
