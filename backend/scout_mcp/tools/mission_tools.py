from app.services import mission_service
from scout_mcp.registry import tool


@tool()
def get_mission(team: str):
    """
    Description:
    Get the latest mission for a team.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "mission_id": "...",
        "team": "...",
        "status": "..."
      },
      "metadata": {
        "tool": "get_mission",
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
    return mission_service.get_mission(team)


@tool()
def get_mission_history(team: str, size: int = 20):
    """
    Description:
    Get recent mission history for a team.

    Input Schema:
    {
      "team": "Egypt",
      "size": 20
    }

    Output Schema:
    {
      "success": true,
      "data": [
        {
          "mission_id": "...",
          "team": "...",
          "status": "..."
        }
      ],
      "metadata": {
        "tool": "get_mission_history",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "team": "Egypt",
      "size": 20
    }
    """
    return mission_service.get_history(team, size=size)
