import pandas as pd

from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, merge_pak2south_asia, write_csv, merge_pak2south_asia_new, REGIONS, DEVELOPED_REGIONS


def get_hydrogen_production_by_tech(ssp_scenario, regions=REGIONS):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/h2_input_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=regions)

    # columns : 'Units', 'scenario', 'region', 'fuel', 'Year', 'value'
    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia_new(df)
    df = df[df['Year'].isin([2030, 2040, 2050])]
    f = pd.pivot_table(df, index=['Year', 'technology', 'region'], values='value', aggfunc='sum').reset_index()
    return f


df_1 = get_hydrogen_production_by_tech(SPA1)
df_2 = get_hydrogen_production_by_tech(SSP2)

df_1_developed = get_hydrogen_production_by_tech(SPA1, regions=DEVELOPED_REGIONS)
df_2_developed = get_hydrogen_production_by_tech(SSP2, regions=DEVELOPED_REGIONS)

write_csv(df_1, 'spa1_developing_h2_input_by_tech', TOPICS.TECHNOLOGY)
write_csv(df_2, 'ssp2_developing_h2_input_by_tech', TOPICS.TECHNOLOGY)

write_csv(df_2_developed, 'spa1_developed_h2_input_by_tech', TOPICS.TECHNOLOGY)
write_csv(df_2_developed, 'ssp2_developed_h2_input_by_tech', TOPICS.TECHNOLOGY)
