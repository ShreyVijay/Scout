from app.services import city_service
from scout_mcp.registry import tool


@tool()
def search_cities(query: str, size: int = 10):
    """
    Description:
    Search host cities.

    Input Schema:
    {
      "query": "Miami",
      "size": 10
    }

    Output Schema:
    {
      "success": true,
      "data": [
        {
          "city": "...",
          "country": "..."
        }
      ],
      "metadata": {
        "tool": "search_cities",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "query": "Miami",
      "size": 10
    }
    """
    return city_service.search_cities(query, size)


@tool()
def get_city(city: str):
    """
    Description:
    Retrieve detailed intelligence for a specific host city.

    Input Schema:
    {
      "city": "Dallas"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "city": "...",
        "country": "...",
        "atmosphere_score": 0
      },
      "metadata": {
        "tool": "get_city",
        "timestamp": "...",
        "version": "v1"
      }
    }

    Example Calls:
    Input:
    {
      "city": "Dallas"
    }
    """
    return city_service.get_city(city)
