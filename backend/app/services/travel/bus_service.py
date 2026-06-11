# backend/app/services/travel/bus_service.py
from datetime import datetime

class BusProvider:
    """
    Abstract interface placeholder for bus travel tracking providers like RedBus, Busbud, FlixBus.
    """
    def search_buses(self, origin: str, destination: str, departure_date: str) -> list:
        return [
            {
                "provider": "FlixBus (Mock)",
                "price": "$48",
                "availability": "Plenty of seats",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "provider": "Busbud (Mock Greyhound)",
                "price": "$55",
                "availability": "Limited",
                "last_updated": datetime.utcnow().isoformat()
            }
        ]

def search_buses(origin: str, destination: str, departure_date: str) -> list:
    provider = BusProvider()
    return provider.search_buses(origin, destination, departure_date)
