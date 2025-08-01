from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Policy Pundit API", description="AI-powered policy analysis and document processing API")

# Updated CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080", 
        "http://localhost:5173", 
        "http://127.0.0.1:8080",
        "https://policysynth.onrender.com",  # Render backend domain
        "https://your-frontend-domain.com",   # Replace with your frontend domain
        "http://localhost:3000",             # Common frontend dev port
        "*"  # Allow all origins for testing
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Policy Pundit API is running!",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify the API is working"""
    return {
        "message": "API is working!",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Import routers conditionally to avoid startup errors
try:
    from app.routers import document
    app.include_router(document.router, prefix="/api/v1")
    print("✅ Document router loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not import document router: {e}")
except Exception as e:
    print(f"⚠️ Warning: Error loading document router: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)