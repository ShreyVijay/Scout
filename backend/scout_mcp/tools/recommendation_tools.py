from app.services import audit_service, reasoning_service, recommendation_service
from scout_mcp.registry import tool


@tool()
def get_recommendation(team: str):
    """
    Description:
    Get Scout's recommendation for a team.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "city": "...",
        "match": "...",
        "rank": 1,
        "raw_score": 0,
        "final_score": 0,
        "score_metadata": {},
        "contributions": {},
        "provenance": {
          "candidate_source": "...",
          "retrieval_score": 0.0,
          "source_multiplier": 1.0,
          "rank": 1
        }
      },
      "metadata": {
        "tool": "get_recommendation",
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
    return recommendation_service.get_recommendation(team)


@tool()
def get_reasoning(team: str):
    """
    Description:
    Get Scout's recommendation reasoning for a team.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "decision": "...",
        "reasons": [],
        "top_factors": [],
        "contributions": {},
        "provenance": {
          "candidate_source": "...",
          "retrieval_score": 0.0,
          "source_multiplier": 1.0,
          "rank": 1
        }
      },
      "metadata": {
        "tool": "get_reasoning",
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
    return reasoning_service.get_reasoning(team)


@tool()
def get_audit(team: str):
    """
    Description:
    Get Scout's recommendation audit for a team.

    Input Schema:
    {
      "team": "Egypt"
    }

    Output Schema:
    {
      "success": true,
      "data": {
        "winner": "...",
        "audit": [],
        "factor_breakdown": {}
      },
      "metadata": {
        "tool": "get_audit",
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
    return audit_service.get_audit(team)
