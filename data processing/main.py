import gcamreader
import os.path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.utils import parse_rewrite
from vis_utils import plot_query

regions = ['India', 'South Asia', 'China', 'Pakistan', 'Brazil', 'Africa_Western']
scenarios = ['GCAM_SSP4', 'GCAM_SSP5', 'GCAM_SSP1', 'GCAM_SSP2', 'GCAM_SSP3']

dbpath = "/Users/pramish/Desktop/Codes/netzero/gcam-v6.0/output"
dbpath2 = "/Users/pramish/Desktop/Codes/netzero/gcam-v6.0/output/spa1/"
dbfile = "database_basexdb"
# dbfile2 = "database_basexdb2"
dbfile3 = "database_basexdb2"
conn = gcamreader.LocalDBConn(dbpath2, dbfile3)

queries = gcamreader.parse_batch_query(os.path.join('data', 'sample-queries.xml'))


def merge_pak2south_asia(res, category_column=None, on=None):
    ## merge pakistan value into south asia

    result = res.copy()

    sa = result[result['region'] == 'South Asia']
    pak = result[result['region'] == 'Pakistan']
    if on is not None:
        sa_pak = pd.merge(sa, pak, on=on, how='left')
    else:
        sa_pak = pd.merge(sa, pak, on=['Year', category_column, 'scenario', 'Units'], how='left')
    sa_pak['value'] = sa_pak['value_x'] + sa_pak['value_y']
    sa_pak.rename(columns={'region_x': 'region'}, inplace=True)
    sa_pak.drop(columns=['value_x', 'value_y'], inplace=True)

    # Pakistan from result
    # result = result[result['region'] != 'South Asia']
    result = result[result['region'] != 'Pakistan']

    # merge with original result
    if on is not None:
        result = pd.merge(result, sa_pak, on=on, how='left')
    else:
        result = pd.merge(result, sa_pak, on=['Year', category_column, 'scenario', 'Units', 'region'], how='left')

    result.rename(columns={'value_x': 'value'}, inplace=True)
    if 'region_y' in result.columns:
        result.drop(columns=['region_y', 'value_y'], inplace=True)

    return result


def rename_column(result, col_name):
    name_mapper = parse_rewrite('./data/rewrite.xml')
    keys = [key[0] for key in name_mapper]
    vals = [key[1] for key in name_mapper]
    result[col_name] = result[col_name].replace(keys, vals)

    return result


# total final energy by sector
def energy_sector_wise(result):
    category_col = 'sector'
    units = result.iloc[0]['Units']

    result = merge_pak2south_asia(result, category_col)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'sector'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'sector'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title='sector_wise', ylabel=units)


# CO2 emissions by sector
def co2_by_sector(result):
    category_col = 'sector'
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, category_col)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'sector'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'sector'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title='co2_by_sector', ylabel=units)


# building final energy by fuel
def energy_by_fuel(result):
    category_col = 'input'
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, category_col)
    # result = rename_sectors(result, category_col)

    # result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'sector'], aggfunc=np.sum)
    # result = result.reset_index(level=['region', 'scenario', 'Year', 'sector'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx,
                       save_title='building_by_fuel', ylabel=units)


def general(result, cat, title=None):
    units = result.iloc[0]['Units']
    category_col = cat
    result = merge_pak2south_asia(result, category_col)
    # result = rename_sectors(result, category_col)

    # result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'sector'], aggfunc=np.sum)
    # result = result.reset_index(level=['region', 'scenario', 'Year', 'sector'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col, region_idx=region_idx,
                       save_title=title, ylabel=units)


def co2_emission_by_tech(result):
    category_col = 'technology'
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', category_col, 'scenario', 'region', 'sector', 'Units'])
    result.rename(columns={'sector_x': 'sector'}, inplace=True)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'technology'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'technology'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title='co2_by_tech', ylabel=units)


def co2_emission_by_region(result):
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', 'scenario', 'region', 'Units'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=None,
                       region_idx=region_idx, save_title='co2_by_region', ylabel=units)


def hydrogen_production_by_tech(result):
    category_col = 'technology'
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', category_col, 'scenario', 'region', 'sector', 'Units'])
    result.rename(columns={'sector_x': 'sector'}, inplace=True)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'technology'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'technology'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title='hydrogen_production_by_tech', ylabel=units)


def hydrogen_cost_by_tech(result):
    category_col = 'technology'
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', category_col, 'scenario', 'region', 'sector', 'Units'])
    result.rename(columns={'sector_x': 'sector'}, inplace=True)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'technology'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'technology'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title='hydrogen_cost_by_tech', ylabel=units)


def general_by_tech(result, category_col='technology', title=None):
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', category_col, 'scenario', 'region', 'sector', 'Units'])
    result.rename(columns={'sector_x': 'sector'}, inplace=True)
    result = rename_column(result, category_col)

    result = pd.pivot_table(result, values='value', index=['region', 'scenario', 'Year', 'technology'], aggfunc=np.sum)
    result = result.reset_index(level=['region', 'scenario', 'Year', 'technology'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=category_col,
                       region_idx=region_idx, save_title=title, ylabel=units)


def gdp_by_region(result):
    units = result.iloc[0]['Units']
    result = merge_pak2south_asia(result, on=['Year', 'scenario', 'region', 'Units'])
    for region_idx in range(len(pd.unique(result['region']))):
        for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=None,
                       region_idx=region_idx, save_title='GDP', ylabel=units)


def global_mean_temp(result, title):
    units = result.iloc[0]['Units']
    result['region'] = None
    # result = merge_pak2south_asia(result, on=['Year', 'scenario', 'Units'])
    for scenario in pd.unique(result['scenario']):
            plot_query(result, scenario, category_col=None,
                       region_idx=None, save_title=title, ylabel=units)


if __name__ == "__main__":
    query_func_idx = {
        3: energy_sector_wise,
        2: co2_by_sector,
        4: energy_by_fuel,  # building final energy by fuel
        5: co2_emission_by_tech,
        6: co2_emission_by_region,

    }
    idx = -1
    res = conn.runQuery(queries[idx], scenarios=scenarios, regions=regions)
    # energy_sector_wise(res)
    # co2_by_sector(res)
    # energy_by_fuel(res)
    # co2_emission_by_tech(res)

    # 9 primary energy consumption by region with CCS
    # co2_emission_by_region(res)

    # 7
    # general(res, 'fuel', 'regional primary energy prices')

    # 8
    # general(res, 'fuel', 'final energy prices')

    # 9
    # general(res, 'fuel', 'primary energy consumption with CCS by region (direct equivalent)')

    # 10
    # hydrogen_production_by_tech(res)

    # 11
    # hydrogen_cost_by_tech(res)

    # 12
    # general(res, 'input', 'transport final energy by fuel')

    # 13
    # general_by_tech(res, title='transport service output by tech')

    # 14
    # general(res, 'sector', title='CO2 sequestration by sector')

    # 15
    # general_by_tech(res, title='CO2 sequestration by tech')

    # 16 elec gen by subsector
    # general(res, cat='subsector', title='ele gen')

    # 17 elec gen costs by subsector
    # general(res, cat='subsector', title='elec gen costs by subsector')

    # 18
    # gdp_by_region(res)

    # 19 total climate forcing

    # 20 global temperature
    global_mean_temp(res, 'global mean temperature')
    print()
