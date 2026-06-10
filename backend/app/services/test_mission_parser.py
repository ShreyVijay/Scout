from app.services.mission_parser import parse_mission

mission = parse_mission(
    """
    I am Egyptian.

    Budget $2500.

    I want the best atmosphere.

    Follow Egypt through the tournament.
    """
)

print(mission)