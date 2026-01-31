import pandas as pd                           # For working with data
pd.set_option("display.max_columns", None)    # Lets us see all columns of the data instead of just a preview
import geopandas as gpd                       # For working with spatial data
import numpy as np                            # For working with numbers
import matplotlib.pyplot as plt               # For making graphs
from datetime import date                     # For formatting dates
from PIL import Image                         # For getting and displaying images from links
import requests                               # For getting information from links
from io import BytesIO                        # For working with types of input and output

url = "https://api.globe.gov/search/v1/measurement/protocol/measureddate/country/?protocols=mosquito_habitat_mapper&startdate=2015-01-01&enddate=2026-01-01&countrycode=IND&geojson=TRUE&sample=FALSE"

response = requests.get(url)
geojson_data = response.json()

data = gpd.GeoDataFrame.from_features(geojson_data["features"])

data.head(10)

print(data.head())
print(data.columns)
print(data.crs)

response = requests.get(url)
geojson_data = response.json()

data = gpd.GeoDataFrame.from_features(geojson_data["features"])
data = data.set_crs(4326)

print("Mosquito points:", len(data))

countries = gpd.read_file(
    "https://github.com/geo-di-lab/emerge-lessons/raw/refs/heads/main/docs/data/world_countries.zip"
)[["COUNTRY", "geometry"]].to_crs(4326)

india = countries[countries["COUNTRY"] == "India"]

fig, ax = plt.subplots(figsize=(10,8))

# Plot India boundary
india.plot(ax=ax, color="lightgray", edgecolor="black")

# Plot mosquito points
data.plot(ax=ax, color="red", markersize=40)

# Force zoom to India
ax.set_xlim(india.total_bounds[0], india.total_bounds[2])
ax.set_ylim(india.total_bounds[1], india.total_bounds[3])

plt.title("Mosquito Habitat Mapper Observations in India (2015–2026)")
plt.show()

