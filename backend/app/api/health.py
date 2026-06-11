import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health():
    return {"status": "ok"}

@router.get("/mcp")
def mcp_health():
    from scout_mcp.metrics import get_tool_metrics
    from scout_mcp.registry import list_tools
    from scout_mcp.tools import (
        budget_tools,
        city_tools,
        mission_tools,
        preference_tools,
        recommendation_tools,
        stadium_tools,
        tournament_tools,
    )

    return {
        "healthy": True,
        "tool_count": len(list_tools()),
        "tools": list_tools(),
        "metrics": get_tool_metrics(),
        "version": "v1",
        "sdk": "FastMCP"
    }

@router.get("/google")
def google_health():
    from google.providers.google_providers import (
        GoogleMapsProvider, GooglePlacesProvider, GoogleGeocodingProvider, GoogleGeminiProvider, GoogleClientSingleton
    )
    
    response = {
        "healthy": True,
        "providers": {
            "maps": False,
            "places": False,
            "geocoding": False,
            "llm": False
        }
    }
    
    try:
        maps_provider = GoogleMapsProvider()
        places_provider = GooglePlacesProvider()
        geocoding_provider = GoogleGeocodingProvider()
        # Verify configuration is present and client initializes
        GoogleClientSingleton.get_maps_client()
        response["providers"]["maps"] = True
        response["providers"]["places"] = True
        response["providers"]["geocoding"] = True
    except Exception as e:
        response["healthy"] = False
        response["providers"]["maps"] = f"failed: {str(e)}"
        response["providers"]["places"] = f"failed: {str(e)}"
        response["providers"]["geocoding"] = f"failed: {str(e)}"
        
    try:
        llm_provider = GoogleGeminiProvider()
        # Verify configuration is present and client initializes
        GoogleClientSingleton.get_genai_client()
        response["providers"]["llm"] = True
    except Exception as e:
        response["healthy"] = False
        response["providers"]["llm"] = f"failed: {str(e)}"
        
    return response
