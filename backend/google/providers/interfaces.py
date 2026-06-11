from abc import ABC, abstractmethod
from typing import List, Optional

from google.schemas.provider_dtos import LocationDTO, RouteDTO, VenueDTO, ExplanationDTO


class MapsProvider(ABC):
    @abstractmethod
    def get_route(self, origin: LocationDTO, destination: LocationDTO) -> RouteDTO:
        pass


class PlacesProvider(ABC):
    @abstractmethod
    def find_hotels(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        pass

    @abstractmethod
    def find_restaurants(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        pass

    @abstractmethod
    def find_attractions(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        pass

    @abstractmethod
    def find_fan_zones(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        pass


class GeocodingProvider(ABC):
    @abstractmethod
    def geocode(self, address: str) -> Optional[LocationDTO]:
        pass


class LLMProvider(ABC):
    @abstractmethod
    def generate_explanation(self, recommendation: dict, reasoning: dict, audit: dict) -> ExplanationDTO:
        pass

    @abstractmethod
    def generate_travel_narrative(self, route_data: dict, recommendation: dict) -> ExplanationDTO:
        pass
