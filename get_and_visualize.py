import requests
import json
import streamlit as st
import leafmap.foliumap as lfmap
import pandas as pd
import os

def fetch_data(keyword, lat, lon, range_val, api_key):
    """Fetch data from the API and return the response"""
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

def main():
    st.set_page_config(page_title="GIS Data Retrieval and Visualization", layout="wide")
    
    st.title("GIS Data Retrieval and Visualization")
    st.markdown("This app retrieves geographic data using the MLIT API and visualizes it on a map.")
    
    # Input form for API parameters
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keyword = st.text_input("Keyword", value="つくば")
            api_key = st.text_input("API Key (optional)", type="password", 
                                   help="If left blank, it will try to use saved data")
        
        with col2:
            lat = st.number_input("Latitude", value=35.69394069179055, format="%.8f")
            lon = st.number_input("Longitude", value=139.75364318486396, format="%.8f")
            range_val = st.number_input("Range (in degrees)", value=1.0, format="%.2f")
        
        submitted = st.form_submit_button("Search and Visualize")
    
    # Path to save or load the data
    data_file = "search_results.json"
    
    # Variables to hold the data and status
    data = None
    using_saved_data = False
    
    # If form is submitted and API key is provided, fetch new data
    if submitted and api_key:
        with st.spinner("Fetching data from API..."):
            try:
                data = fetch_data(keyword, lat, lon, range_val, api_key)
                # Save the data
                with open(data_file, "w") as f:
                    json.dump(data, f)
                st.success("Data successfully fetched and saved!")
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
    # Otherwise try to load saved data
    elif os.path.exists(data_file):
        with st.spinner("Loading saved data..."):
            try:
                with open(data_file, "r") as f:
                    data = json.load(f)
                using_saved_data = True
                st.info("Using saved data. Submit with API key to fetch new data.")
            except Exception as e:
                st.error(f"Error loading saved data: {str(e)}")
    
    # If data is available, visualize it
    if data and "data" in data and "search" in data["data"] and "searchResults" in data["data"]["search"]:
        # Extract locations
        locations = []
        for result in data["data"]["search"]["searchResults"]:
            if "title" in result and "lat" in result and "lon" in result:
                locations.append({
                    "title": result["title"],
                    "lat": result["lat"],
                    "lon": result["lon"]
                })
        
        # If locations found, create DataFrame and visualize
        if locations:
            df = pd.DataFrame(locations)
            
            # Display total number of results
            total_number = data["data"]["search"]["totalNumber"]
            st.subheader(f"Found {total_number} total results, showing {len(locations)} points")
            
            # Display the data table
            st.subheader("Data Table")
            st.dataframe(df)
            
            # Create the map
            st.subheader("Map Visualization")
            
            # Calculate the center of the map
            center_lat = df["lat"].mean()
            center_lon = df["lon"].mean()
            
            # Create a map
            m = lfmap.Map(center=(center_lat, center_lon), zoom=9)
            
            # Add the points to the map
            for _, row in df.iterrows():
                popup = f"<b>{row['title']}</b><br>Latitude: {row['lat']}<br>Longitude: {row['lon']}"
                m.add_marker(location=(row['lat'], row['lon']), popup=popup)
            
            # Display the map
            m.to_streamlit(height=600)
        else:
            st.warning("No location data found in the API response.")
    elif not submitted:
        st.info("Fill in the form and click 'Search and Visualize' to retrieve and display data.")

if __name__ == "__main__":
    main()
