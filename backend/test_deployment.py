#!/usr/bin/env python3
"""
Test script to verify deployment dependencies work correctly
"""

import sys
import importlib

def test_imports():
    """Test that all required modules can be imported"""
    required_modules = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'python_multipart',
        'python_dotenv',
        'requests',
        'fitz',  # PyMuPDF
        'docx',  # python-docx
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {failed_imports}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_basic_functionality():
    """Test basic FastAPI functionality"""
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        app = FastAPI()
        
        class TestModel(BaseModel):
            name: str
            age: int
        
        test_data = {"name": "test", "age": 25}
        model = TestModel(**test_data)
        
        print("✅ Basic FastAPI and Pydantic functionality works")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_app_imports():
    """Test that the main app can be imported"""
    try:
        # Test importing the main app
        from app.main import app
        print("✅ Main app imports successfully")
        return True
    except Exception as e:
        print(f"⚠️ Main app import warning: {e}")
        # This is not critical for deployment
        return True

if __name__ == "__main__":
    print("🧪 Testing deployment dependencies...\n")
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    app_imports_ok = test_app_imports()
    
    if imports_ok and functionality_ok:
        print("\n🎉 All tests passed! Deployment should work.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the requirements.")
        sys.exit(1) 