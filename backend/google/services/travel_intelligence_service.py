from google.providers.google_providers import GoogleMapsProvider
from google.schemas.provider_dtos import LocationDTO

class TravelIntelligenceService:
    def __init__(self):
        self.provider = GoogleMapsProvider()

    def calculate_travel_metrics(self, origin: LocationDTO, destination: LocationDTO) -> dict:
        route = self.provider.get_route(origin, destination)
        
        # Calculate burden score based on distance, time, and arbitrary transitions for the sake of the API
        distance_burden = route.distance_km * 0.05
        time_burden = route.travel_time_hours * 2.0
        
        burden_score = distance_burden + time_burden
        
        return {
            "distance_km": route.distance_km,
            "travel_time_hours": route.travel_time_hours,
            "burden_score": burden_score,
            "polyline": route.polyline
        }
