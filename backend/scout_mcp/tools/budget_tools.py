from app.services import budget_service
from scout_mcp.registry import tool


@tool()
def get_budget(team: str):
    """
    Description:
    Get budget intelligence for a team's latest mission.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "total_budget": 0,
        "flight_cost": 0,
        "accommodation_cost": 0
      },
      "metadata": {
        "tool": "get_budget",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "team": "Egypt"
    }
    """
    return budget_service.get_budget(team)
