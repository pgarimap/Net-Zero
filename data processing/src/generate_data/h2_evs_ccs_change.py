import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS
from src.utils import get_data, REGIONS, DEVELOPED_REGIONS, write_csv, merge_pak2south_asia_new


def get_ccs(ssp_scenario, regions=None, return_raw=False):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/sequestration.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    if return_raw:
        return df
    df = df[df['Year'].isin([2020, 2030, 2050, 2085])]
    f = pd.pivot_table(df, index=['Year'], values='value', aggfunc='sum').reset_index()
    f['change (times of 2020)'] = f['value'] / f[f['Year'] == 2020].value[0]
    return f


def get_hydrogen(ssp, regions=None, return_raw=False):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_use_by_tech.xml"
    df = get_data(ssp_name=ssp, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    if return_raw:
        return df
    df = df[df['Year'].isin([2020, 2025, 2030, 2050, 2085])]
    f = pd.pivot_table(df, index=['Year'], values='value', aggfunc='sum').reset_index()
    # f['change (times of 2025)'] = f['value']/f[f['Year'] == 2025].value[0]
    return f


def get_evs(ssp, regions=None, return_raw=False):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/transport_energy_by_fuel.xml"
    df = get_data(ssp_name=ssp, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    df = df[df['input'] == 'elect_td_trn']
    if return_raw:
        return df
    df = df[df['Year'].isin([2020, 2030, 2050, 2085])]
    f = pd.pivot_table(df, index=['Year'], values='value', aggfunc='sum').reset_index()
    f['change (times if 2020)'] = f['value'] / f[f['Year'] == 2020].value[0]
    return f


def get_major_minor_change(spa1, ssp2, base_year=2020, target_year=2085):
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

    p1 = pd.pivot_table(df1, index=['Year', 'region'], values='value', aggfunc=np.sum).reset_index()
    p2 = pd.pivot_table(df2, index=['Year', 'region'], values='value', aggfunc=np.sum).reset_index()

    def get_change(base, target, region):
        base_val = base[(base['Year'] == base_year) &
                        (base['region'] == region)]['value'].values[0]
        target_val = target[(target['Year'] == target_year) &
                            (target['region'] == region)]['value'].values[0]
        return target_val / base_val

    major_increase = get_change(p2, p1, 'major')

    minor_increase = get_change(p2, p1, 'minor')

    return major_increase, minor_increase


def get_change_main():
    # evs
    spa1_evs = get_evs(SPA1, regions=REGIONS, return_raw=True)
    ssp2_evs = get_evs(SSP2, regions=REGIONS, return_raw=True)
    evs_change_major, evs_change_minor = get_major_minor_change(ssp2_evs, spa1_evs)

    # ccs
    spa1_ccs = get_ccs(SPA1, regions=REGIONS, return_raw=True)
    ssp2_ccs = get_ccs(SSP2, regions=REGIONS, return_raw=True)
    ccs_change_major, ccs_change_minor = get_major_minor_change(ssp2_ccs, spa1_ccs)

    # h2
    spa1_h2 = get_hydrogen(SPA1, regions=REGIONS, return_raw=True)
    # ssp2_h2 = get_hydrogen(SSP2, regions=REGIONS, return_raw=True)
    # h2 calculated from 2025 OS
    h2_change_major, h2_change_minor = get_major_minor_change(spa1_h2, spa1_h2, base_year=2025)

    print()


# get_change_main()

ccs_sap1_developing = get_ccs(SPA1, regions=REGIONS)
ccs_ssp2_developing = get_ccs(SSP2, regions=REGIONS)

ccs_sap1_developed = get_ccs(SPA1, regions=DEVELOPED_REGIONS)
ccs_ssp2_developed = get_ccs(SSP2, regions=DEVELOPED_REGIONS)

h2_sap1_developing = get_hydrogen(SPA1, regions=REGIONS)
h2_ssp2_developing = get_hydrogen(SSP2, regions=REGIONS)

h2_sap1_developed = get_hydrogen(SPA1, regions=DEVELOPED_REGIONS)
h2_ssp2_developed = get_hydrogen(SSP2, regions=DEVELOPED_REGIONS)

evs_sap1_developing = get_evs(SPA1, regions=REGIONS)
evs_ssp2_developing = get_evs(SSP2, regions=REGIONS)

evs_sap1_developed = get_evs(SPA1, regions=DEVELOPED_REGIONS)
evs_ssp2_developed = get_evs(SSP2, regions=DEVELOPED_REGIONS)

# call write_csv func with appropriate params for all above dataframes
write_csv(ccs_sap1_developing, 'developing_spa1_ccs', TOPICS.TECHNOLOGY)
write_csv(ccs_ssp2_developing, 'developing_ssp2_ccs', TOPICS.TECHNOLOGY)
write_csv(ccs_sap1_developed, 'developed_spa1_ccs', TOPICS.TECHNOLOGY)
write_csv(ccs_ssp2_developed, 'developed_ssp2_ccs', TOPICS.TECHNOLOGY)

write_csv(h2_sap1_developing, 'developing_spa1_h2', TOPICS.TECHNOLOGY)
write_csv(h2_ssp2_developing, 'developing_ssp2_h2', TOPICS.TECHNOLOGY)
write_csv(h2_sap1_developed, 'developed_spa1_h2', TOPICS.TECHNOLOGY)
write_csv(h2_ssp2_developed, 'developed_ssp2_h2', TOPICS.TECHNOLOGY)

write_csv(evs_sap1_developing, 'developing_spa1_evs', TOPICS.TECHNOLOGY)
write_csv(evs_ssp2_developing, 'developing_ssp2_evs', TOPICS.TECHNOLOGY)
write_csv(evs_sap1_developed, 'developed_spa1_evs', TOPICS.TECHNOLOGY)
write_csv(evs_ssp2_developed, 'developed_ssp2_evs', TOPICS.TECHNOLOGY)
