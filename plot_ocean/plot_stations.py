import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# File path containing lon, lat, and ocean basin data
file_path = "/scratch1/NCEPDEV/da/Edward.Givelberg/workflow06112024/global-workflow/sorc/gdas.cd/ush/ioda/bufr2ioda/marine/argo.txt"

# Lists to store data from file
lon = []
lat = []
ocean_basin = []

# Read data from file
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        lon.append(float(parts[1]))
        lat.append(float(parts[0]))
        ocean_basin.append(int(parts[2]))

# Initialize the plot
plt.figure(figsize=(12, 8))

# Create a Cartopy map with PlateCarree projection (latitude/longitude)
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines and borders
ax.coastlines()
# ax.add_feature(ccrs.BORDERS, linestyle=':', linewidth=0.5)

# Scatter plot with colored dots for each basin type
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
for basin_type in range(6):
    indices = [i for i, val in enumerate(ocean_basin) if val == basin_type]
    ax.scatter([lon[i] for i in indices], [lat[i] for i in indices], color=colors[basin_type], label=f'Basin {basin_type}', alpha=0.7)

# Add a legend
plt.legend(loc='lower left')

# Add title and show plot
plt.title('Ocean Basins Plot using Cartopy')
# plt.show()
plt.savefig("argo.png")

