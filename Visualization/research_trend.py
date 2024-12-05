import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import numpy as np

# reading data from csv
path = "./data/Scopus_Data.csv"
df = pd.read_csv(path, encoding='unicode_escape')
df['count'] = [1 for _ in range(len(df))]

# print data in console for reference
print(df.head())
print(df.columns)

# group row by Year and count
df_pivot = pd.pivot_table(df, index=['Year'], values=['count'], aggfunc=np.sum)
# remove 2023 as it has only 1 paper of this date
df_pivot.drop(index=[2023], inplace=True)
print(df_pivot.head())

# x = year and y=count
x, y = df_pivot.index, df_pivot.values.reshape(-1)

# global params

fsize = 9
tsize = 18
tdir = 'out'
major = 5.0
minor = 3.0
lwidth = 1.5# to bold the axes boundary i.e. spines
lhandle = 2.0
plt.style.use('default')
plt.rcParams['text.usetex'] = False
plt.rcParams['font.size'] = fsize
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['legend.fontsize'] = tsize
plt.rcParams['xtick.direction'] = tdir
plt.rcParams['ytick.direction'] = tdir
plt.rcParams['xtick.major.size'] = major # tick size
plt.rcParams['xtick.minor.size'] = minor
plt.rcParams['ytick.major.size'] = 5.0
plt.rcParams['ytick.minor.size'] = 3.0
plt.rcParams['axes.linewidth'] = lwidth
plt.rcParams['legend.handlelength'] = lhandle
plt.rcParams['lines.linewidth']= 1.5


# plot using matplotlib
plt.plot(x, y)
plt.xlabel('Year', fontname= 'Times New Roman', fontweight='bold', fontsize='12')
plt.ylabel('Number of Papers Published',fontname= 'Times New Roman', fontweight='bold', fontsize='12')

ax=plt.subplot()
# hide top and right spines
#ax.spines.right.set_visible(False)
#ax.spines.top.set_visible(False)

# ax.x(fontweight=1.5)
# ax.y(fontweigth=1.5)

# x axis labels spacing control

# ax.xaxis.set_minor_locator(MultipleLocator(0)) # minor tick in X axis # span of 1 year
# ax.yaxis.set_minor_locator(MultipleLocator(.05))

# ax.set_xticks([1980,1990,2000,2010,2020], fontweight='bold')
# ax.set_yticks([0,50,100,150,200,250,300],fontweight='bold' )

plt.show()
