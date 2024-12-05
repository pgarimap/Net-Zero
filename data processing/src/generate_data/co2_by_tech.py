import pandas as pd
import numpy as np
import json

from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv, rename_column

with open('/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology2input.json', 'r') as f:
    tech2input = json.load(f)


def get_co2_by_region(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/co2_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    cat_col = 'technology'
    on = ['Year', 'region', cat_col, 'scenario', 'Units']
    df = df[df['Year'] >= 2000]
    # merge pakistan into south asia
    df = merge_pak2south_asia(df, cat_col, on)
    # rename sectors
    if '' in df.columns:
        df.drop(columns=[''], inplace=True)

    # rename_column()
    keys = tech2input.keys()
    vals = tech2input.values()
    df[cat_col] = df[cat_col].replace(keys, vals)

    df = pd.pivot_table(df, values='value', index=['region', 'scenario', cat_col, 'Year'], aggfunc=np.sum)
    df = df.reset_index(level=['region', 'scenario', cat_col, 'Year'])

    return df


df_ssp1 = get_co2_by_region(SPA1)

df_ssp2 = get_co2_by_region(SSP2)


write_csv(df_ssp1, 'ssp1_co2_by_input', TOPICS.TECHNOLOGY)
write_csv(df_ssp2, 'ssp2_co2_by_input', TOPICS.TECHNOLOGY)
