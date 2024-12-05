import pandas as pd

from src.consts import SPA1, SSP2, TOPICS
from src.utils import get_data, REGIONS, DEVELOPED_REGIONS, write_csv, merge_pak2south_asia_new

nameMapper_ccs = {
    'H2 central production': 'industry',
    'N fertilizer': 'industry',
    'alumina': 'industry', 'cement': 'industry',
    'chemical energy use': 'industry', 'chemical feedstocks': 'industry',
    'construction feedstocks': 'industry',
    'elec_biomass (IGCC CCS)': 'biomass',
    'elec_biomass (conv CCS)': 'biomass',
    'elec_coal (IGCC CCS)': 'fossil fuel',
    'elec_coal (conv pul CCS)': 'fossil fuel',
    'elec_gas (CC CCS)': 'fossil fuel',
    'elec_refined liquids (CC CCS)': 'refined liquid',
    'iron and steel': 'industry',
    'other industrial feedstocks': 'industry',
    'refining': 'industry'
}

# transport evs, h2, ccs

def get_capital_h2(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/cost/capital_investment_demand_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    df = df[df['Year'].isin([2020, 2030, 2050, 2085])]

    df = df[df['technology'].str.contains('H2')| df['technology'].str.contains('hydrogen') | (df['sector'].str.contains('H2'))]

    f = pd.pivot_table(df, index=['Year', 'region'], values='value', aggfunc='sum').reset_index()
    # f['change (times of 2015)'] = f['value']/f[f['Year'] == 2015].value[0]
    return f

def get_capital_ccs(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/cost/capital_investment_demand_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    df = df[df['Year'].isin([2020, 2030, 2050, 2085])]

    # df.loc[df['sector'].str.contains('CCS'), 'sector'] = 'CCS'
    # df.loc[df['technology'].str.contains('CCS'), 'technology'] = 'CCS'

    df = df[df['technology'].str.contains('CCS') | (df['sector'].str.contains('CCS'))]

    f = pd.pivot_table(df, index=['Year', 'region'], values='value', aggfunc='sum').reset_index()
    # f['change (times of 2015)'] = f['value']/f[f['Year'] == 2015].value[0]
    return f

def get_evs_investment(ssp_scenario, regions=None):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/cost/capital_investment_demand_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)
    df = merge_pak2south_asia_new(df)
    # df = df[df['Year'].isin([2020, 2030, 2050, 2085])]

    df = df.loc[df['sector'].str.contains('trn')]

    df = df[df['technology'].isin(['BEV', 'FCEV', 'Electric'])]

    f = pd.pivot_table(df, index=['region', 'Year', 'technology'], values='value', aggfunc='sum')
    # f['change (times of 2015)'] = f['value']/f[f['Year'] == 2015].value[0]
    return f

df1_h2 = get_capital_h2(SPA1, regions=REGIONS)
df2_h2 = get_capital_h2(SSP2, regions=REGIONS)

df1_ccs = get_capital_ccs(SPA1, regions=REGIONS)
df2_ccs = get_capital_ccs(SSP2, regions=REGIONS)

df1_evs = get_evs_investment(SPA1, regions=REGIONS)
df2_evs = get_evs_investment(SSP2, regions=REGIONS)

write_csv(df1_h2, 'ssp1_developing_capital_investment_h2', TOPICS.COST)
write_csv(df2_h2, 'ssp2_developing_capital_investment_h2', TOPICS.COST)

write_csv(df1_ccs, 'ssp1_developing_capital_investment_ccs', TOPICS.COST)
write_csv(df2_ccs, 'ssp2_developing_capital_investment_ccs', TOPICS.COST)

write_csv(df1_evs, 'ssp1_developing_capital_investment_evs', TOPICS.COST)
write_csv(df2_evs, 'ssp2_developing_capital_investment_evs', TOPICS.COST)
