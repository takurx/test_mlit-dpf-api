import streamlit as st
import leafmap.foliumap as lfmap
import json
import pandas as pd

# Set page title
st.set_page_config(page_title="Geographic Data Visualization", layout="wide")

# Title and introduction
st.title("Geographic Data Visualization")
st.markdown("This app visualizes the geographic points from the JSON data.")

# Function to load JSON data
@st.cache_data
def load_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

# Load the JSON data
data = load_data("test_simple_search-2_result-1.json")

# Extract locations from JSON
locations = []
if "data" in data and "search" in data["data"] and "searchResults" in data["data"]["search"]:
    for result in data["data"]["search"]["searchResults"]:
        if "title" in result and "lat" in result and "lon" in result:
            locations.append({
                "title": result["title"],
                "lat": result["lat"],
                "lon": result["lon"]
            })

# Create a DataFrame from the locations
if locations:
    df = pd.DataFrame(locations)
    
    # Display data table
    st.subheader("Data Table")
    st.dataframe(df)
    
    # Create the map
    st.subheader("Map Visualization")
    
    # Create a map centered around the mean latitude and longitude
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    
    m = lfmap.Map(center=(center_lat, center_lon), zoom=10)
    
    # Add points to the map
    for _, row in df.iterrows():
        popup = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
        m.add_marker(location=(row['lat'], row['lon']), popup=popup)
    
    # Display the map
    m.to_streamlit(height=600)
else:
    st.error("No valid location data found in the JSON file.")
