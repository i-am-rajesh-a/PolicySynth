from typing import List, Tuple
import re

def adaptive_chunk(texts: list[dict], max_tokens: int = 512, overlap: float = 0.15) -> Tuple[List[str], List[dict]]:
    chunks = []
    metadata = []
    
    for doc in texts:
        text = doc["text"]
        file_path = doc["file_path"]
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        current_tokens = 0
        chunk_id = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            token_count = len(para.split())
            
            if current_tokens + token_count > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk)
                    metadata.append({
                        "file_path": file_path,
                        "chunk_id": f"{file_path}_{chunk_id}",
                        "start_pos": len(text) - len(current_chunk)
                    })
                    overlap_size = int(len(current_chunk.split()) * overlap)
                    overlap_text = " ".join(current_chunk.split()[-overlap_size:])
                    current_chunk = overlap_text
                    current_tokens = len(overlap_text.split())
                    chunk_id += 1
                
                if token_count > max_tokens:
                    words = para.split()
                    while words:
                        chunk_words = words[:max_tokens]
                        chunks.append(" ".join(chunk_words))
                        metadata.append({
                            "file_path": file_path,
                            "chunk_id": f"{file_path}_{chunk_id}",
                            "start_pos": len(text) - len(current_chunk)
                        })
                        words = words[max_tokens - int(max_tokens * overlap):]
                        chunk_id += 1
                else:
                    current_chunk = para
                    current_tokens = token_count
            else:
                current_chunk += "\n\n" + para if current_chunk else para
                current_tokens += token_count
        
        if current_chunk:
            chunks.append(current_chunk)
            metadata.append({
                "file_path": file_path,
                "chunk_id": f"{file_path}_{chunk_id}",
                "start_pos": len(text) - len(current_chunk)
            })
    
    return chunks, metadata