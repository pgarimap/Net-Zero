import matplotlib.pyplot as plt

# Data
regions = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5']
oil = [10, 20, 15, 25, 30]
hydro = [5, 10, 12, 20, 25]
solar = [2, 8, 5, 15, 18]
wind = [8, 15, 10, 22, 18]
nuclear = [7, 9, 5, 19, 16]
coal = [20, 18, 25, 30, 28]
natural_gas = [15, 12, 20, 25, 22]
geothermal = [3, 5, 4, 10, 8]

# Plotting
fig, ax = plt.subplots()
ax.scatter(regions, oil, marker='o', s=100, label='Oil')
ax.scatter(regions, hydro, marker='s', s=100, label='Hydro')
ax.scatter(regions, solar, marker='^', s=100, label='Solar')
ax.scatter(regions, wind, marker='v', s=100, label='Wind')
ax.scatter(regions, nuclear, marker='d', s=100, label='Nuclear')
ax.scatter(regions, coal, marker='p', s=100, label='Coal')
ax.scatter(regions, natural_gas, marker='*', s=100, label='Natural Gas')
ax.scatter(regions, geothermal, marker='+', s=100, label='Geothermal')

# Adding labels, legend and lines
# ax.set_xlabel('Regions')
# ax.set_xticklabels(regions, rotation=45*2, ha='right')

ax.set_ylabel('Electricity Generated (in GWh)')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
for i in range(0, 5):
    ax.axvline(x=i + 0.5, linestyle='-', color='gray', alpha=0.7)
for i in range(0, 35, 5):
    ax.axhline(y=i, linestyle='-', color='gray', alpha=0.5)

# Show plot
plt.tight_layout()
plt.show()
