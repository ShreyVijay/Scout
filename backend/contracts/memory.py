from contracts.base import ScoutDTO


class AgentMemory(ScoutDTO):
    memory_type: str
    mission_id: str
    summary: str
    timestamp: str
