import gcamreader
import pandas as pd
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new


## get co2 emission by region for spa1 and ssp2

def get_elec_demand_in_transport(ssp_scenario, agg_trans=False):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_use_by_tech.xml"
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/total_consumption_by_sector_n_fuel.xml"

    # REGIONS = ['India', 'China', 'Brazil']
    # REGIONS = ['South Asia', 'Pakistan', 'Africa_Western']

    df_ = get_data(ssp_name=ssp_scenario, query_path=query_file)
    df_ = merge_pak2south_asia_new(df_)

    df_ = df_[df_['Year'].isin([2030, 2050, 2085])]

    if agg_trans:
        df_.loc[df_['sector'].str.startswith('trn_'), 'sector'] = 'transport'

    df = df_[df_['input'] == 'electricity']
    df = df[df['sector'] == 'transport']
    df = pd.pivot_table(df, values='value', index=['sector', 'region'], columns=['Year'], aggfunc=np.sum)
    df = df.fillna(0)
    # df = df.reset_index(level=['sector'])

    df_all = pd.pivot_table(df_, values='value', aggfunc=np.sum, index=['sector', 'region'], columns=['Year'])
    # take only the sectors where sector is transport and input is electricity
    df_all = df_all.loc[df.index]

    # demand_df = (df / df_all) * 100
    demand_df = df

    demand_df.sort_values(2085, ascending=False, inplace=True)
    demand_df = demand_df.apply(lambda x: round(x, 2))
    return demand_df


df_aggregated_trans = get_elec_demand_in_transport(SPA1, True)
# write_csv(df_aggregated_trans, 'region_wise_relative_elec_demand_in_trans_2030_2050_2085', TOPICS.TECHNOLOGY)
write_csv(df_aggregated_trans, 'region_wise_absolute_elec_demand_in_trans_2030_2050_2085', TOPICS.TECHNOLOGY)
# write_csv(df_aggregated_trans, 'energy_demand_by_sector_agg_trans_sector', TOPICS.TECHNOLOGY)
