#interactive map with surface temperature, mosqiito habitats, precipitation, and humidities across India
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import requests
from shapely.geometry import Point


# Function to fetch and process data
def fetch_globe_data(protocol):
    url = f"https://api.globe.gov/search/v1/measurement/protocol/measureddate/measurementcountry/?protocols={protocol}&startdate=2015-01-01&enddate=2026-01-01&countrycode=IND&geojson=TRUE&sample=FALSE"

    response = requests.get(url)
    data = response.json()

    # Extract the results
    results = data.get('results', [])
    print(f"{protocol}: {len(results)} records")

    # Create a list to hold our data
    records = []
    for record in results:
        lat = record.get('latitude') or record.get('lat')
        lon = record.get('longitude') or record.get('lon') or record.get('lng')

        if lat is not None and lon is not None:
            records.append({
                'latitude': lat,
                'longitude': lon,
                'geometry': Point(lon, lat),
                **record
            })

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(records, crs=4326) if records else gpd.GeoDataFrame()
    return gdf


# Fetch all four datasets
print("Fetching datasets...")
surface_temp = fetch_globe_data('surface_temperatures')
humidity = fetch_globe_data('humidities')
mosquito = fetch_globe_data('mosquito_habitat_mapper')
precipitation = fetch_globe_data('precipitations')

# Load world countries data
countries = gpd.read_file(
    "https://github.com/geo-di-lab/emerge-lessons/raw/refs/heads/main/docs/data/world_countries.zip"
)[["COUNTRY", "geometry"]].to_crs(4326)

# Filter for India
india = countries[countries["COUNTRY"] == "India"]

# Major Indian cities with coordinates and text positions to avoid overlap
cities = {
    'Mumbai': {'coords': (72.8777, 19.0760), 'textposition': 'middle left'},
    'Delhi': {'coords': (77.1025, 28.7041), 'textposition': 'top center'},
    'Bangalore': {'coords': (77.5946, 12.9716), 'textposition': 'bottom right'},
    'Hyderabad': {'coords': (78.4867, 17.3850), 'textposition': 'middle right'},
    'Chennai': {'coords': (80.2707, 13.0827), 'textposition': 'middle right'},
    'Kolkata': {'coords': (88.3639, 22.5726), 'textposition': 'middle right'},
    'Pune': {'coords': (73.8567, 18.5204), 'textposition': 'bottom center'},
    'Ahmedabad': {'coords': (72.5714, 23.0225), 'textposition': 'middle left'},
    'Jaipur': {'coords': (75.7873, 26.9124), 'textposition': 'top right'},
    'Lucknow': {'coords': (80.9462, 26.8467), 'textposition': 'top center'},
    'Nagpur': {'coords': (79.0882, 21.1458), 'textposition': 'bottom center'},
    'Indore': {'coords': (75.8577, 22.7196), 'textposition': 'middle left'},
    'Bhopal': {'coords': (77.4126, 23.2599), 'textposition': 'bottom left'},
    'Patna': {'coords': (85.1376, 25.5941), 'textposition': 'top center'},
    'Srinagar': {'coords': (74.7973, 34.0837), 'textposition': 'top center'},
    'Chandigarh': {'coords': (76.7794, 30.7333), 'textposition': 'bottom center'},
    'Kochi': {'coords': (76.2673, 9.9312), 'textposition': 'bottom left'},
}

# Create the interactive plot
fig = go.Figure()

# Add India boundary (always visible, not in legend with clickable box)
for i, geom in enumerate(india.geometry):
    if geom.geom_type == 'Polygon':
        x, y = geom.exterior.xy
        fig.add_trace(go.Scattergl(
            x=list(x),
            y=list(y),
            mode='lines',
            line=dict(color='black', width=2),
            fill='toself',
            fillcolor='lightgray',
            name='India Boundary',
            hoverinfo='skip',
            showlegend=(i == 0),
            legendgroup='boundary'
        ))
    elif geom.geom_type == 'MultiPolygon':
        for j, poly in enumerate(geom.geoms):
            x, y = poly.exterior.xy
            fig.add_trace(go.Scattergl(
                x=list(x),
                y=list(y),
                mode='lines',
                line=dict(color='black', width=2),
                fill='toself',
                fillcolor='lightgray',
                name='India Boundary',
                hoverinfo='skip',
                showlegend=False,
                legendgroup='boundary'
            ))

