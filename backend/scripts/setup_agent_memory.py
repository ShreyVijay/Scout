import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp.elastic_client import get_elastic_client
from datetime import datetime

def setup_agent_memory():
    es = get_elastic_client()
    index_name = "agent_memory"
    
    # Check if index exists
    if not es.indices.exists(index=index_name):
        print(f"Index '{index_name}' does not exist. Creating...")
        mapping = {
            "mappings": {
                "properties": {
                    "memory_type": {"type": "keyword"},
                    "mission_id": {"type": "keyword"},
                    "summary": {"type": "text"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        es.indices.create(index=index_name, body=mapping)
        print("Index created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")
        
    # Insert test records
    print("Inserting test records...")
    records = [
        {
            "memory_type": "recommendation_summary",
            "mission_id": "m-test",
            "summary": "Recommended Dallas based on high atmosphere score and budget efficiency.",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "memory_type": "mission_summary",
            "mission_id": "m-test",
            "summary": "Team is currently in planning phase. Budget constraints applied.",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "memory_type": "reasoning_summary",
            "mission_id": "m-test",
            "summary": "Decision primarily driven by a 1.2x multiplier from semantic matching.",
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
    
    for record in records:
        es.index(index=index_name, document=record)
        
    es.indices.refresh(index=index_name)
    print("Records inserted successfully.")
    
    # Verify retrieval
    print("\nVerifying retrieval...")
    res = es.search(index=index_name, body={"query": {"match_all": {}}})
    hits = res["hits"]["hits"]
    print(f"Retrieved {len(hits)} records:")
    for hit in hits:
        print(f" - [{hit['_source']['memory_type']}] {hit['_source']['summary']}")
        
if __name__ == "__main__":
    try:
        setup_agent_memory()
    except Exception as e:
        print(f"Failed to setup agent memory: {e}")
