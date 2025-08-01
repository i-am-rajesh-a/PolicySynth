import requests
import json
import time

def test_backend_integration():
    """Test the backend API endpoints for frontend integration"""
    base_url = "http://127.0.0.1:8000/"
    
    print("🧪 Testing Backend Integration...")
    
    try:
        # Test 1: Health check
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data.get('message', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
        
        # Test 3: API documentation
        print("\n3. Testing API documentation...")
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API documentation failed: {response.status_code}")
        
        # Test 4: Upload endpoint (without file)
        print("\n4. Testing upload endpoint structure...")
        response = requests.post(f"{base_url}/api/v1/upload/")
        if response.status_code == 422:  # Expected: validation error for missing file
            print("✅ Upload endpoint structure correct")
        else:
            print(f"⚠️ Upload endpoint returned: {response.status_code}")
        
        # Test 5: Ask endpoint (without document)
        print("\n5. Testing ask endpoint structure...")
        response = requests.post(
            f"{base_url}/api/v1/ask/",
            json={"question": "test question"}
        )
        if response.status_code == 400:  # Expected: no document uploaded
            print("✅ Ask endpoint structure correct")
        else:
            print(f"⚠️ Ask endpoint returned: {response.status_code}")
        
        print("\n🎉 Backend integration tests completed!")
        print("\n📋 Next steps:")
        print("1. Start the frontend: cd frontend && npm run dev")
        print("2. Open http://localhost:5173 in your browser")
        print("3. Upload a document and test the analysis")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server")
        print("Make sure the backend is running: python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    test_backend_integration() 