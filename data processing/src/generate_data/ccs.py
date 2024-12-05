import pandas as pd
import numpy as np
import sys
sys.path.append('/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing')
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, write_csv, merge_pak2south_asia_new


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

nameMapper_emission = {
    'H2 central production': 'industry',
    'N fertilizer': 'industry',
    'alumina': 'industry', 'cement': 'industry',
    'chemical energy use': 'industry', 'chemical feedstocks': 'industry',
    'construction energy use': 'industry',
    'elec_biomass (IGCC)': 'biomass',
    'elec_biomass (conv)': 'biomass',
    'elec_coal (IGCC)': 'fossil fuel',
    'elec_coal (conv pul)': 'fossil fuel',
    'elec_gas (CC)': 'fossil fuel',
    'elec_refined liquids (CC)': 'refined liquid',
    'elec_biomass (IGCC CCS)': 'biomass',
    'elec_biomass (conv CCS)': 'biomass',
    'elec_coal (IGCC CCS)': 'fossil fuel',
    'elec_coal (conv pul CCS)': 'fossil fuel',
    'elec_gas (CC CCS)': 'fossil fuel',
    'elec_refined liquids (CC CCS)': 'refined liquid',
    'iron and steel': 'industry',
    'other industrial energy use': 'industry',
    'refining': 'industry'
}


def get_sequestration(ssp_scenario, ):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_use_by_tech.xml"
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/technology/sequestration.xml"
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/primary_energy_with_CCS.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)
    df = process_df(df, nameMapper=nameMapper_ccs)
    return df


def process_df(df, nameMapper):
    # df = df[df['Year'] == 2050]

    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)
    keys = [key for key in nameMapper.keys()]
    vals = [key for key in nameMapper.values()]
    df = df[df['sector'].isin(keys)]
    df['sector'] = df['sector'].replace(keys, vals)

    # df.drop(columns=['scenario', 'Year', 'Units'], inplace=True)

    pivot_table = pd.pivot_table(df, index='region', columns='sector', values='value', aggfunc=np.sum)
    return pivot_table.reset_index()


def get_emission(ssp_scenario):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/co2_by_sector.xml"
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/ccs/emission_excluding_resource_production.xml"
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/primary_energy_with_CCS.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file,)
    # df.drop(columns=['scenario', 'Units'], inplace=True)

    return process_df(df, nameMapper_emission)


# df_sub = get_sequestration(SPA1)

# df_emi = get_emission(SPA1)
df_ccs = get_sequestration(SPA1)

write_csv(df_emi, 'emission_for_ccs', TOPICS.CCS)
write_csv(df_ccs, 'sequestration_ccs', TOPICS.CCS)


def merge_emission_n_ccs(emission_data, sequestration_data):
    # Add the "Type" column to both dataframes
    emission_data['Type'] = 'Emission'
    sequestration_data['Type'] = 'CCS'

    # Reorder columns to match the desired format
    columns_order = ['region', 'Type', 'industry', 'biomass', 'fossil fuel', 'refined liquid']
    emission_data = emission_data[columns_order]
    sequestration_data = sequestration_data[columns_order]

    # Concatenate the two dataframes
    combined_data = pd.concat([emission_data, sequestration_data], ignore_index=True)

    # Rename columns to match the Excel file format
    # combined_data.columns = ['Region', 'Type', 'Industry', 'Biomass', 'Fossil Fuel', 'Refined Liquid']

    # Save the combined dataframe to Excel format
    write_csv(combined_data, 'emission_ccs', TOPICS.CCS)


merge_emission_n_ccs(df_emi, df_ccs)
