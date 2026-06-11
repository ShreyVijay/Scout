# backend/app/services/travel/flight_service.py
from abc import ABC, abstractmethod
from datetime import datetime

class TravelProvider(ABC):
    """
    Abstract interface for Travel Intelligence API integration.
    Guarantees no provider lock-in when switching between Amadeus, Skyscanner, Kiwi, etc.
    """
    @abstractmethod
    def search_flights(self, origin: str, destination: str, departure_date: str) -> list:
        pass

class MockFlightProvider(TravelProvider):
    def search_flights(self, origin: str, destination: str, departure_date: str) -> list:
        # Mocking flights dynamically based on parameters
        d_date = departure_date or datetime.utcnow().date().isoformat()
        return [
            {
                "provider": "Amadeus (Mock Delta)",
                "price": "$380",
                "availability": "5 seats left",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "provider": "Skyscanner (Mock United)",
                "price": "$420",
                "availability": "Available",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "provider": "Kiwi (Mock Spirit)",
                "price": "$295",
                "availability": "Last seat",
                "last_updated": datetime.utcnow().isoformat()
            }
        ]

def search_flights(origin: str, destination: str, departure_date: str) -> list:
    """
    Exposed wrapper that uses the mock provider for now.
    Easily plug real APIs later with zero UI or backend route changes.
    """
    provider = MockFlightProvider()
    return provider.search_flights(origin, destination, departure_date)
