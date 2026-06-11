from app.mcp.elastic_client import get_elastic_client


INDEX_NAME = "agent_memory"


def create_index() -> None:
    es = get_elastic_client()
    if es.indices.exists(index=INDEX_NAME):
        return
    es.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "memory_type": {"type": "keyword"},
                "mission_id": {"type": "keyword"},
                "summary": {"type": "text"},
                "timestamp": {"type": "date"},
            }
        },
    )


if __name__ == "__main__":
    create_index()
