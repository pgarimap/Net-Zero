import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, write_csv, merge_pak2south_asia_new


def figure(df_ssp1, df_ssp2):
    years_of_interest = [2030, 2050, 2085]
    df_ssp1_filtered = df_ssp1[df_ssp1['Year'].isin(years_of_interest)]
    df_ssp2_filtered = df_ssp2[df_ssp2['Year'].isin(years_of_interest)]

    # Setting up the plot style
    plt.style.use('seaborn-darkgrid')

    # Creating the bar plot
    fig, axs = plt.subplots(nrows=len(years_of_interest), ncols=1, figsize=(10, 15), sharex=True)

    # Iterate over each year and plot
    for i, year in enumerate(years_of_interest):
        # Merging the two datasets for the specific year
        df_year_ssp1 = df_ssp1_filtered[df_ssp1_filtered['Year'] == year].set_index('region')
        df_year_ssp2 = df_ssp2_filtered[df_ssp2_filtered['Year'] == year].set_index('region')

        # Ensure the regions are the same in both datasets
        common_regions = df_year_ssp1.index.intersection(df_year_ssp2.index)
        df_year_ssp1 = df_year_ssp1.loc[common_regions]
        df_year_ssp2 = df_year_ssp2.loc[common_regions]

        # Plotting the data
        bar_width = 0.35
        index = np.arange(len(common_regions))

        bars1 = axs[i].bar(index, df_year_ssp1['value'], bar_width, label='SSP1')
        bars2 = axs[i].bar(index + bar_width, df_year_ssp2['value'], bar_width, label='SSP2')

        axs[i].set_xlabel('Region')
        axs[i].set_ylabel('Value')
        axs[i].set_title(f'Year {year}')
        axs[i].set_xticks(index + bar_width / 2)
        axs[i].set_xticklabels(common_regions)
        axs[i].legend()

    # Adjust layout
    plt.tight_layout()
    plt.show()


def get_price(ssp_scenario):
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/co2_by_sector.xml"
    query_file = "data/temp.xml"
    # query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/primary_energy_with_CCS.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, )
    # df.drop(columns=['scenario', 'Units'], inplace=True)

    return df


df_1 = get_price(SPA1)
cats = ['labor-force', 'population', 'GDP', 'capital-net-export',
       'capital-stock', 'consumer-durable', 'depreciation',
       'energy-investment', 'energy-net-export', 'energy-service',
       'energy-service-value', 'gdp-per-capita', 'gdp-per-capita-ppp',
       'gross-output', 'investment', 'labor-wages',
       'materials-net-export', 'savings', 'total-factor-productivity',
       'value-added', 'savings-rate', 'fac-share-capital',
       'fac-share-energy', 'fac-share-labor']

df_1 = df_1[df_1['Account']=='savings']
df_1 = pd.pivot_table(df_1, index=['region', 'Year'], values='value', aggfunc=np.sum).reset_index()
df_2 = get_price(SSP2)
df_2 = df_2[df_2['Account']=='savings']
df_2 = pd.pivot_table(df_2, index=['region', 'Year'], values='value', aggfunc=np.sum).reset_index()

figure(df_1, df_2)