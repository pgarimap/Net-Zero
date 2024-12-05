import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

h2 = pd.read_csv(
    '/Users/pramish/Desktop/Codes/netzero/Visualization/preprocessed_data/finance/capital/ssp1_developing_capital_investment_h2.csv',
    index_col=0)
ccs = pd.read_csv(
    '/Users/pramish/Desktop/Codes/netzero/Visualization/preprocessed_data/finance/capital/ssp1_developing_capital_investment_ccs.csv',
    index_col=0)
#
# h2.loc[h2['region'].isin(['Africa_Western', 'South Asia']), 'region'] = 'non-emerging'
# h2.loc[h2['region'].isin(['Brazil', "India", "China"]), 'region'] = 'emerging'
#
# ccs.loc[ccs['region'].isin(['Africa_Western', 'South Asia']), 'region'] = 'non-emerging'
# ccs.loc[ccs['region'].isin(['Brazil', "India", "China"]), 'region'] = 'emerging'

merged_df = pd.merge(h2, ccs, on=['Year', 'region'])
merged_df.rename(columns={'value_x': 'H2', 'value_y': 'CCS'}, inplace=True)

merged_df['CCS'] = merged_df['CCS'] * 5.71
merged_df['H2'] = merged_df['H2'] * 5.71

merged_df = pd.pivot_table(merged_df, index=['region', 'Year'], values=['H2', 'CCS'], aggfunc='sum')
df_unstacked = merged_df.unstack(level='Year')

df_unstacked.to_excel('./results/tables/ccs_h2_capital_investment.xlsx')