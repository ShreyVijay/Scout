# backend/app/services/travel/ticket_service.py
from datetime import datetime

class TicketMarketProvider:
    """
    Abstract interface placeholder for match ticket market tracking (FIFA, Ticketmaster, StubHub, SeatGeek).
    """
    def search_tickets(self, match: str = "World Cup Match") -> list:
        match_name = match or "World Cup Match"
        return [
            {
                "match": match_name,
                "price": "$180",
                "availability": "Limited Quantity",
                "provider": "Ticketmaster (Mock Official)",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "match": match_name,
                "price": "$290 (Resale)",
                "availability": "Available",
                "provider": "StubHub (Mock Resale)",
                "last_updated": datetime.utcnow().isoformat()
            },
            {
                "match": match_name,
                "price": "$340 (Premium)",
                "availability": "Last 5 tickets",
                "provider": "SeatGeek (Mock)",
                "last_updated": datetime.utcnow().isoformat()
            }
        ]

def search_tickets(match: str = "World Cup Match") -> list:
    provider = TicketMarketProvider()
    return provider.search_tickets(match)
