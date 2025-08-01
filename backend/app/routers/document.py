from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
import os
import numpy as np

# Import services with error handling
try:
    from app.services.parser import parse_files
    from app.services.chunker import adaptive_chunk
    from app.services.simple_embedder import build_index, retrieve
    from app.services.logic import evaluate
    from app.services.output import generate_json
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some services not available: {e}")
    SERVICES_AVAILABLE = False

router = APIRouter()

# In-memory storage for simplicity
chunks = []
metadata = []
faiss_index = None

class QueryRequest(BaseModel):
    question: str

class Evidence(BaseModel):
    clause_id: str
    text: str
    similarity_score: float
    source: str
    section: str | None = None

class QueryResult(BaseModel):
    query: str
    answer: str
    evidence: List[Evidence]
    conditions: List[str]
    decision_rationale: str
    confidence: float
    status: str
    token_usage: int | None = None
    processing_time: float | None = None

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Document processing services not available")
    
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed")
    
    upload_dir = "data/uploaded_docs/"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    global chunks, metadata, faiss_index
    try:
        extracted_text = parse_files([file_path])
        chunks, metadata = adaptive_chunk(extracted_text)
        faiss_index = build_index(chunks)
        
        return JSONResponse(content={
            "message": "Document uploaded successfully",
            "chunks_processed": len(chunks),
            "filename": file.filename
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/status/")
async def get_status():
    """Get the current status of loaded documents"""
    return JSONResponse(content={
        "documents_loaded": len(chunks) > 0,
        "chunks_count": len(chunks),
        "index_built": faiss_index is not None,
        "services_available": SERVICES_AVAILABLE
    })

@router.post("/ask/", response_model=QueryResult)
async def ask_question(request: QueryRequest):
    if not SERVICES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Document processing services not available")
    
    if not faiss_index or not chunks:
        raise HTTPException(status_code=400, detail="No document uploaded. Please upload a document first.")
    
    try:
        question = request.question
        retrieved_chunks = retrieve(faiss_index, chunks, metadata, question)
        
        # Clean any NaN values from retrieved chunks
        for chunk in retrieved_chunks:
            if 'similarity_score' in chunk:
                if np.isnan(chunk['similarity_score']) or np.isinf(chunk['similarity_score']):
                    chunk['similarity_score'] = 0.0
        
        decision = evaluate(question, retrieved_chunks)
        result = generate_json(decision, retrieved_chunks, question)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")