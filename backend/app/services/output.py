from typing import List, Dict
from pydantic import BaseModel

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

def generate_json(decision: Dict, retrieved_chunks: List[dict], query: str) -> QueryResult:
    evidence = [
        Evidence(
            clause_id=chunk["clause_id"],
            text=chunk["text"],
            similarity_score=chunk["similarity_score"],
            source=chunk["source"],
            section=chunk.get("section")
        ) for chunk in retrieved_chunks
    ]
    
    return QueryResult(
        query=query,
        answer=decision.get("answer", "No answer provided"),
        evidence=evidence,
        conditions=decision.get("conditions", []),
        decision_rationale=decision.get("decision_rationale", "No rationale provided"),
        confidence=decision.get("confidence", 0.9),
        status=decision.get("status", "conditional"),
        token_usage=decision.get("token_usage"),
        processing_time=decision.get("processing_time")
    )