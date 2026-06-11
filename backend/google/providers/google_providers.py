import json
from typing import List, Optional

import googlemaps
from google import genai

from google.schemas.provider_dtos import LocationDTO, RouteDTO, VenueDTO, ExplanationDTO
from google.providers.interfaces import MapsProvider, PlacesProvider, GeocodingProvider, LLMProvider
from google.settings import get_secret


class GoogleClientSingleton:
    _maps_client = None
    _genai_client = None

    @classmethod
    def get_maps_client(cls):
        if not cls._maps_client:
            api_key = get_secret("GOOGLE_MAPS_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_MAPS_API_KEY not found")
            cls._maps_client = googlemaps.Client(key=api_key)
        return cls._maps_client

    @classmethod
    def get_genai_client(cls):
        if not cls._genai_client:
            project_id = get_secret("GCP_PROJECT_ID")
            if project_id:
                # Use Vertex AI via Application Default Credentials (Cloud Credits)
                cls._genai_client = genai.Client(vertexai=True, project=project_id, location="us-central1")
            else:
                api_key = get_secret("GOOGLE_GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GCP_PROJECT_ID or GOOGLE_GEMINI_API_KEY must be provided")
                cls._genai_client = genai.Client(api_key=api_key)
        return cls._genai_client


class GoogleMapsProvider(MapsProvider):
    def get_route(self, origin: LocationDTO, destination: LocationDTO) -> RouteDTO:
        try:
            client = GoogleClientSingleton.get_maps_client()
            directions = client.directions(
                origin=(origin.lat, origin.lng),
                destination=(destination.lat, destination.lng),
                mode="driving"
            )
            
            if not directions:
                # Fallback to defaults if no route found
                return RouteDTO(distance_km=0.0, travel_time_hours=0.0)

            leg = directions[0]["legs"][0]
            distance_meters = leg["distance"]["value"]
            duration_seconds = leg["duration"]["value"]

            return RouteDTO(
                distance_km=distance_meters / 1000.0,
                travel_time_hours=duration_seconds / 3600.0,
                polyline=directions[0].get("overview_polyline", {}).get("points")
            )
        except Exception:
            return RouteDTO(distance_km=0.0, travel_time_hours=0.0)


class GooglePlacesProvider(PlacesProvider):
    def _search_places(self, location: LocationDTO, radius: int, query: str, type_str: str) -> List[VenueDTO]:
        try:
            client = GoogleClientSingleton.get_maps_client()
            places = client.places_nearby(
                location=(location.lat, location.lng),
                radius=radius,
                keyword=query,
                type=type_str
            )

            results = []
            for p in places.get("results", [])[:5]: # Top 5
                photos = p.get("photos") or []
                photo_reference = photos[0].get("photo_reference") if photos else None
                results.append(VenueDTO(
                    name=p.get("name", "Unknown"),
                    category=type_str,
                    rating=p.get("rating", 0.0),
                    photo_url=f"/google/place-photo/{photo_reference}" if photo_reference else None,
                    vicinity=p.get("vicinity") or p.get("formatted_address"),
                    price_level=p.get("price_level"),
                    place_id=p.get("place_id"),
                    location=LocationDTO(
                        lat=p["geometry"]["location"]["lat"],
                        lng=p["geometry"]["location"]["lng"]
                    )
                ))
            return results
        except Exception:
            return []

    def find_hotels(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self._search_places(location, radius, "hotel", "lodging")

    def find_restaurants(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self._search_places(location, radius, "restaurant", "restaurant")

    def find_attractions(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self._search_places(location, radius, "tourist attraction", "tourist_attraction")

    def find_fan_zones(self, location: LocationDTO, radius: int = 5000) -> List[VenueDTO]:
        return self._search_places(location, radius, "sports bar", "bar")


class GoogleGeocodingProvider(GeocodingProvider):
    def geocode(self, address: str) -> Optional[LocationDTO]:
        try:
            client = GoogleClientSingleton.get_maps_client()
            result = client.geocode(address)
            if not result:
                return None
            loc = result[0]["geometry"]["location"]
            return LocationDTO(lat=loc["lat"], lng=loc["lng"])
        except Exception:
            return None


class GoogleGeminiProvider(LLMProvider):
    def generate_explanation(self, recommendation: dict, reasoning: dict, audit: dict) -> ExplanationDTO:
        prompt = f"""
        You are a travel agent assistant for skaut.
        Based on the following system decision, explain to the user why this city was chosen in 2-3 friendly sentences.
        Recommendation: {json.dumps(recommendation)}
        Reasoning: {json.dumps(reasoning)}
        """
        try:
            client = GoogleClientSingleton.get_genai_client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return ExplanationDTO(explanation=response.text)
        except Exception as e:
            return ExplanationDTO(explanation="Unable to generate explanation at this time.")

    def generate_travel_narrative(self, route_data: dict, recommendation: dict) -> ExplanationDTO:
        prompt = f"""
        You are a travel agent assistant for skaut.
        Based on the recommendation and travel details, provide a short travel narrative.
        Recommendation: {json.dumps(recommendation)}
        Travel Route: {json.dumps(route_data)}
        """
        try:
            client = GoogleClientSingleton.get_genai_client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return ExplanationDTO(explanation=response.text)
        except Exception:
            return ExplanationDTO(explanation="Unable to generate travel narrative at this time.")
