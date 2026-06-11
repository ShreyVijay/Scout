from app.services import stadium_service
from scout_mcp.registry import tool


@tool()
def search_stadiums(query: str, size: int = 10):
    """
    Description:
    Search tournament stadiums.

    Input Schema:
    {
      "query": "MetLife",
      "size": 10
    }

    Output Schema:
    {
      "success": true,
      "data": [
        {
          "stadium": "...",
          "city": "..."
        }
      ],
      "metadata": {
        "tool": "search_stadiums",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "query": "MetLife",
      "size": 10
    }
    """
    return stadium_service.search_stadiums(query, size)


@tool()
def get_stadium(stadium: str):
    """
    Description:
    Get one tournament stadium.

    Input Schema:
    {
      "stadium": "MetLife Stadium"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "stadium": "...",
        "city": "...",
        "capacity": 0
      },
      "metadata": {
        "tool": "get_stadium",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "stadium": "MetLife Stadium"
    }
    """
    return stadium_service.get_stadium(stadium)
