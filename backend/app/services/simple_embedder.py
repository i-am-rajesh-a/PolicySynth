"""
Simplified embedder service for initial testing without FAISS
"""
import numpy as np
from typing import List, Dict, Any

class SimpleEmbedder:
    """Simple embedder that creates basic embeddings without FAISS"""
    
    def __init__(self):
        self.embeddings = []
        self.chunks = []
        self.metadata = []
    
    def build_index(self, chunks: List[Any], metadata: List[Dict[str, Any]] = None) -> None:
        """Build a simple index from chunks"""
        self.chunks = chunks
        self.metadata = metadata or []
        
        # Create simple embeddings (just for testing)
        self.embeddings = []
        for i, chunk in enumerate(chunks):
            # Handle both string and dict formats
            if isinstance(chunk, str):
                text = chunk
            else:
                text = chunk.get('text', '')
            embedding = self._simple_embed(text)
            self.embeddings.append(embedding)
    
    def _simple_embed(self, text: str) -> np.ndarray:
        """Create a simple embedding for testing"""
        # Simple hash-based embedding (not for production)
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to numpy array
        embedding = np.frombuffer(hash_bytes, dtype=np.float32)
        # Pad or truncate to 128 dimensions
        if len(embedding) < 128:
            embedding = np.pad(embedding, (0, 128 - len(embedding)), 'constant')
        else:
            embedding = embedding[:128]
        
        return embedding
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve similar chunks based on query"""
        if not self.embeddings or not self.chunks:
            return []
        
        # Create query embedding
        query_embedding = self._simple_embed(query)
        
        # Calculate similarities
        similarities = []
        for i, embedding in enumerate(self.embeddings):
            # Avoid division by zero
            query_norm = np.linalg.norm(query_embedding)
            embedding_norm = np.linalg.norm(embedding)
            
            if query_norm > 0 and embedding_norm > 0:
                similarity = np.dot(query_embedding, embedding) / (query_norm * embedding_norm)
                # Handle NaN values
                if np.isnan(similarity):
                    similarity = 0.0
            else:
                similarity = 0.0
                
            similarities.append((similarity, i))
        
        # Sort by similarity
        similarities.sort(reverse=True)
        
        # Return top_k results
        results = []
        for similarity, idx in similarities[:top_k]:
            # Ensure similarity is a valid float
            if np.isnan(similarity) or np.isinf(similarity):
                similarity = 0.0
            
            chunk = self.chunks[idx]
            if isinstance(chunk, str):
                result = {
                    'text': chunk,
                    'similarity_score': float(similarity),
                    'clause_id': f"chunk_{idx}",
                    'source': 'document'
                }
            else:
                result = chunk.copy()
                result['similarity_score'] = float(similarity)
                result['clause_id'] = f"chunk_{idx}"
                result['source'] = chunk.get('source', 'document')
            results.append(result)
        
        return results

def build_index(chunks: List[Any], metadata: List[Dict[str, Any]] = None):
    """Build index function for compatibility"""
    embedder = SimpleEmbedder()
    embedder.build_index(chunks, metadata)
    return embedder

def retrieve(index, chunks: List[Any], metadata: List[Dict[str, Any]], query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve function for compatibility"""
    if hasattr(index, 'retrieve'):
        return index.retrieve(query, top_k)
    else:
        # Fallback to simple text matching
        results = []
        query_lower = query.lower()
        
        for i, chunk in enumerate(chunks):
            if isinstance(chunk, str):
                text = chunk.lower()
            else:
                text = chunk.get('text', '').lower()
            
            if any(word in text for word in query_lower.split()):
                if isinstance(chunk, str):
                    result = {
                        'text': chunk,
                        'similarity_score': 0.8,  # Mock similarity
                        'clause_id': f"chunk_{i}",
                        'source': 'document'
                    }
                else:
                    result = chunk.copy()
                    result['similarity_score'] = 0.8  # Mock similarity
                    result['clause_id'] = f"chunk_{i}"
                    result['source'] = chunk.get('source', 'document')
                results.append(result)
        
        return results[:top_k] 