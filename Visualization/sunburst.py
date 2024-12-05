import pandas as pd
import plotly.express as px
import numpy as np

path = "./data/erlabee4esupp1.xlsx"

df_sector = pd.read_excel(path, sheet_name='sector classification')
# print(df_sector.head())

df_result = pd.pivot_table(df_sector,
                           index=['subsector_ar6'])
# df_result['subsector_ar6'] = pd.to_numeric(df_result['subsector_ar6'])
df_result['total'] = [0 for _ in range(len(df_result))]
df_result['sector'] = ['' for _ in range(len(df_result))]
df_result['subsector'] = ['' for _ in range(len(df_result))]

categories = df_sector['IPCC_AR6_chapter_title'].unique()

for cat in categories:
    df = pd.read_excel(path, sheet_name=f'{cat} trend')
    for i in range(len(df)):
        subsector = df.iloc[i]['subsector']
        subsector_title = df.iloc[i]['subsector_title']

        try:
            df_result.loc[subsector, 'total'] = df.iloc[i][2:].sum()
            df_result.loc[subsector, 'sector'] = cat
            df_result.loc[subsector, 'subsector'] = subsector_title
        except:
            print(f"Not found {subsector}")


print(df_result.head())

fig = px.sunburst(df_result, path=['sector', 'subsector'], values='total',
                  # color='lifeExp', hover_data=['iso_alpha'],
                  # color_continuous_scale='RdBu',
                  # color_continuous_midpoint=np.average(df['lifeExp'], weights=df['total'])
                  )
fig.update_traces(textinfo="label+percent parent")
fig.show()
