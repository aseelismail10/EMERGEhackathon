import pandas as pd                           # For working with data
pd.set_option("display.max_columns", None)    # Lets us see all columns of the data instead of just a preview
import geopandas as gpd                       # For working with spatial data
import numpy as np                            # For working with numbers
import matplotlib.pyplot as plt               # For making graphs
from datetime import date                     # For formatting dates
from PIL import Image                         # For getting and displaying images from links
import requests                               # For getting information from links
from io import BytesIO                        # For working with types of input and output

url = "https://api.globe.gov/search/v1/measurement/protocol/measureddate/country/?protocols=mosquito_habitat_mapper&startdate=2025-01-01&enddate=2026-01-01&countrycode=IND&geojson=TRUE&sample=FALSE"

response = requests.get(url)
geojson_data = response.json()

data = gpd.GeoDataFrame.from_features(geojson_data["features"])

end_date = "2024-12-31"

data.head(10)

print(data.head())
print(data.columns)
print(data.crs)

