from datetime import datetime, timezone

from contracts.memory import AgentMemory
from app.mcp.elastic_client import get_elastic_client


INDEX_NAME = "agent_memory"
ALLOWED_MEMORY_TYPES = {"mission_summary", "recommendation_summary", "reasoning_summary"}


def save_memory(memory_type: str, mission_id: str, summary: str) -> AgentMemory:
    if memory_type not in ALLOWED_MEMORY_TYPES:
        raise ValueError(f"Unsupported memory type: {memory_type}")

    memory = AgentMemory(
        memory_type=memory_type,
        mission_id=mission_id,
        summary=summary,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    get_elastic_client().index(index=INDEX_NAME, document=memory.model_dump(mode="json"))
    return memory


def get_memories(mission_id: str, size: int = 20) -> list[AgentMemory]:
    result = get_elastic_client().search(
        index=INDEX_NAME,
        size=size,
        query={"term": {"mission_id": mission_id}},
        sort=[{"timestamp": {"order": "desc"}}],
    )
    return [AgentMemory.model_validate(hit["_source"]) for hit in result["hits"]["hits"]]
