import pandas as pd
import seaborn as sns
import sys

sys.path.append("../../")
import matplotlib.pyplot as plt

from helpers.io import save

from constants import FIG_SINGLE_WIDTH, mm2inch

# Load the data
data = pd.read_csv(
    "preprocessed_data/ccs/emission_ccs.csv", index_col=0)

data['region'] = data['region'].replace(['Africa_Western'], ['Western Africa'])
# Split the dataframe into two: one for CCS and one for Emission
ccs_data = data[data['Type'] == 'CCS'].set_index('region')
emission_data = data[data['Type'] == 'Emission'].set_index('region')

# Calculate the percentage: (ccs/emission) * 100
percentage_data = (ccs_data.drop(columns='Type') / (
            ccs_data.drop(columns='Type') + emission_data.drop(columns='Type'))) * 100

# Set up the figure and axis
plt.figure(figsize=(FIG_SINGLE_WIDTH, mm2inch(50)))

# Create the heatmap
# Here, the data annotations will be the CCS values, but the color is determined by the percentage
heatmap = sns.heatmap(percentage_data,
                      annot=ccs_data.drop(columns='Type'),  # Annotate with CCS values
                      cmap='YlGnBu',  # Color map for the heatmap
                      cbar_kws={'label': 'CCS/Emission (%)'},
                      vmin=0, vmax=100,  # Setting the color scale limits
                      linewidths=.5,
                      fmt=".2f",  # Formatting for the annotations
                      mask=(percentage_data.isnull()),  # Masking NaN values
                      )

# Set the title and labels
# heatmap.set_title('CCS Values with Color Intensity based on CCS/Emission (%)')

# set xticks
xtick_labels = data.columns[2:]
tick_positions = [0.5 + i for i in range(len(xtick_labels))]
tick_labels = [x.title() for x in xtick_labels]
plt.xticks(ticks=tick_positions, labels=tick_labels)

# rotate y labels to make it horizontal
plt.yticks(rotation=0)
# Remove x and y tick lines
plt.tick_params(axis='both', length=0)
plt.ylabel('')
plt.xlabel('')

plt.tight_layout()
# plt.show()
save('ccs_heatmap')
