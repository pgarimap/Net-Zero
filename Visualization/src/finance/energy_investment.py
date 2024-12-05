import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

df_ssp1 = pd.read_csv('preprocessed_data/finance/energy_investment_ssp1.csv')
df_ssp2 = pd.read_csv('preprocessed_data/finance/energy_investment_ssp2.csv')
# Filtering the data for the years 2030, 2050, and 2085
