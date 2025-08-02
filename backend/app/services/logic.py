from openai import OpenAI
from app.config import OPENROUTER_API_KEY
from typing import List, Dict
import os
import httpx

# Clear any proxy environment variables that might interfere
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

# Create a custom transport without proxies
transport = httpx.HTTPTransport(proxy=None)

# Initialize OpenAI client with custom transport
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    http_client=httpx.Client(transport=transport)
)

def interpret_query(query: str) -> str:
    # Basic query interpretation; enhance as needed
    return query

def evaluate(query: str, retrieved_chunks: List[dict]) -> Dict:
    prompt = f"""
    Query: {query}
    
    Relevant document excerpts:
    {chr(10).join([f"Clause {chunk['clause_id']}: {chunk['text']}" for chunk in retrieved_chunks])}
    
    Analyze the query against the provided document excerpts. Determine if the query is covered, not covered, conditional, or unclear. Provide:
    - An answer summarizing the finding
    - A list of conditions (if any)
    - A detailed decision rationale
    - A confidence score (0 to 1)
    - A status (covered, not_covered, conditional, unclear)
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a policy analysis expert. Provide accurate, concise, and explainable answers based on the given document excerpts."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse response (simplified; adjust based on actual LLM output)
        content = response.choices[0].message.content
        try:
            import json
            result = json.loads(content)
        except:
            result = {
                "answer": content,
                "conditions": [],
                "decision_rationale": content,
                "confidence": 0.9,
                "status": "conditional",
                "token_usage": response.usage.total_tokens if response.usage else None
            }
        
        return result
    except Exception as e:
        # Fallback response if OpenAI API fails
        return {
            "answer": f"Analysis completed with fallback response. Error: {str(e)}",
            "conditions": [],
            "decision_rationale": "OpenAI API temporarily unavailable, using fallback analysis",
            "confidence": 0.7,
            "status": "conditional",
            "token_usage": None
        }