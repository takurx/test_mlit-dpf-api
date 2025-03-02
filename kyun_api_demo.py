import requests
import json
import sys

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_api(base_url="http://localhost:5000"):
    """Test the Kyun sightings API endpoints"""
    
    print("🦌 Kyun Sightings API Test 🦌")
    print("=" * 40)
    
    # Test 1: Get all sightings
    print("\n📊 Testing GET all sightings...")
    try:
        response = requests.get(f"{base_url}/api/kyun/sightings")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success! Found {data['count']} sightings")
        print("First sighting preview:")
        if data['count'] > 0:
            print_json(data['data'][0])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Get coordinates for mapping
    print("\n🗺️ Testing GET coordinates for mapping...")
    try:
        response = requests.get(f"{base_url}/api/kyun/coordinates")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success! Found {data['count']} coordinate entries")
        print("Sample coordinates:")
        if data['count'] > 0:
            print_json(data['data'][0])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Get sightings by location
    location = "みどりの東"
    print(f"\n🔍 Testing GET sightings by location: '{location}'...")
    try:
        response = requests.get(f"{base_url}/api/kyun/sightings/{location}")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Success! Found {data['count']} sightings for '{location}'")
        if data['count'] > 0:
            print_json(data['data'])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 40)
    print("API test completed!")

if __name__ == "__main__":
    # Use custom base URL if provided as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    test_api(base_url)
