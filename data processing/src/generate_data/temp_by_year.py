from src.consts import SPA1, SSP2, TOPICS
from src.utils import get_data, write_csv


def get_global_temp(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/intro/temp_by_year.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file, regions=None)
    return df


df_ssp1 = get_global_temp(SPA1)
df_ssp2 = get_global_temp(SSP2)

write_csv(df_ssp1, 'global_mean_temp_ssp1', TOPICS.INTRO)
write_csv(df_ssp2, 'global_mean_temp_ssp2', TOPICS.INTRO)
