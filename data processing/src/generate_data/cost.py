import pandas as pd
import numpy as np

from src.consts import SPA1, SSP2, TOPICS
from src.utils import get_data, write_csv, merge_pak2south_asia_new


def get_policy_cost(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/cost/policy_cost.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)
    df = merge_pak2south_asia_new(df)
    p = pd.pivot_table(df, index=['region', 'Year'], values='value', aggfunc=np.sum)
    p.reset_index(level=['region', 'Year'], inplace=True)
    return p

def get_gdp(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data/cost/gdp.xml"
    df = get_data(ssp_name=ssp_scenario, query_path=query_file)
    df = merge_pak2south_asia_new(df)
    p = pd.pivot_table(df, index=['region', 'Year'], values='value', aggfunc=np.sum)
    p.reset_index(level=['region', 'Year'], inplace=True)
    return p

df_policy = get_policy_cost(SPA1)
df_gdp = get_gdp(SPA1)

write_csv(df_policy, 'policy_cost', TOPICS.COST)
write_csv(df_gdp, 'gdp', TOPICS.COST)
