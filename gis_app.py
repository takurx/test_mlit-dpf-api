import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import pandas as pd
import os
import requests

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
    st.set_page_config(page_title="GIS Data Visualization", layout="wide")
    
    st.title("GIS Data Visualization")
    st.markdown("This app allows you to visualize geographic data from either the MLIT API or a JSON file.")
    
    # Create tabs for different data input methods
    tab1, tab2 = st.tabs(["Use API", "Upload JSON"])
    
    with tab1:
        st.header("Fetch Data from MLIT API")
        
        # Input form for API parameters
        with st.form("search_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                keyword = st.text_input("Keyword", value="つくば")
                api_key = st.text_input("API Key", type="password", 
                                        help="Enter your MLIT API key")
            
            with col2:
                lat = st.number_input("Latitude", value=35.69394069179055, format="%.8f")
                lon = st.number_input("Longitude", value=139.75364318486396, format="%.8f")
                range_val = st.number_input("Range (in degrees)", value=1.0, format="%.2f")
            
            submitted = st.form_submit_button("Search and Visualize")
        
        # If form is submitted and API key is provided, fetch new data
        if submitted and api_key:
            with st.spinner("Fetching data from API..."):
                try:
                    data = fetch_data(keyword, lat, lon, range_val, api_key)
                    # Save the data
                    with open("api_results.json", "w") as f:
                        json.dump(data, f)
                    st.success("Data successfully fetched!")
                    
                    # Visualize the data
                    visualize_data(data)
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
    
    with tab2:
        st.header("Upload JSON File")
        
        # File uploader for JSON data
        uploaded_file = st.file_uploader("Choose a JSON file", type="json")
        
        # If a file is uploaded, process it
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                # Visualize the data
                visualize_data(data)
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        
        # Option to use example data
        st.markdown("---")
        if st.button("Use Example Data"):
            example_file = "test_simple_search-2_result-1.json"
            if os.path.exists(example_file):
                with open(example_file, "r") as f:
                    data = json.load(f)
                # Visualize the data
                visualize_data(data)
            else:
                st.warning(f"Example file '{example_file}' not found.")

def visualize_data(data):
    """Visualize the data on a map and in a table"""
    # Extract locations from JSON
    locations = []
    if "data" in data and "search" in data["data"] and "searchResults" in data["data"]["search"]:
        total_number = data["data"]["search"]["totalNumber"]
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
            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
            
            # Add the points to the map
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
            st.warning("No location data found in the data.")
    else:
        st.error("Invalid data format: Could not find expected fields in the data.")

if __name__ == "__main__":
    main()
