# backend/app/api/travel_routes.py
from fastapi import APIRouter, Query
from app.services.travel.flight_service import search_flights
from app.services.travel.hotel_service import search_hotels
from app.services.travel.bus_service import search_buses
from app.services.travel.ticket_service import search_tickets

router = APIRouter(prefix="/travel", tags=["Travel Intelligence"])

@router.get("/flights")
def get_flights_endpoint(
    origin: str = Query(...),
    destination: str = Query(...),
    departure_date: str = Query(default=None)
):
    try:
        results = search_flights(origin, destination, departure_date)
        return {"flights": results}
    except Exception as e:
        return {"flights": [], "error": str(e)}

@router.get("/hotels")
def get_hotels_endpoint(city: str = Query(...)):
    try:
        results = search_hotels(city)
        return {"hotels": results}
    except Exception as e:
        return {"hotels": [], "error": str(e)}

@router.get("/buses")
def get_buses_endpoint(
    origin: str = Query(...),
    destination: str = Query(...),
    departure_date: str = Query(default=None)
):
    try:
        results = search_buses(origin, destination, departure_date)
        return {"buses": results}
    except Exception as e:
        return {"buses": [], "error": str(e)}

@router.get("/tickets")
def get_tickets_endpoint(match: str = Query(...)):
    try:
        results = search_tickets(match)
        return {"tickets": results}
    except Exception as e:
        return {"tickets": [], "error": str(e)}
