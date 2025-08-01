"""
Simplified logic service for testing without API dependencies
"""
from typing import List, Dict

def evaluate(query: str, retrieved_chunks: List[dict]) -> Dict:
    """Simplified evaluation function for testing"""
    
    # Simple keyword-based analysis
    query_lower = query.lower()
    chunks_text = " ".join([chunk.get('text', '') for chunk in retrieved_chunks]).lower()
    
    # Basic keyword matching
    coverage_keywords = ['cover', 'covered', 'coverage', 'include', 'included']
    exclusion_keywords = ['exclude', 'excluded', 'not covered', 'not include']
    condition_keywords = ['if', 'when', 'provided', 'subject to', 'condition']
    
    # Determine status based on keywords
    has_coverage = any(keyword in chunks_text for keyword in coverage_keywords)
    has_exclusions = any(keyword in chunks_text for keyword in exclusion_keywords)
    has_conditions = any(keyword in chunks_text for keyword in condition_keywords)
    
    # Generate response
    if has_coverage and not has_exclusions:
        status = "covered"
        answer = f"Yes, the policy covers {query.lower()}. Based on the document analysis, this is included in the coverage."
    elif has_coverage and has_exclusions:
        status = "conditional"
        answer = f"The policy may cover {query.lower()}, but there are specific conditions and exclusions that apply."
    elif has_exclusions:
        status = "not_covered"
        answer = f"No, the policy does not cover {query.lower()}. This is explicitly excluded from coverage."
    else:
        status = "unclear"
        answer = f"The coverage status for {query.lower()} is unclear based on the available information."
    
    # Generate conditions
    conditions = []
    if has_conditions:
        conditions.append("Specific conditions may apply")
    if has_coverage:
        conditions.append("Coverage is subject to policy terms")
    
    # Generate rationale
    rationale = f"Analysis of the document found {len(retrieved_chunks)} relevant sections. "
    if has_coverage:
        rationale += "The policy appears to provide coverage for this query."
    if has_conditions:
        rationale += "However, there are specific conditions that must be met."
    if has_exclusions:
        rationale += "There are also exclusions that may limit coverage."
    
    return {
        "answer": answer,
        "conditions": conditions,
        "decision_rationale": rationale,
        "confidence": 0.8 if retrieved_chunks else 0.5,
        "status": status,
        "token_usage": len(query) + sum(len(chunk.get('text', '')) for chunk in retrieved_chunks)
    } 