# Add surface temperature points
if not surface_temp.empty:
    fig.add_trace(go.Scattergl(
        x=surface_temp['longitude'],
        y=surface_temp['latitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='orange',
            opacity=0.6,
            line=dict(width=0.5, color='darkorange')
        ),
        name='Surface Temperature',
        visible=True,
        legendgroup='surface_temp',
        hovertemplate='<b>Surface Temperature</b><br>' +
                      'Latitude: %{y:.4f}<br>' +
                      'Longitude: %{x:.4f}<br>' +
                      '<extra></extra>'
    ))

# Add humidity points
if not humidity.empty:
    fig.add_trace(go.Scattergl(
        x=humidity['longitude'],
        y=humidity['latitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='blue',
            opacity=0.6,
            line=dict(width=0.5, color='darkblue')
        ),
        name='Humidity',
        visible=True,
        legendgroup='humidity',
        hovertemplate='<b>Humidity</b><br>' +
                      'Latitude: %{y:.4f}<br>' +
                      'Longitude: %{x:.4f}<br>' +
                      '<extra></extra>'
    ))

# Add mosquito habitat points
if not mosquito.empty:
    fig.add_trace(go.Scattergl(
        x=mosquito['longitude'],
        y=mosquito['latitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            opacity=0.6,
            line=dict(width=0.5, color='darkred')
        ),
        name='Mosquito Habitat',
        visible=True,
        legendgroup='mosquito',
        hovertemplate='<b>Mosquito Habitat</b><br>' +
                      'Latitude: %{y:.4f}<br>' +
                      'Longitude: %{x:.4f}<br>' +
                      '<extra></extra>'
    ))

# Add precipitation points
if not precipitation.empty:
    fig.add_trace(go.Scattergl(
        x=precipitation['longitude'],
        y=precipitation['latitude'],
        mode='markers',
        marker=dict(
            size=8,
            color='purple',
            opacity=0.6,
            line=dict(width=0.5, color='indigo')
        ),
        name='Precipitation',
        visible=True,
        legendgroup='precipitation',
        hovertemplate='<b>Precipitation</b><br>' +
                      'Latitude: %{y:.4f}<br>' +
                      'Longitude: %{x:.4f}<br>' +
                      '<extra></extra>'
    ))

# Add city labels (not in legend)
for city_name, city_info in cities.items():
    lon, lat = city_info['coords']
    textpos = city_info['textposition']

    fig.add_trace(go.Scattergl(
        x=[lon],
        y=[lat],
        mode='markers+text',
        marker=dict(
            size=8,
            color='black',
            symbol='circle',
            line=dict(width=1, color='white')
        ),
        text=[city_name],
        textposition=textpos,
        textfont=dict(
            size=12,
            color='black',
            family='Arial Black'
        ),
        showlegend=False,
        hovertemplate='<b>%{text}</b><br>' +
                      'Latitude: %{y:.4f}<br>' +
                      'Longitude: %{x:.4f}<br>' +
                      '<extra></extra>'
    ))

# Update layout
fig.update_layout(
    title=dict(
        text='Factors Influencing Mosquito Distribution Across India (2015-2026)',
        font=dict(size=18, color='black', family='Arial Black')
    ),
    xaxis_title='Longitude',
    yaxis_title='Latitude',
    hovermode='closest',
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=1,
        itemsizing='constant'
    ),
    width=1200,
    height=900,
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridcolor='lightgray', scaleanchor="x", scaleratio=1)
)

# Show the plot
fig.show()