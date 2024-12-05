import geopandas as gpd
import matplotlib.pyplot as plt

# Load the world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Set up the color map
cmap = {'India': 'darkred', 'China': 'darkred', 'Brazil': 'darkred',
        'Pakistan': 'orange', 'Bangladesh': 'orange', 'Nepal': 'orange', 'Sri Lanka': 'orange', 'Bhutan': 'orange', 'Maldives': 'orange',
        'Senegal': 'orange', 'Guinea': 'orange', 'Sierra Leone': 'orange', 'Liberia': 'orange', 'Ivory Coast': 'orange', 'Ghana': 'orange', 'Togo': 'orange', 'Benin': 'orange', 'Nigeria': 'orange'}

# Apply colors to countries; all others in light grey
world['color'] = world['name'].apply(lambda x: cmap.get(x, 'lightgrey'))

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(ax=ax, color=world['color'], legend=True)

# Custom legend
import matplotlib.patches as mpatches
major_patch = mpatches.Patch(color='darkred', label='Major Emitting Regions (India, China, Brazil)')
minor_patch = mpatches.Patch(color='orange', label='Minor Emitting Regions (South Asia, Western Africa)')
plt.legend(handles=[major_patch, minor_patch])

plt.title('Major and Minor Carbon Emitting Regions')
plt.show()
