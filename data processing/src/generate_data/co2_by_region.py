import pandas as pd
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new


## get co2 emission by region for spa1 and ssp2
def get_co2_by_region(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/intro/co2_by_region.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=None)

    cat_col = 'region'
    on = ['Year', 'region', 'scenario', 'Units']
    # df = df[df['Year'] >= 2000]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)
    # rename sectors
    if '' in df.columns:
        df.drop(columns=[''], inplace=True)
    df = pd.pivot_table(df, values='value', index=['region', 'scenario', 'Year'], aggfunc=np.sum)
    df = df.reset_index(level=['region', 'scenario', 'Year'])

    return df


REGIONS = ['India', 'South Asia', 'China', 'Pakistan', 'Brazil', 'Africa_Western']

df_ssp1 = get_co2_by_region(SPA1)
## filter ssp1 to remove REGIONS
df_ssp1_filtered = df_ssp1[~df_ssp1['region'].isin(REGIONS)]

df_ssp2 = get_co2_by_region(SSP2)
## filter ssp2 to select REGIONS
df_ssp2_filtered = df_ssp2[df_ssp2['region'].isin(REGIONS)]

# spa1 for other regions, ssp2 for developing regions
no_part_developing = pd.concat([df_ssp2_filtered, df_ssp1_filtered])
take_part_developing = df_ssp1

write_csv(no_part_developing, 'emission_by_region_no_part_dev', TOPICS.INTRO)
write_csv(take_part_developing, 'emission_by_region_part_dev', TOPICS.INTRO)
