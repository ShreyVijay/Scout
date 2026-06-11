from typing import Optional

from google.providers.google_providers import GoogleGeocodingProvider
from google.schemas.provider_dtos import LocationDTO

# We'll use the existing Elasticsearch client from Scout
from app.mcp.elastic_client import get_elastic_client


class MapIntelligenceService:
    def __init__(self):
        self.provider = GoogleGeocodingProvider()
        self.es = get_elastic_client()

    def get_city_coordinates(self, city_name: str) -> Optional[LocationDTO]:
        # First check Elasticsearch
        try:
            doc = self.es.get(index="cities", id=city_name)
            source = doc.get("_source", {})
            if "lat" in source and "lng" in source:
                return LocationDTO(lat=source["lat"], lng=source["lng"])
        except Exception:
            pass  # Document not found or error

        # Fallback to Geocoding
        loc = self.provider.geocode(city_name)
        if loc:
            # Update ES to save for future
            try:
                self.es.update(
                    index="cities",
                    id=city_name,
                    body={"doc": {"lat": loc.lat, "lng": loc.lng}}
                )
            except Exception:
                pass
        return loc

    def get_stadium_coordinates(self, stadium_name: str) -> Optional[LocationDTO]:
        # First check Elasticsearch
        try:
            doc = self.es.get(index="stadiums", id=stadium_name)
            source = doc.get("_source", {})
            if "lat" in source and "lng" in source:
                return LocationDTO(lat=source["lat"], lng=source["lng"])
        except Exception:
            pass

        loc = self.provider.geocode(stadium_name)
        if loc:
            try:
                self.es.update(
                    index="stadiums",
                    id=stadium_name,
                    body={"doc": {"lat": loc.lat, "lng": loc.lng}}
                )
            except Exception:
                pass
        return loc
