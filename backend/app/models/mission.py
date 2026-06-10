from pydantic import BaseModel

class Mission(BaseModel):

    team: str

    budget: int

    travel_style: str

    objective: str

    itinerary: list

    mission_state: str

    tournament_state: str

    state_history: list