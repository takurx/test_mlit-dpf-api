import csv
import json
import re
from flask import Flask, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def parse_wkt_point(wkt):
    """Parse WKT POINT format and return longitude and latitude"""
    match = re.search(r'POINT \(([0-9.]+) ([0-9.]+)\)', wkt)
    if match:
        return {
            "longitude": float(match.group(1)),
            "latitude": float(match.group(2))
        }
    return None

def load_kyon_data():
    """Load kyon sighting data from CSV and convert to JSON format"""
    data = []
    
    try:
        with open('つくばのキョン目撃情報- 市内での目撃事例.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header row
            
            for row in reader:
                if len(row) >= 3:
                    wkt, name, description = row[0], row[1], row[2]
                    location = parse_wkt_point(wkt)
                    
                    if location:
                        data.append({
                            "location": {
                                "name": name,
                                "coordinates": location
                            },
                            "description": description,
                            "raw_wkt": wkt
                        })
                else:
                    logger.warning(f"Skipping malformed row: {row}")
        
        logger.info(f"Successfully loaded {len(data)} kyon sighting records")
        return data
    except Exception as e:
        logger.error(f"Error loading CSV data: {str(e)}")
        return []

# Global variable to store the data
kyon_DATA = load_kyon_data()

@app.route('/api/kyon/sightings', methods=['GET'])
def get_all_sightings():
    """Return all kyon sighting data"""
    return jsonify({
        "status": "success",
        "count": len(kyon_DATA),
        "data": kyon_DATA
    })

@app.route('/api/kyon/sightings/<location_name>', methods=['GET'])
def get_sighting_by_location(location_name):
    """Return kyon sighting data filtered by location name"""
    filtered_data = [item for item in kyon_DATA if location_name in item["location"]["name"]]
    
    return jsonify({
        "status": "success",
        "count": len(filtered_data),
        "data": filtered_data
    })

@app.route('/api/kyon/coordinates', methods=['GET'])
def get_all_coordinates():
    """Return all kyon sighting coordinates for mapping"""
    coordinates = [
        {
            "name": item["location"]["name"],
            "longitude": item["location"]["coordinates"]["longitude"],
            "latitude": item["location"]["coordinates"]["latitude"],
            "description": item["description"]
        }
        for item in kyon_DATA
    ]
    
    return jsonify({
        "status": "success",
        "count": len(coordinates),
        "data": coordinates
    })

if __name__ == '__main__':
    logger.info("Starting kyon Sightings API Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
