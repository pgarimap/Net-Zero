import pandas as pd
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv


def energy_by_fuel(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/energy_by_fuel.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    cat_col = 'input'
    on = ['Year', 'region', 'scenario', 'input', 'Units']
    df = df[df['Year'] >= 2000]
    # merge pakistan into south asia
    df = merge_pak2south_asia(df, cat_col, on)
    # rename sectors
    if '' in df.columns:
        df.drop(columns=[''], inplace=True)
    df = pd.pivot_table(df, values='value', index=['region', 'scenario', cat_col, 'Year'], aggfunc=np.sum)
    df = df.reset_index(level=['region', 'scenario', cat_col, 'Year'])

    return df


df_ssp1 = energy_by_fuel(SPA1)

df_ssp2 = energy_by_fuel(SSP2)

write_csv(df_ssp2, 'energy_by_fuel_ssp2', TOPICS.TECHNOLOGY)
write_csv(df_ssp1, 'energy_by_fuel_ssp1', TOPICS.TECHNOLOGY)
