import sys
from app.mcp.tools.mission_tools import get_latest_mission as tool_get_latest_mission
from app.mcp.tools.city_tools import search_cities as tool_search_cities
from app.mcp.tools.stadium_tools import search_stadiums as tool_search_stadiums
from app.mcp.tools.budget_tools import get_budget_status as tool_get_budget_status
from app.mcp.tools.preference_tools import get_preferences as tool_get_preferences
from app.mcp.tools.retrieval_tools import (
    retrieve_city_candidates as tool_retrieve_city_candidates,
    retrieve_stadium_candidates as tool_retrieve_stadium_candidates,
    retrieve_route_candidates as tool_retrieve_route_candidates
)
from app.mcp.tools.recommendation_tools import get_replanning_recommendation as tool_get_replanning_recommendation

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("Scout")
except ImportError:
    mcp = None

# Fallback python registry
fallback_registry = {}


def tool(name=None):
    """
    Decorator to register a tool with both the fallback registry and FastMCP.
    """
    def decorator(func):
        reg_name = name or func.__name__
        fallback_registry[reg_name] = func
        if mcp is not None:
            mcp.tool(name=reg_name)(func)
        return func
    return decorator


@tool(name="get_latest_mission")
def get_latest_mission(team: str):
    """Retrieves the latest mission document for a given team name."""
    return tool_get_latest_mission(team)


@tool(name="search_cities")
def search_cities(query: str, size: int = 10):
    """Searches the cities index using a query string."""
    return tool_search_cities(query, size=size)


@tool(name="search_stadiums")
def search_stadiums(query: str, size: int = 10):
    """Searches the stadiums index using a query string."""
    return tool_search_stadiums(query, size=size)


@tool(name="get_budget_status")
def get_budget_status(team: str):
    """Retrieves the current budget status and risk level for a team."""
    return tool_get_budget_status(team)


@tool(name="get_preferences")
def get_preferences(mission_id: str):
    """Retrieves the fan preferences (weights) for a mission."""
    return tool_get_preferences(mission_id)


@tool(name="retrieve_city_candidates")
def retrieve_city_candidates(query: str, size: int = 5):
    """Retrieves semantically matched city candidates for a query."""
    return tool_retrieve_city_candidates(query, size=size)


@tool(name="retrieve_stadium_candidates")
def retrieve_stadium_candidates(query: str, size: int = 5):
    """Retrieves semantically matched stadium candidates for a query."""
    return tool_retrieve_stadium_candidates(query, size=size)


@tool(name="retrieve_route_candidates")
def retrieve_route_candidates(size: int = 10):
    """Retrieves alternative route candidates up to a given size."""
    return tool_retrieve_route_candidates(size=size)


@tool(name="get_replanning_recommendation")
def get_replanning_recommendation(team: str):
    """Runs adaptive replanning for a team's latest mission and returns recommendation and reasoning."""
    return tool_get_replanning_recommendation(team=team)


def list_tools():
    """
    Returns a dict containing the list of registered tools with metadata.
    """
    tools_list = []
    for name, func in fallback_registry.items():
        tools_list.append({
            "name": name,
            "description": func.__doc__ or "No description",
            "parameters": list(func.__code__.co_varnames[:func.__code__.co_argcount])
        })
    return {"tools": tools_list}


def tool_count():
    """
    Returns the total count of registered read-only MCP tools.
    """
    return len(fallback_registry)


if __name__ == "__main__":
    if mcp is not None:
        mcp.run()
    else:
        print("MCP SDK not installed. Fallback registry loaded successfully:")
        for t_name in fallback_registry:
            print(f" - {t_name}")
