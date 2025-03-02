import folium
import requests
import webbrowser
import os
import sys
from datetime import datetime

def create_kyun_map(api_url="http://localhost:5000"):
    """Create an interactive map with Kyun sighting locations"""
    try:
        # Fetch Kyun sighting coordinates from the API
        response = requests.get(f"{api_url}/api/kyun/coordinates")
        response.raise_for_status()
        data = response.json()
        
        if data["count"] == 0:
            print("No Kyun sighting data available.")
            return None
        
        # Calculate the center of the map (average of all points)
        latitudes = [item["latitude"] for item in data["data"]]
        longitudes = [item["longitude"] for item in data["data"]]
        center_lat = sum(latitudes) / len(latitudes)
        center_lng = sum(longitudes) / len(longitudes)
        
        # Create a map centered on the average position of all sightings
        m = folium.Map(location=[center_lat, center_lng], zoom_start=13)
        
        # Add a title to the map
        title_html = '''
        <h3 align="center" style="font-size:16px"><b>つくば市内キョン目撃情報マップ</b></h3>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add markers for each sighting
        for item in data["data"]:
            popup_text = f"""
            <b>{item['name']}</b><br>
            {item['description']}<br>
            緯度: {item['latitude']}<br>
            経度: {item['longitude']}
            """
            
            folium.Marker(
                location=[item['latitude'], item['longitude']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=item['name'],
                icon=folium.Icon(icon="deer", prefix="fa", color="orange")
            ).add_to(m)
        
        # Save the map to an HTML file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"kyun_map_{timestamp}.html"
        m.save(output_file)
        
        print(f"Map saved to {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Error creating map: {str(e)}")
        return None

def open_map(map_file):
    """Open the generated map in the default web browser"""
    if map_file and os.path.exists(map_file):
        try:
            # Convert to absolute path
            abs_path = os.path.abspath(map_file)
            # Open in default browser
            webbrowser.open(f"file://{abs_path}")
            print(f"Opening map in browser: {abs_path}")
        except Exception as e:
            print(f"Error opening map in browser: {str(e)}")
    else:
        print("Map file not found or not created.")

if __name__ == "__main__":
    # Use custom base URL if provided as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print("🦌 Kyun Sightings Map Generator 🦌")
    print("=" * 40)
    print(f"Using API at: {base_url}")
    
    # Create and open the map
    map_file = create_kyun_map(base_url)
    if map_file:
        print("\nWould you like to open the map in your browser? (y/n)")
        response = input().strip().lower()
        if response == 'y':
            open_map(map_file)
    
    print("\nYou can manually open the map file in your web browser.")
    print("=" * 40)
