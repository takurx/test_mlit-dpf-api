import streamlit as st
import leafmap.foliumap as lfmap
import json
import pandas as pd
import requests
from datetime import datetime

# Set page title
st.set_page_config(page_title="Geographic Data Visualization", layout="wide")

# Title and introduction
st.title("Geographic Data Visualization")
st.markdown("This app visualizes the geographic points from both a JSON file and Kyun sightings API.")

# Function to load JSON data
@st.cache_data
def load_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

# Function to fetch data from Kyun API
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_kyun_data(api_url="http://localhost:5000/api/kyun/sightings"):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching API data: {str(e)}")
        return None

# Tabs for different data sources
tab1, tab2, tab3 = st.tabs(["JSON Data", "Kyun API Data", "Combined Map"])

# Tab 1: JSON Data
with tab1:
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
        df_json = pd.DataFrame(locations)
        
        # Display data table
        st.subheader("JSON Data Table")
        st.dataframe(df_json)
        
        # Create the map
        st.subheader("JSON Data Map Visualization")
        
        # Create a map centered around the mean latitude and longitude
        center_lat = df_json["lat"].mean()
        center_lon = df_json["lon"].mean()
        
        m_json = lfmap.Map(center=(center_lat, center_lon), zoom=10)
        
        # Add points to the map
        for _, row in df_json.iterrows():
            popup = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
            m_json.add_marker(location=(row['lat'], row['lon']), popup=popup)
        
        # Display the map
        m_json.to_streamlit(height=600)
    else:
        st.error("No valid location data found in the JSON file.")

# Tab 2: Kyun API Data
with tab2:
    # Fetch Kyun API data
    kyun_data = fetch_kyun_data()
    
    if kyun_data and "data" in kyun_data:
        # Extract locations from Kyun API data
        kyun_locations = []
        for item in kyun_data["data"]:
            if "location" in item and "coordinates" in item["location"]:
                kyun_locations.append({
                    "name": item["location"]["name"],
                    "description": item["description"],
                    "lat": item["location"]["coordinates"]["latitude"],
                    "lon": item["location"]["coordinates"]["longitude"]
                })
        
        # Create a DataFrame from the Kyun locations
        if kyun_locations:
            df_kyun = pd.DataFrame(kyun_locations)
            
            # Display data table
            st.subheader("Kyun Sightings Data Table")
            st.dataframe(df_kyun)
            
            # Create the map
            st.subheader("Kyun Sightings Map Visualization")
            
            # Create a map centered around the mean latitude and longitude
            center_lat = df_kyun["lat"].mean()
            center_lon = df_kyun["lon"].mean()
            
            m_kyun = lfmap.Map(center=(center_lat, center_lon), zoom=10)
            
            # Add points to the map with custom styling for Kyun sightings
            for _, row in df_kyun.iterrows():
                popup = f"<b>{row['name']}</b><br>{row['description']}<br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                m_kyun.add_marker(
                    location=(row['lat'], row['lon']), 
                    popup=popup,
                    icon_name="deer",
                    icon_color="orange"
                )
            
            # Display the map
            m_kyun.to_streamlit(height=600)
        else:
            st.error("No valid location data found in the Kyun API response.")
    else:
        st.error("Unable to fetch data from Kyun API. Make sure the API server is running.")

# Tab 3: Combined Map
with tab3:
    # Check if we have both datasets
    has_json_data = 'df_json' in locals() and not df_json.empty
    has_kyun_data = 'df_kyun' in locals() and not df_kyun.empty
    
    if has_json_data or has_kyun_data:
        st.subheader("Combined Map Visualization")
        
        # Determine center coordinates based on available data
        if has_json_data and has_kyun_data:
            # Use the average of both datasets
            all_lats = pd.concat([df_json["lat"], df_kyun["lat"]])
            all_lons = pd.concat([df_json["lon"], df_kyun["lon"]])
            center_lat = all_lats.mean()
            center_lon = all_lons.mean()
        elif has_json_data:
            center_lat = df_json["lat"].mean()
            center_lon = df_json["lon"].mean()
        else:
            center_lat = df_kyun["lat"].mean()
            center_lon = df_kyun["lon"].mean()
        
        # Create a combined map
        m_combined = lfmap.Map(center=(center_lat, center_lon), zoom=9)
        
        # Add legend to the map
        legend_dict = {}
        
        # Add JSON data points to the map if available
        if has_json_data:
            legend_dict["JSON Data"] = "blue"
            for _, row in df_json.iterrows():
                popup = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                m_combined.add_marker(
                    location=(row['lat'], row['lon']), 
                    popup=popup,
                    icon_name="info-sign",
                    icon_color="blue"
                )
        
        # Add Kyun data points to the map if available
        if has_kyun_data:
            legend_dict["Kyun Sightings"] = "orange"
            for _, row in df_kyun.iterrows():
                popup = f"<b>{row['name']}</b><br>{row['description']}<br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                m_combined.add_marker(
                    location=(row['lat'], row['lon']), 
                    popup=popup,
                    icon_name="deer",
                    icon_color="orange"
                )
        
        # Add the legend
        m_combined.add_legend(title="Data Sources", legend_dict=legend_dict)
        
        # Display the map
        m_combined.to_streamlit(height=700)
        
        # Add timestamp
        st.caption(f"Map generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("No data available to create a combined map.")
