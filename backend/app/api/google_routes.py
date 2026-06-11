from typing import List

import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel

from app.mcp.elastic_client import ElasticConfigurationError
from google.schemas.provider_dtos import ExplanationDTO, VenueDTO
from google.services.gemini_explanation_service import GeminiExplanationService
from google.services.map_intelligence_service import MapIntelligenceService
from google.services.travel_intelligence_service import TravelIntelligenceService
from google.services.venue_intelligence_service import VenueIntelligenceService
from google.settings import get_secret

router = APIRouter(prefix="/google", tags=["google"])

INTEGRATION_UNAVAILABLE = "Google/Elastic integration not configured"

_gemini_service = None
_map_service = None
_travel_service = None
_venue_service = None


class ExplanationRequest(BaseModel):
    recommendation: dict
    reasoning: dict
    audit: dict


class TravelPlanRequest(BaseModel):
    recommendation: dict
    route_data: dict


def integration_unavailable(exc: Exception):
    raise HTTPException(
        status_code=503,
        detail=f"{INTEGRATION_UNAVAILABLE}: {exc}",
    )


def require_google_maps_config():
    if not get_secret("GOOGLE_MAPS_API_KEY"):
        integration_unavailable(ValueError("GOOGLE_MAPS_API_KEY not found"))


def require_google_gemini_config():
    if not get_secret("GOOGLE_GEMINI_API_KEY"):
        integration_unavailable(ValueError("GOOGLE_GEMINI_API_KEY not found"))


def get_gemini_service():
    global _gemini_service
    require_google_gemini_config()
    if _gemini_service is None:
        try:
            _gemini_service = GeminiExplanationService()
        except Exception as exc:
            integration_unavailable(exc)
    return _gemini_service


def get_map_service():
    global _map_service
    require_google_maps_config()
    if _map_service is None:
        try:
            _map_service = MapIntelligenceService()
        except ElasticConfigurationError as exc:
            integration_unavailable(exc)
        except Exception as exc:
            integration_unavailable(exc)
    return _map_service


def get_travel_service():
    global _travel_service
    require_google_maps_config()
    if _travel_service is None:
        try:
            _travel_service = TravelIntelligenceService()
        except Exception as exc:
            integration_unavailable(exc)
    return _travel_service


def get_venue_service():
    global _venue_service
    require_google_maps_config()
    if _venue_service is None:
        try:
            _venue_service = VenueIntelligenceService()
        except Exception as exc:
            integration_unavailable(exc)
    return _venue_service


@router.get("/city/{city}/map")
def get_city_map(city: str):
    loc = get_map_service().get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City coordinates not found")
    return loc


@router.get("/stadium/{stadium}/map")
def get_stadium_map(stadium: str):
    loc = get_map_service().get_stadium_coordinates(stadium)
    if not loc:
        raise HTTPException(status_code=404, detail="Stadium coordinates not found")
    return loc


@router.get("/place-photo")
def get_place_photo_by_query(query: str = Query(...), max_width: int = 900):
    require_google_maps_config()
    api_key = get_secret("GOOGLE_MAPS_API_KEY")
    client = get_venue_service().provider.get_maps_client() if hasattr(get_venue_service().provider, "get_maps_client") else None
    if client is None:
        from google.providers.google_providers import GoogleClientSingleton
        client = GoogleClientSingleton.get_maps_client()

    search = client.places(query=query)
    results = search.get("results", [])
    photos = results[0].get("photos", []) if results else []
    if not photos:
        raise HTTPException(status_code=404, detail="Google Places photo not found")
    return get_place_photo(photos[0]["photo_reference"], max_width)


@router.get("/place-photo/{photo_reference}")
def get_place_photo(photo_reference: str, max_width: int = 900):
    require_google_maps_config()
    api_key = get_secret("GOOGLE_MAPS_API_KEY")
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/photo",
        params={
            "maxwidth": max_width,
            "photo_reference": photo_reference,
            "key": api_key,
        },
        timeout=12,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail="Google Places photo request failed")
    return Response(
        content=response.content,
        media_type=response.headers.get("content-type", "image/jpeg"),
        headers={"Cache-Control": "public, max-age=86400"},
    )


@router.get("/route")
def get_route(origin_city: str, dest_city: str):
    map_service = get_map_service()
    origin = map_service.get_city_coordinates(origin_city)
    dest = map_service.get_city_coordinates(dest_city)
    if not origin or not dest:
        raise HTTPException(status_code=404, detail="Coordinates not found for origin or destination")
    return get_travel_service().calculate_travel_metrics(origin, dest)


@router.get("/city/{city}/hotels", response_model=List[VenueDTO])
def get_city_hotels(city: str, radius: int = 5000):
    loc = get_map_service().get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return get_venue_service().nearby_hotels(loc, radius)


@router.get("/city/{city}/restaurants", response_model=List[VenueDTO])
def get_city_restaurants(city: str, radius: int = 5000):
    loc = get_map_service().get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return get_venue_service().nearby_restaurants(loc, radius)


@router.get("/city/{city}/attractions", response_model=List[VenueDTO])
def get_city_attractions(city: str, radius: int = 5000):
    loc = get_map_service().get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return get_venue_service().nearby_attractions(loc, radius)


@router.post("/explain", response_model=ExplanationDTO)
def explain_recommendation(request: ExplanationRequest):
    return get_gemini_service().get_recommendation_explanation(
        request.recommendation,
        request.reasoning,
        request.audit,
    )


@router.post("/travel-plan", response_model=ExplanationDTO)
def travel_plan(request: TravelPlanRequest):
    return get_gemini_service().get_travel_narrative(
        request.route_data,
        request.recommendation,
    )
