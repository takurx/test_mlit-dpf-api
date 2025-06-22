import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd
import requests
from datetime import datetime
import os

# Set page title
st.set_page_config(page_title="Geographic Data Visualization", layout="wide")

# Title and introduction
st.title("Geographic Data Visualization")
st.markdown("This app visualizes the geographic points from both the MLIT API and kyon sightings API.")

# Function to fetch data from MLIT API
def fetch_mlit_data(keyword, lat, lon, range_val, api_key):
    """Fetch data from the MLIT API and return the response"""
    # GraphQLクエリー内容を作成
    top = lat + range_val
    bottom = lat - range_val
    left = lon - range_val
    right = lon + range_val
    graph_ql_query = """
    query {
      search(
        term: "%s",
        first: 0,
        size: 10,
        locationFilter: {
          rectangle: {
            topLeft: {
              lat: %f,
              lon: %f
            },
            bottomRight: {
              lat: %f,
              lon: %f
            }
          }
        }
      ) {
        totalNumber
        searchResults {
          title
          lat
          lon
        }
      }
    }
    """ % (keyword, top, left, bottom, right)

    # APIを呼び出して結果を準備する。
    end_point = "https://www.mlit-data.jp/api/v1/"
    response = requests.post(
        end_point,
        headers={
            "Content-type": "application/json",
            "apikey": api_key,
        },
        json={"query": graph_ql_query})
    
    return response.json()

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
tab1, tab2, tab3 = st.tabs(["MLIT API Data", "kyon API Data", "Combined Map"])

# Path to save or load the MLIT data
data_file = "api_results.json"

# Tab 1: MLIT API Data
with tab1:
    st.subheader("MLIT API Data Search")
    
    # Input form for API parameters
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keyword = st.text_input("Keyword", value="つくば")
            api_key = st.text_input("API Key (optional)", type="password", 
                                  help="If left blank, it will try to use saved data")
        
        with col2:
            lat = st.number_input("Latitude", value=36.10, format="%.8f")
            lon = st.number_input("Longitude", value=140.10, format="%.8f")
            range_val = st.number_input("Range (in degrees)", value=0.5, format="%.2f")
        
        submitted = st.form_submit_button("Search and Visualize")
    
    # Variables to hold the data and status
    mlit_data = None
    using_saved_data = False
    
    # If form is submitted and API key is provided, fetch new data
    if submitted and api_key:
        with st.spinner("Fetching data from MLIT API..."):
            try:
                mlit_data = fetch_mlit_data(keyword, lat, lon, range_val, api_key)
                # Save the data
                with open(data_file, "w") as f:
                    json.dump(mlit_data, f)
                st.success("Data successfully fetched and saved!")
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
    # Otherwise try to load saved data
    elif os.path.exists(data_file):
        with st.spinner("Loading saved data..."):
            try:
                with open(data_file, "r") as f:
                    mlit_data = json.load(f)
                using_saved_data = True
                st.info("Using saved data. Submit with API key to fetch new data.")
            except Exception as e:
                st.error(f"Error loading saved data: {str(e)}")
    
    # Extract locations from MLIT data
    locations = []
    if mlit_data and "data" in mlit_data and "search" in mlit_data["data"] and "searchResults" in mlit_data["data"]["search"]:
        for result in mlit_data["data"]["search"]["searchResults"]:
            if "title" in result and "lat" in result and "lon" in result:
                locations.append({
                    "title": result["title"],
                    "lat": result["lat"],
                    "lon": result["lon"]
                })
    
    # Create a DataFrame from the locations
    if locations:
        df_mlit = pd.DataFrame(locations)
        
        # Display total number of results
        total_number = mlit_data["data"]["search"]["totalNumber"]
        st.subheader(f"Found {total_number} total results, showing {len(locations)} points")
        
        # Display data table
        st.subheader("MLIT Data Table")
        st.dataframe(df_mlit)
        
        # Create the map
        st.subheader("MLIT Data Map Visualization")
        
        # Create a map centered around the mean latitude and longitude
        center_lat = df_mlit["lat"].mean()
        center_lon = df_mlit["lon"].mean()
        
        m_mlit = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add points to the map
        for _, row in df_mlit.iterrows():
            popup_text = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=row['title'],
                icon=folium.Icon(icon="info-sign", prefix="fa", color="blue")
            ).add_to(m_mlit)
        
        # Display the map
        folium_static(m_mlit, height=600)
    elif not submitted:
        st.info("Fill in the form and click 'Search and Visualize' to retrieve and display data.")
    else:
        st.error("No valid location data found in the MLIT API response.")

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
    has_mlit_data = 'df_mlit' in locals() and not df_mlit.empty
    has_kyon_data = 'df_kyon' in locals() and not df_kyon.empty
    
    if has_mlit_data or has_kyon_data:
        st.subheader("Combined Map Visualization")
        
        # Determine center coordinates based on available data
        if has_mlit_data and has_kyon_data:
            # Use the average of both datasets
            all_lats = pd.concat([df_mlit["lat"], df_kyon["lat"]])
            all_lons = pd.concat([df_mlit["lon"], df_kyon["lon"]])
            center_lat = all_lats.mean()
            center_lon = all_lons.mean()
        elif has_mlit_data:
            center_lat = df_mlit["lat"].mean()
            center_lon = df_mlit["lon"].mean()
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
        
        # Add MLIT data points to the map if available
        if has_mlit_data:
            for _, row in df_mlit.iterrows():
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
            <p><i class="fa fa-info-sign fa-2x" style="color:blue"></i> MLIT API Data</p>
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
