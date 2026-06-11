from typing import Optional, List
from pydantic import BaseModel


class LocationDTO(BaseModel):
    lat: float
    lng: float


class RouteDTO(BaseModel):
    distance_km: float
    travel_time_hours: float
    polyline: Optional[str] = None


class VenueDTO(BaseModel):
    name: str
    category: str
    rating: float
    location: LocationDTO


class ExplanationDTO(BaseModel):
    explanation: str
