from app.services import tournament_service
from scout_mcp.registry import tool


@tool()
def get_team_status(team: str):
    """
    Description:
    Get the current team status.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "team": "...",
        "status": "..."
      },
      "metadata": {
        "tool": "get_team_status",
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
    return tournament_service.get_team_status(team)


@tool()
def get_tournament_state(team: str):
    """
    Description:
    Get tournament and mission state for a team.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "team": "...",
        "status": "..."
      },
      "metadata": {
        "tool": "get_tournament_state",
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
    return tournament_service.get_tournament_state(team)
