import geopandas as gpd
import folium

# Load the shapefile
footprints = gpd.read_file('BuildingFootprints_NE_India.shp')

# Calculate area in square meters (assuming EPSG:4326, you may need to project to a metric CRS first)
footprints = footprints.to_crs(epsg=3857)
footprints['area'] = footprints.geometry.area

# Define solar radiation and efficiency
solar_radiation = 5.5  # Example value in kWh/m^2/day
efficiency = 0.15  # Solar panel efficiency

# Calculate potential solar energy generation
footprints['solar_energy'] = footprints['area'] * solar_radiation * efficiency

# Define a threshold for coloring
threshold = 1000  # Example threshold value for solar energy

# Create a map centered on the region of interest
latitude, longitude = 25.5, 93.0  # Example coordinates for North-East India
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add building footprints to the map
for _, row in footprints.iterrows():
    folium.GeoJson(
        row['geometry'], 
        style_function=lambda x, row=row: {'color': 'green' if row['solar_energy'] > threshold else 'red'}
    ).add_to(m)

# Save the map to an HTML file
m.save('solar_potential_map.html')
