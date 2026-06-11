# backend/app/services/travel/hotel_service.py
from datetime import datetime

class HotelBookingProvider:
    """
    Abstract interface placeholder for hotel booking tracking providers (Booking.com, Expedia, Hotels.com, Amadeus Hotels).
    """
    def search_hotels(self, city: str = None) -> list:
        return [
            {
                "provider": "Booking.com (Mock)",
                "price": "$125/night",
                "availability": "4 rooms remaining",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "provider": "Expedia (Mock)",
                "price": "$140/night",
                "availability": "Available",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "provider": "Hotels.com (Mock)",
                "price": "$115/night",
                "availability": "Last 2 rooms",
                "last_updated": datetime.utcnow().isoformat()
            }
        ]

def search_hotels(city: str = None) -> list:
    provider = HotelBookingProvider()
    return provider.search_hotels(city)
