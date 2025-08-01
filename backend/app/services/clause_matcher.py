from typing import List, Tuple
from .embedder import VectorIndex

def retrieve(index: VectorIndex, chunks: List[str], metadata: List[dict], query: str, k: int = 5) -> List[dict]:
    """Retrieve relevant chunks using TF-IDF similarity"""
    scores, indices = index.search(query, k)
    
    results = []
    for idx, score in zip(indices, scores):
        if idx < len(chunks):
            results.append({
                "clause_id": metadata[idx]["chunk_id"],
                "text": chunks[idx],
                "similarity_score": float(score),
                "source": metadata[idx]["file_path"],
                "section": None  # Add section extraction logic if needed
            })
    
    return results