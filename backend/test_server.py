import requests
import json

def test_server():
    """Test the backend server endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        # Test docs endpoint
        response = requests.get(f"{base_url}/docs")
        print(f"Docs endpoint: {response.status_code}")
        
        print("✅ Server is running successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000.")
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    test_server() 