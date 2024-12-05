import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read data from CSV files
from constants import FIG_SIZE_SINGLE, DISPLAY_DIP
from helpers.colors import set_stacked_area_colors

file1 = "../../preprocessed_data/technology/spa1_hydrogen_production_by_tech.csv"
file2 = "../../preprocessed_data/technology/ssp2_hydrogen_production_by_tech.csv"

cost_file1 = "../../preprocessed_data/technology/spa1_hydrogen_cost_by_tech.csv"
cost_file2 = "../../preprocessed_data/technology/ssp2_hydrogen_cost_by_tech.csv"

df1 = pd.read_csv(file1, index_col=0)
df2 = pd.read_csv(file2, index_col=0)

pt1 = pd.pivot_table(df1, index=['Year'], values='value', aggfunc=np.sum)
pt1.reset_index(inplace=True)

pt2 = pd.pivot_table(df2, index=['Year'], values='value', aggfunc=np.sum)
pt2.reset_index(inplace=True)

# cost data
cost_df1 = pd.read_csv(cost_file1, index_col=0)
cost_df2 = pd.read_csv(cost_file2, index_col=0)

cost_pt1 = pd.pivot_table(cost_df1, index=['Year'], values='value', aggfunc=np.median)
cost_pt1.reset_index(inplace=True)
cost_pt2 = pd.pivot_table(cost_df2, index=['Year'], values='value', aggfunc=np.median)
cost_pt2.reset_index(inplace=True)

# plot

plt.plot(pt1['Year'], pt1['value'], color='green', label="SPA1")
plt.plot(pt2['Year'], pt2['value'], color='red', label="SSP2")
plt.legend()
plt.show()
#
plt.plot(cost_pt1['Year'], cost_pt1['value'], color='green', label="SPA1")
plt.plot(cost_pt2['Year'], cost_pt2['value'], color='red', label="SSP2")
plt.legend()
plt.show()


