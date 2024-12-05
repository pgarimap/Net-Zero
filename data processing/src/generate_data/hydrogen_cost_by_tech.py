from src.consts import SPA1, SSP2, TOPICS

from src.utils import get_data, merge_pak2south_asia, write_csv

rename = {
    'H2 retail dispensing': "H2",
}


def get_hydrogen_cost_by_tech(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/technology/hydrogen_cost_by_tech.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)

    # columns : 'Units', 'scenario', 'region', 'fuel', 'Year', 'value'
    # merge pakistan into south asia

    cat_col = 'technology'
    on = ['Year', 'sector', cat_col, 'subsector', 'scenario', 'Units']
    df = df[df['Year'] > 1995]
    # merge pakistan into south asia
    df = merge_pak2south_asia(df, cat_col, on)

    # rename
    # df['input'] = df['input'].replace(rename.keys(), rename.values())
    return df


df_1 = get_hydrogen_cost_by_tech(SPA1)
df_2 = get_hydrogen_cost_by_tech(SSP2)

write_csv(df_1, 'spa1_hydrogen_cost_by_tech', TOPICS.TECHNOLOGY)
write_csv(df_2, 'ssp2_hydrogen_cost_by_tech', TOPICS.TECHNOLOGY)
