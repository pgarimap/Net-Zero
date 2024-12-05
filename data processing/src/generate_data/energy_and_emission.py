"""
To show present state of energy source and what's required.
Show energy sources in year 2050 in SPA1 and year 2023 SSP 2

"""
import os.path
from os.path import join
import pandas as pd

# get SPA 1 energy sources
from src.consts import SPA1, SSP2
from src.utils import get_data, merge_pak2south_asia, merge_pak2south_asia_new, DEVELOPED_REGIONS, REGIONS


def get_energy_consumption_by_region(ssp_scenario, regions=REGIONS):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/energy_and_emission/primary energy consumption by region.xml"

    # developed_regions = ['USA', 'EU-12', 'EU-15', 'Europe_Eastern', 'Japan',
    #                      'Mexico', 'Canada', ]
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    # columns : 'Units', 'scenario', 'region', 'fuel', 'Year', 'value'
    # merge pakistan into south asia

    cat_col = 'fuel'
    on = ['Year', 'fuel', 'scenario', 'Units']
    # merge pakistan into south asia
    # df = merge_pak2south_asia_new(df)
    return df


def get_spa1_energy_consumption_by_region(regions=REGIONS):
    spa1_df = get_energy_consumption_by_region(SPA1, regions=regions)

    # select a year as a good case scenario to compare present result to
    # taking year 2050
    scenario_year = 2050

    df_2050 = spa1_df[spa1_df['Year'] == scenario_year]
    df_2050.drop(columns=['Year', 'scenario'], inplace=True)
    return df_2050


def get_ssp2_energy_consumption_by_region(current_year=2020, regions=REGIONS):
    df = get_energy_consumption_by_region(SSP2, regions=regions)

    df_current = df[df['Year'] == current_year]
    df_current.drop(columns=['Year', 'scenario'], inplace=True)
    return df_current


# data post processing

fuels = ['a oil', 'b natural gas', 'c coal', 'd biomass', 'e nuclear',
         'f hydro', 'g wind', 'h solar', 'i geothermal',
         'j traditional biomass']

# convert above fuels name to label by removing the letter index and capitalizing the initial letters
fuel2label = {_id: _id[2:].title() for _id in fuels}

df2050 = get_spa1_energy_consumption_by_region(regions=DEVELOPED_REGIONS)
df2020 = get_ssp2_energy_consumption_by_region(regions=DEVELOPED_REGIONS)
df2050_ssp2 = get_ssp2_energy_consumption_by_region(current_year=2050, regions=DEVELOPED_REGIONS)

outpath = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out"
# df2050.to_csv(join(outpath, 'df2050_ene.csv'))
# df2020.to_csv(join(outpath, 'df2020_ene.csv'))
# df2050_ssp2.to_csv(join(outpath, 'df2050_ssp2_ene.csv'))

df2050.to_csv(join(outpath, 'df2050_ene_developed.csv'))
df2020.to_csv(join(outpath, 'df2020_ene_developed.csv'))
df2050_ssp2.to_csv(join(outpath, 'df2050_ssp2_ene_developed.csv'))