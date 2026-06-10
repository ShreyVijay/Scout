from app.services.mission_store import save_mission

mission = {
    "team": "Egypt",
    "budget": 2500,
    "travel_style": "Atmosphere",
    "objective": "Follow Egypt",
    "itinerary": [
        "New York",
        "Dallas",
        "Los Angeles"
    ],
    "status": "active"
}

save_mission(mission)

print("Mission saved")