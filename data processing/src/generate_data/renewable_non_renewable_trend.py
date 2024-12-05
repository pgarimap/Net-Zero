"""
To show present state of energy source and what's required.
Show trend of renewable and non-renewables
"""

from os.path import join
import pandas as pd
import numpy as np

# get SPA 1 energy sources
from src.consts import SPA1, SSP2
from src.utils import get_data, merge_pak2south_asia_new

fuel2category = {
    'a oil': 'non-renewable',
    'b natural gas': 'non-renewable',
    'c coal': 'non-renewable',
    'd biomass': 'renewable',
    'e nuclear': 'renewable',
    'f hydro': 'renewable',
    'g wind': 'renewable',
    'h solar': 'renewable',
    'i geothermal': 'renewable',
    'j traditional biomass': 'renewable'
}


def get_energy_consumption(ssp_scenario, return_raw=False):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/energy_and_emission/primary energy consumption by region.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    df = merge_pak2south_asia_new(df)
    df['fuel'] = df['fuel'].replace(fuel2category.keys(), fuel2category.values())

    if return_raw:
        return df

    df.drop(columns=['Units', 'region'], inplace=True)

    return pd.pivot_table(df, index=['Year', 'fuel'], values='value', aggfunc=np.sum).reset_index()


def get_spa1_energy_consumption():
    spa1_df = get_energy_consumption(SPA1)

    return spa1_df


def get_ssp2_energy_consumption():
    df = get_energy_consumption(SSP2)
    return df


def get_major_minor_change():
    spa1 = get_energy_consumption(SPA1, return_raw=True)
    ssp2 = get_energy_consumption(SSP2, return_raw=True)
    df1 = spa1.copy()
    df2 = ssp2.copy()

    def categorize_region(df):
        df.loc[df['region'] == 'South Asia', 'region'] = 'minor'
        df.loc[df['region'] == 'Africa_Western', 'region'] = 'minor'
        df.loc[df['region'] == 'Brazil', 'region'] = 'major'
        df.loc[df['region'] == 'China', 'region'] = 'major'
        df.loc[df['region'] == 'India', 'region'] = 'major'
        return df

    df1 = categorize_region(df1)
    df2 = categorize_region(df2)

    p1 = pd.pivot_table(df1, index=['Year', 'fuel', 'region'], values='value', aggfunc=np.sum).reset_index()
    p2 = pd.pivot_table(df2, index=['Year', 'fuel', 'region'], values='value', aggfunc=np.sum).reset_index()

    def get_change(base, target, fuel, region):
        base_val = base[(base['Year'] == 2020) &
                        (base['region'] == region) &
                        (base['fuel'] == fuel)]['value'].values[0]
        target_val = target[(target['Year'] == 2085) &
                            (target['region'] == region) &
                            (target['fuel'] == fuel)]['value'].values[0]
        return target_val / base_val

    major_increase_ren = get_change(p2, p1, 'renewable', 'major')

    major_increase_non_ren = get_change(p2, p1, 'non-renewable', 'major')

    minor_increase_ren = get_change(p2, p1, 'renewable', 'minor')
    minor_increase_non_ren = get_change(p2, p1, 'non-renewable', 'minor')

    return None


get_major_minor_change()
spa1 = get_spa1_energy_consumption()
ssp2 = get_ssp2_energy_consumption()

outpath = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out"
spa1.to_csv(join(outpath, 'spa1_renewable_non_renewable_trend.csv'))
ssp2.to_csv(join(outpath, 'ssp2_renewable_non_renewable_trend.csv'))
