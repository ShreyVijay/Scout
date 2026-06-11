from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from google.schemas.provider_dtos import VenueDTO, ExplanationDTO, RouteDTO
from google.services.gemini_explanation_service import GeminiExplanationService
from google.services.map_intelligence_service import MapIntelligenceService
from google.services.travel_intelligence_service import TravelIntelligenceService
from google.services.venue_intelligence_service import VenueIntelligenceService

router = APIRouter(prefix="/google", tags=["google"])

# Initialize services
gemini_service = GeminiExplanationService()
map_service = MapIntelligenceService()
travel_service = TravelIntelligenceService()
venue_service = VenueIntelligenceService()


class ExplanationRequest(BaseModel):
    recommendation: dict
    reasoning: dict
    audit: dict


class TravelPlanRequest(BaseModel):
    recommendation: dict
    route_data: dict


@router.get("/city/{city}/map")
def get_city_map(city: str):
    loc = map_service.get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City coordinates not found")
    return loc


@router.get("/stadium/{stadium}/map")
def get_stadium_map(stadium: str):
    loc = map_service.get_stadium_coordinates(stadium)
    if not loc:
        raise HTTPException(status_code=404, detail="Stadium coordinates not found")
    return loc


@router.get("/route")
def get_route(origin_city: str, dest_city: str):
    origin = map_service.get_city_coordinates(origin_city)
    dest = map_service.get_city_coordinates(dest_city)
    if not origin or not dest:
        raise HTTPException(status_code=404, detail="Coordinates not found for origin or destination")
    return travel_service.calculate_travel_metrics(origin, dest)


@router.get("/city/{city}/hotels", response_model=List[VenueDTO])
def get_city_hotels(city: str, radius: int = 5000):
    loc = map_service.get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return venue_service.nearby_hotels(loc, radius)


@router.get("/city/{city}/restaurants", response_model=List[VenueDTO])
def get_city_restaurants(city: str, radius: int = 5000):
    loc = map_service.get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return venue_service.nearby_restaurants(loc, radius)


@router.get("/city/{city}/attractions", response_model=List[VenueDTO])
def get_city_attractions(city: str, radius: int = 5000):
    loc = map_service.get_city_coordinates(city)
    if not loc:
        raise HTTPException(status_code=404, detail="City not found")
    return venue_service.nearby_attractions(loc, radius)


@router.post("/explain", response_model=ExplanationDTO)
def explain_recommendation(request: ExplanationRequest):
    return gemini_service.get_recommendation_explanation(
        request.recommendation,
        request.reasoning,
        request.audit
    )


@router.post("/travel-plan", response_model=ExplanationDTO)
def travel_plan(request: TravelPlanRequest):
    return gemini_service.get_travel_narrative(
        request.route_data,
        request.recommendation
    )
