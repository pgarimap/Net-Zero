import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path1 = '/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out/technology/energy_by_fuel_ssp1.csv'
path2 = '/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out/technology/energy_by_fuel_ssp2.csv'

co2_path1 = '/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out/technology/ssp1_co2_by_input.csv'
co2_path2 = '/Users/pramish/Desktop/Codes/netzero/gcam_code/data_out/technology/ssp2_co2_by_input.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

co2_df1 = pd.read_csv(co2_path1)
co2_df2 = pd.read_csv(co2_path2)

selected_years = [2020, 2025, 2030, 2050, 2085]

# filter year
df1 = df1[df1['Year'].isin(selected_years)]
df2 = df2[df2['Year'].isin(selected_years)]

co2_df1 = co2_df1[co2_df1['Year'].isin(selected_years)]
co2_df2 = co2_df2[co2_df2['Year'].isin(selected_years)]

regions = pd.unique(df1['region'])
result = {
    region: None for region in regions
}
all_region1 = pd.pivot_table(df1, index=['input'], columns=['Year'], values='value', aggfunc=np.sum)
all_region2 = pd.pivot_table(df2, index=['input'], columns=['Year'], values='value', aggfunc=np.sum)

for region in regions[::-1]:
    print('--------------Region: ', region, '----------------')
    df1_ = df1[df1['region'] == region]
    df2_ = df2[df2['region'] == region]

    df1_ = pd.pivot_table(df1_, index=['input'], columns=['Year'], values='value', aggfunc=np.sum)
    df2_ = pd.pivot_table(df2_, index=['input'], columns=['Year'], values='value', aggfunc=np.sum)

    # df1_.drop(index=['hydrogen'], inplace=True)
    # df2_.drop(index=['hydrogen'], inplace=True)

    # # energy mix percentage
    # for col in df1_.columns:
    #     for index in df1_.index:
    #         df1_.loc[index]['mix'] = df1_.loc[index][col] / df1_[col].sum()
    #         df2_.loc[index]['mix'] = df2_.loc[index][col] / df2_[col].sum()

    co2_df1_ = pd.pivot_table(co2_df1, index=['technology'], columns=['Year'], values='value', aggfunc=np.sum)
    co2_df2_ = pd.pivot_table(co2_df2, index=['technology'], columns=['Year'], values='value', aggfunc=np.sum)

    # find percentage change in both scenario
    def find_dff_percentage(df):
        df_percentage_diff = df.copy()  # Create a copy of the original dataframe

        # Calculate the percentage difference for each year based on 2025
        for column in df_percentage_diff.columns:
            df_percentage_diff[column] = ((df[column] - df[2025]) / df[2025]) * 100

        return df_percentage_diff


    diff1 = find_dff_percentage(df1_)
    diff2 = find_dff_percentage(df2_)

    diff = diff1 - diff2
    result[region] = {
        'ssp1': df1_,
        'ssp2': df2_,
        'ssp1_diff_ssp2': diff
    }

    print('-' * 20)
    print("SSP1")
    print('-' * 20)
    print(df1_)
    print('-' * 20)
    print("SSP2")
    print('-' * 20)
    print(df2_)
    print('-' * 20)
    # print(diff)
    print('-' * 20)

# Plotting the data
for region in result:
    print('--------------Region: ', region, '----------------')
    diff1 = result[region]['ssp1']
    diff2 = result[region]['ssp2']
    diff = result[region]['ssp1_diff_ssp2']

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Plot for SSP1
    axes[0].set_title('SSP1')
    diff1.plot(ax=axes[0], kind='bar')
    axes[0].set_ylabel('Percentage Difference')

    # Plot for SSP2
    axes[1].set_title('SSP2')
    diff2.plot(ax=axes[1], kind='bar')
    axes[1].set_ylabel('Percentage Difference')

    # Plot for the difference between SSP1 and SSP2
    axes[2].set_title('Difference: SSP1 - SSP2')
    diff.plot(ax=axes[2], kind='bar')
    axes[2].set_ylabel('Percentage Difference')

    fig.suptitle(region)
plt.tight_layout()
plt.show()
