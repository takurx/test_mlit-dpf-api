import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd
import requests
from datetime import datetime

# Set page title
st.set_page_config(page_title="Geographic Data Visualization", layout="wide")

# Title and introduction
st.title("Geographic Data Visualization")
st.markdown("This app visualizes the geographic points from both a JSON file and kyon sightings API.")

# Function to load JSON data
@st.cache_data
def load_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

# Function to fetch data from kyon API
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_kyon_data(api_url="http://localhost:5000/api/kyon/sightings"):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching API data: {str(e)}")
        return None

# Tabs for different data sources
tab1, tab2, tab3 = st.tabs(["JSON Data", "kyon API Data", "Combined Map"])

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
        
        m_json = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add points to the map
        for _, row in df_json.iterrows():
            popup_text = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=row['title'],
                icon=folium.Icon(icon="info-sign", prefix="fa", color="blue")
            ).add_to(m_json)
        
        # Display the map
        folium_static(m_json, height=600)
    else:
        st.error("No valid location data found in the JSON file.")

# Tab 2: kyon API Data
with tab2:
    # Fetch kyon API data
    kyon_data = fetch_kyon_data()
    
    if kyon_data and "data" in kyon_data:
        # Extract locations from kyon API data
        kyon_locations = []
        for item in kyon_data["data"]:
            if "location" in item and "coordinates" in item["location"]:
                kyon_locations.append({
                    "name": item["location"]["name"],
                    "description": item["description"],
                    "lat": item["location"]["coordinates"]["latitude"],
                    "lon": item["location"]["coordinates"]["longitude"]
                })
        
        # Create a DataFrame from the kyon locations
        if kyon_locations:
            df_kyon = pd.DataFrame(kyon_locations)
            
            # Display data table
            st.subheader("kyon Sightings Data Table")
            st.dataframe(df_kyon)
            
            # Create the map
            st.subheader("kyon Sightings Map Visualization")
            
            # Create a map centered around the mean latitude and longitude
            center_lat = df_kyon["lat"].mean()
            center_lon = df_kyon["lon"].mean()
            
            m_kyon = folium.Map(location=[center_lat, center_lon], zoom_start=10)
            
            # Add a title to the map
            title_html = '''
            <h3 align="center" style="font-size:16px"><b>つくば市内キョン目撃情報マップ</b></h3>
            '''
            m_kyon.get_root().html.add_child(folium.Element(title_html))
            
            # Add points to the map with custom styling for kyon sightings
            for _, row in df_kyon.iterrows():
                popup_text = f"""
                <b>{row['name']}</b><br>
                {row['description']}<br>
                緯度: {row['lat']}<br>
                経度: {row['lon']}
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['name'],
                    icon=folium.Icon(icon="paw", prefix="fa", color="orange")
                ).add_to(m_kyon)
            
            # Display the map
            folium_static(m_kyon, height=600)
        else:
            st.error("No valid location data found in the kyon API response.")
    else:
        st.error("Unable to fetch data from kyon API. Make sure the API server is running.")

# Tab 3: Combined Map
with tab3:
    # Check if we have both datasets
    has_json_data = 'df_json' in locals() and not df_json.empty
    has_kyon_data = 'df_kyon' in locals() and not df_kyon.empty
    
    if has_json_data or has_kyon_data:
        st.subheader("Combined Map Visualization")
        
        # Determine center coordinates based on available data
        if has_json_data and has_kyon_data:
            # Use the average of both datasets
            all_lats = pd.concat([df_json["lat"], df_kyon["lat"]])
            all_lons = pd.concat([df_json["lon"], df_kyon["lon"]])
            center_lat = all_lats.mean()
            center_lon = all_lons.mean()
        elif has_json_data:
            center_lat = df_json["lat"].mean()
            center_lon = df_json["lon"].mean()
        else:
            center_lat = df_kyon["lat"].mean()
            center_lon = df_kyon["lon"].mean()
        
        # Create a combined map
        m_combined = folium.Map(location=[center_lat, center_lon], zoom_start=9)
        
        # Add a title to the map
        title_html = '''
        <h3 align="center" style="font-size:16px"><b>Combined Geographic Visualization</b></h3>
        '''
        m_combined.get_root().html.add_child(folium.Element(title_html))
        
        # Add JSON data points to the map if available
        if has_json_data:
            for _, row in df_json.iterrows():
                popup_text = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['title'],
                    icon=folium.Icon(icon="info-sign", prefix="fa", color="blue")
                ).add_to(m_combined)
        
        # Add kyon data points to the map if available
        if has_kyon_data:
            for _, row in df_kyon.iterrows():
                popup_text = f"""
                <b>{row['name']}</b><br>
                {row['description']}<br>
                緯度: {row['lat']}<br>
                経度: {row['lon']}
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['name'],
                    icon=folium.Icon(icon="paw", prefix="fa", color="orange")
                ).add_to(m_combined)
        
        # Add a legend to the map
        legend_html = '''
        <div style="position: fixed; 
            bottom: 50px; right: 50px; z-index: 1000;
            background-color: white; padding: 10px; 
            border: 2px solid grey; border-radius: 5px;
            font-size: 14px;">
            <p><b>Data Sources</b></p>
            <p><i class="fa fa-info-sign fa-2x" style="color:blue"></i> JSON Data</p>
            <p><i class="fa fa-paw fa-2x" style="color:orange"></i> kyon Sightings</p>
        </div>
        '''
        m_combined.get_root().html.add_child(folium.Element(legend_html))
        
        # Display the map
        folium_static(m_combined, height=700)
        
        # Add timestamp
        st.caption(f"Map generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.error("No data available to create a combined map.")
