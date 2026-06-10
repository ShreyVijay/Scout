from app.services.mission_service import create_mission

mission = create_mission(
    team="Egypt",
    budget=2500,
    travel_style="Atmosphere",
    objective="Follow Egypt"
)

print(mission)