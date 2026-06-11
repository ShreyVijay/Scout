import os


def tool_timeout_seconds() -> float:
    return float(os.getenv("MCP_TOOL_TIMEOUT_SECONDS", "30"))
