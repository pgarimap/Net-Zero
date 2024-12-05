import pandas as pd

path = "/Users/pramish/Downloads/mac_curve.csv"

df = pd.read_csv(path)
x_axis = df.columns[4: -1]

pivot = pd.pivot_table(df, columns=['CostCurves'], values='')

print(x_axis)