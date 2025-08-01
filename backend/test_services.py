#!/usr/bin/env python3
"""
Test script for backend services without FAISS
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_services():
    """Test the backend services"""
    print("🧪 Testing Backend Services...")
    
    try:
        # Test 1: Import services
        print("\n1. Testing imports...")
        from app.services.parser import parse_files
        from app.services.chunker import adaptive_chunk
        from app.services.simple_embedder import build_index, retrieve
        from app.services.simple_logic import evaluate
        from app.services.output import generate_json
        print("✅ All service imports successful")
        
        # Test 2: Create mock data with correct structure
        print("\n2. Testing with mock data...")
        mock_text = """
        This is a sample policy document.
        Section 1: Coverage
        The policy covers medical procedures including surgery.
        Section 2: Exclusions
        Cosmetic procedures are not covered.
        Section 3: Waiting Period
        There is a 12-month waiting period for pre-existing conditions.
        """
        
        # Create the correct data structure that chunker expects
        mock_docs = [{
            "text": mock_text,
            "file_path": "test_document.txt"
        }]
        
        # Test chunking
        chunks, metadata = adaptive_chunk(mock_docs)
        print(f"✅ Chunking successful: {len(chunks)} chunks created")
        
        # Convert chunks to the format expected by the embedder
        chunk_dicts = []
        for i, chunk in enumerate(chunks):
            chunk_dicts.append({
                "text": chunk,
                "source": "test_document.txt",
                "chunk_id": f"chunk_{i}"
            })
        
        # Test embedding
        index = build_index(chunk_dicts, metadata)
        print("✅ Index building successful")
        
        # Test retrieval
        query = "What is covered under this policy?"
        results = retrieve(index, chunk_dicts, metadata, query)
        print(f"✅ Retrieval successful: {len(results)} results found")
        
        # Test evaluation
        decision = evaluate(query, results)
        print("✅ Evaluation successful")
        
        # Test output generation
        result = generate_json(decision, results, query)
        print("✅ Output generation successful")
        
        print("\n🎉 All backend services are working!")
        print("\n📋 You can now:")
        print("1. Start the backend server")
        print("2. Test with the frontend")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required dependencies")
        return False
    except Exception as e:
        print(f"❌ Service error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_services() 