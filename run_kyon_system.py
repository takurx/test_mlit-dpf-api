#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import signal
import webbrowser

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import requests
        import folium
        print("✅ All required dependencies are installed.")
        return True
    except ImportError as e:
        missing_package = str(e).split("'")[1]
        print(f"❌ Missing dependency: {missing_package}")
        print("\nPlease install required packages:")
        print("pip install flask requests folium")
        return False

def main():
    """Run the complete kyon sighting information system"""
    if not check_dependencies():
        return
    
    print_header("つくばキョン目撃情報システム (Tsukuba kyon Sighting System)")
    
    # Start the API server as a background process
    print("\n🚀 Starting the API server...")
    api_process = subprocess.Popen(
        [sys.executable, "kyon_api_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start (give it a few seconds)
    print("⏳ Waiting for server to initialize...")
    time.sleep(3)
    
    # Check if server is running
    if api_process.poll() is not None:
        print("❌ API server failed to start!")
        out, err = api_process.communicate()
        print(f"Error: {err}")
        return
    
    try:
        print("✅ API server running!")
        
        # Run the demo script
        print("\n📊 Running API demo...")
        subprocess.run([sys.executable, "kyon_api_demo.py"], check=True)
        
        # Generate the map
        print("\n🗺️ Generating map visualization...")
        subprocess.run([sys.executable, "kyon_map_visualizer.py"], check=True)
        
        # Provide instructions
        print_header("システムが正常に動作しています (System is running normally)")
        print("\nAPI Server is running at: http://localhost:5000")
        print("\nAvailable endpoints:")
        print("  - http://localhost:5000/api/kyon/sightings")
        print("  - http://localhost:5000/api/kyon/coordinates")
        print("  - http://localhost:5000/api/kyon/sightings/<location_name>")
        
        print("\nPress Ctrl+C to stop the system when finished.")
        
        # Keep the server running until user interrupts
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down system...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        # Terminate the API server process
        if api_process.poll() is None:
            print("🛑 Stopping API server...")
            # Send SIGTERM, which allows for graceful shutdown
            if os.name == 'nt':  # Windows
                api_process.terminate()
            else:  # Unix/Linux/MacOS
                os.kill(api_process.pid, signal.SIGTERM)
            api_process.wait(timeout=5)
        
        print("\n✨ System shutdown complete. Thank you for using the kyon Sighting System!")

if __name__ == "__main__":
    main()
