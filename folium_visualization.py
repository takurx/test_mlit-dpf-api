import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd
import os

def main():
    st.set_page_config(page_title="Geographic Data Visualization", layout="wide")
    
    st.title("Geographic Data Visualization")
    st.markdown("This app visualizes the geographic points from the JSON data.")

    # Function to load JSON data
    @st.cache_data
    def load_data(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    # Load the JSON data
    data_file = "test_simple_search-2_result-1.json"
    if os.path.exists(data_file):
        data = load_data(data_file)
        
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
            
            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
            
            # Add points to the map
            for _, row in df.iterrows():
                popup_text = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['title']
                ).add_to(m)
            
            # Display the map
            folium_static(m, width=1000, height=600)
        else:
            st.error("No valid location data found in the JSON file.")
    else:
        st.error(f"File not found: {data_file}")

if __name__ == "__main__":
    main()
