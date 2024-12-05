"""
To show present state of energy source and what's required.
Show energy sources in year 2050 in SPA1 and year 2023 SSP 2

"""
import os.path
from os.path import join
import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new, rename_column

rename = {
    'H2 central production': "Hydrogen",
    'H2 wholesale dispensing': "Hydrogen",
    'backup_electricity': "electricity",
    'delivered gas': "gas",
    'gas processing': "gas",
    'gas pipeline': "gas",
    'refined liquids enduse': "refined liquids",
    'refined liquids industrial': "refined liquids",
}

# ['H2 central production', 'H2 wholesale dispensing', 'agriculture',
#        'industry', 'backup_electricity', 'building', 'delivered biomass',
#        'delivered gas', 'electricity', 'gas pipeline', 'gas processing',
#        'refined liquids enduse', 'refined liquids industrial', 'refining',
#        'transportation', '', 'csp_backup', 'district heat']

# get SPA 1 energy sources
def get_co2_by_sector(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/co2_by_sector.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    # columns : 'Units', 'scenario', 'region', 'fuel', 'Year', 'value'
    # merge pakistan into south asia

    cat_col = 'sector'
    on = ['Year', 'sector', 'scenario', 'Units']
    df = df[df['Year'] >= 2000]
    # merge pakistan into south asia
    df = rename_column(df, 'sector')
    df['sector'] = df['sector'].replace(rename.keys(), rename.values())
    df = merge_pak2south_asia_new(df)
    # df = merge_pak2south_asia(df, cat_col, on)
    # TODO: verify what is happening with merge_pak2south_asia and new
    # rename sectors
    if '' in df.columns:
        df.drop(columns=[''], inplace=True)
    df = pd.pivot_table(df, values='value', index=['sector', 'region', 'scenario', 'Year'], aggfunc=np.sum)
    df = df.reset_index(level=['region', 'scenario', 'Year', 'sector'])
    return df


df_1 = get_co2_by_sector(SPA1)
df_2 = get_co2_by_sector(SSP2)

write_csv(df_1, 'spa1_co2_by_sector', TOPICS.ENERGY_AND_EMISSION)
write_csv(df_2, 'spa2_co2_by_sector', TOPICS.ENERGY_AND_EMISSION)
