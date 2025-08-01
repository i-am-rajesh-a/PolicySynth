import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorIndex:
    def __init__(self, chunks=None):
        self.chunks = chunks if chunks else []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.embeddings = None
        
    def build_index(self, chunks):
        """Build TF-IDF index from chunks"""
        self.chunks = chunks
        if chunks:
            self.embeddings = self.vectorizer.fit_transform(chunks)
    
    def search(self, query, k=5):
        """Search for similar chunks"""
        if not self.embeddings or not self.chunks:
            return [], []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.embeddings).flatten()
        
        # Get top k results
        indices = np.argsort(similarities)[::-1][:k]
        scores = similarities[indices]
        
        return scores, indices

def build_index(chunks: list[str]) -> VectorIndex:
    """Build vector index from chunks"""
    index = VectorIndex()
    index.build_index(chunks)
    return index