import gcamreader
import pandas as pd
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new


## get co2 emission by region for spa1 and ssp2

def get_h2_demand(ssp_scenario, agg_trans=False):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_use_by_tech.xml"
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/total_consumption_by_sector_n_fuel.xml"

    # REGIONS = ['India', 'China', 'Brazil']
    # REGIONS = ['South Asia', 'Pakistan', 'Africa_Western']

    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    df = merge_pak2south_asia_new(df)

    df = df[df['Year'].isin([2030, 2050, 2085])]

    if agg_trans:
        df.loc[df['sector'].str.startswith('trn_'), 'sector'] = 'transport'

    df_h2 = df[df['input'] == 'hydrogen']
    df_h2 = pd.pivot_table(df_h2, values='value', index=['sector'], columns=['Year'], aggfunc=np.sum)
    df_h2 = df_h2.fillna(0)
    # df_h2 = df_h2.reset_index(level=['sector'])

    df_all = pd.pivot_table(df, values='value', aggfunc=np.sum, index=['sector'], columns=['Year'])
    # take only the sectors where H2 is in demand
    df_all = df_all.loc[df_h2.index]

    demand_df = (df_h2 / df_all) * 100
    # demand_df = df_all

    demand_df.sort_values(2085, ascending=False, inplace=True)
    demand_df = demand_df.apply(lambda x: round(x, 2))
    return demand_df


def get_demand_table(ssp_scenario, input, agg_trans=False):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_use_by_tech.xml"
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/technology/total_consumption_by_sector_n_fuel.xml"

    # REGIONS = ['India', 'China', 'Brazil']
    # REGIONS = ['South Asia', 'Pakistan', 'Africa_Western']

    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    df = merge_pak2south_asia_new(df)

    if agg_trans:
        df.loc[df['sector'].str.contains('resid'), 'sector'] = 'building'
        df.loc[df['sector'].str.startswith('trn_'), 'sector'] = 'transport'
        df.loc[df['sector'].str.startswith('industrial'), 'sector'] = 'industry'
        df.loc[df['sector'].str.startswith('iron and steel'), 'sector'] = 'industry'
        df.loc[df['sector'].str.startswith('municipal'), 'sector'] = 'municipal'
        df.loc[df['sector'].str.contains('comm'), 'sector'] = 'building'

    df_input = df[df['input'] == input]
    df_input = pd.pivot_table(df_input, values='value', index=['region', 'sector', 'Year'], aggfunc=np.sum)
    df_input = df_input.fillna(0)
    df_input.reset_index(inplace=True)
    return df_input

# df_sub = get_h2_demand(SPA1)
# df_aggregated_trans = get_h2_demand(SPA1, True)
# write_csv(df_sub, 'h2_demand_by_sector', TOPICS.TECHNOLOGY)
# write_csv(df_aggregated_trans, 'h2_demand_by_agg_trans_sector', TOPICS.TECHNOLOGY)
# write_csv(df_aggregated_trans, 'electricity_relative_demand_by_agg_trans_sector', TOPICS.TECHNOLOGY)

# df_elec = get_demand_table(SPA1, 'electricity', False)

df_h2 = get_demand_table(SPA1, 'hydrogen', True)
df_h2_ssp2 = get_demand_table(SSP2, 'hydrogen', True)

write_csv(df_h2, 'h2_demand_by_sector_5_regions_spa1', TOPICS.TECHNOLOGY)
write_csv(df_h2_ssp2, 'h2_demand_by_sector_5_regions_ssp2', TOPICS.TECHNOLOGY)
# write_csv(df_h2, 'h2_demand_by_sector_ssp1_non_agg', TOPICS.TECHNOLOGY)