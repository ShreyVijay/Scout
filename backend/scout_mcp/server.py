from mcp.server.fastmcp import FastMCP

from scout_mcp.registry import register_tools
from scout_mcp.tools import (
    budget_tools,
    city_tools,
    mission_tools,
    preference_tools,
    recommendation_tools,
    stadium_tools,
    tournament_tools,
)


mcp = FastMCP("Scout")
register_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="sse")
