from typing import List

from google.providers.google_providers import GooglePlacesProvider
from google.schemas.provider_dtos import LocationDTO, VenueDTO

class VenueIntelligenceService:
    def __init__(self):
        self.provider = GooglePlacesProvider()

    def nearby_hotels(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self.provider.find_hotels(location, radius)

    def nearby_restaurants(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self.provider.find_restaurants(location, radius)

    def nearby_attractions(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self.provider.find_attractions(location, radius)

    def nearby_fan_zones(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self.provider.find_fan_zones(location, radius)
