from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# ── Request Models ──────────────────────────────────────────────

class MissionCreateRequest(BaseModel):
    team: str
    budget: int
    travel_style: str
    objective: str


# ── POST /mission ───────────────────────────────────────────────

@router.post("/mission")
def create_mission_endpoint(request: MissionCreateRequest):
    from app.services.mission_service import create_mission

    try:
        mission = create_mission(
            team=request.team,
            budget=request.budget,
            travel_style=request.travel_style,
            objective=request.objective
        )

        # Strip internal Elasticsearch metadata before returning
        result = {
            k: v for k, v in mission.items()
            if k not in ["_elastic_id", "_seq_no", "_primary_term"]
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /mission/{team} ────────────────────────────────────────

@router.get("/mission/{team}")
def get_mission_endpoint(team: str):
    from app.services.mission_store import get_latest_mission
    from app.services.mission_budget_service import integrate_mission_budget

    mission = get_latest_mission(team)

    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission not found for team: {team}")

    # Integrate budget intelligence if not already present
    if "budget_intelligence" not in mission:
        try:
            mission = integrate_mission_budget(mission, spent_budget=0)
        except Exception:
            pass  # Budget intelligence is optional; don't fail the whole request

    result = {
        k: v for k, v in mission.items()
        if k not in ["_elastic_id", "_seq_no", "_primary_term"]
    }

    return result


# ── POST /replan/{team} ────────────────────────────────────────

@router.post("/replan/{team}")
def replan_endpoint(team: str):
    from app.services.mission_store import get_latest_mission
    from app.services.replanning_engine import run_replanning

    mission = get_latest_mission(team)

    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission not found for team: {team}")

    try:
        result = run_replanning(mission)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /cities ─────────────────────────────────────────────────

@router.get("/cities")
def get_cities_endpoint():
    from app.services.city_search import get_all_cities

    try:
        cities = get_all_cities()
        return {"cities": cities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /stadiums ───────────────────────────────────────────────

@router.get("/stadiums")
def get_stadiums_endpoint():
    from app.services.stadium_search import get_all_stadiums

    try:
        stadiums = get_all_stadiums()
        return {"stadiums": stadiums}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /budget/{team} ─────────────────────────────────────────

@router.get("/budget/{team}")
def get_budget_endpoint(team: str):
    from app.services.mission_store import get_latest_mission
    from app.services.budget_intelligence import get_budget_intelligence

    mission = get_latest_mission(team)

    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission not found for team: {team}")

    try:
        intel = get_budget_intelligence(mission, spent_budget=0)
        return intel
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /preferences/{team} ────────────────────────────────────

@router.get("/preferences/{team}")
def get_preferences_endpoint(team: str):
    from app.services.mission_store import get_latest_mission
    from app.services.mission_preference_service import resolve_mission_preferences

    mission = get_latest_mission(team)

    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission not found for team: {team}")

    mission_id = mission.get("mission_id")

    try:
        preferences = resolve_mission_preferences(mission_id)

        result = {
            k: v for k, v in preferences.items()
            if k not in ["_elastic_id", "_seq_no", "_primary_term"]
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /city/{city} ───────────────────────────────────────────

@router.get("/city/{city}")
def get_city_detail_endpoint(city: str):
    from app.services.city_intelligence import get_city_intelligence

    result = get_city_intelligence(city)

    if not result:
        raise HTTPException(status_code=404, detail=f"City not found: {city}")

    return result


# ── GET /stadium/{stadium} ─────────────────────────────────────

@router.get("/stadium/{stadium}")
def get_stadium_detail_endpoint(stadium: str):
    from app.services.stadium_search import get_stadium

    result = get_stadium(stadium)

    if not result:
        raise HTTPException(status_code=404, detail=f"Stadium not found: {stadium}")

    return result


# ── GET /user ──────────────────────────────────────────────────

@router.get("/user")
def get_user_endpoint():
    from app.services.user_store import get_user
    user = get_user("default-fan")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── POST /user ─────────────────────────────────────────────────

class UserPreferencesUpdateRequest(BaseModel):
    atmosphere_weight: float
    budget_weight: float
    transport_weight: float

class UserUpdateRequest(BaseModel):
    email: str
    name: str
    preferences: UserPreferencesUpdateRequest

@router.post("/user")
def update_user_endpoint(request: UserUpdateRequest):
    from app.services.user_store import get_user, save_user
    user = get_user("default-fan")
    if not user:
        user = {
            "user_id": "default-fan",
            "email": request.email,
            "name": request.name,
            "preferences": {
                "atmosphere_weight": request.preferences.atmosphere_weight,
                "budget_weight": request.preferences.budget_weight,
                "transport_weight": request.preferences.transport_weight
            },
            "saved_missions": []
        }
    else:
        user["email"] = request.email
        user["name"] = request.name
        user["preferences"] = {
            "atmosphere_weight": request.preferences.atmosphere_weight,
            "budget_weight": request.preferences.budget_weight,
            "transport_weight": request.preferences.transport_weight
        }
    
    updated = save_user(user)
    return updated


# ── GET /missions ──────────────────────────────────────────────

@router.get("/missions")
def get_all_missions_endpoint():
    try:
        from app.services.user_store import es
        if not es.indices.exists(index="missions"):
            return {"missions": []}
        result = es.search(
            index="missions",
            query={"match_all": {}},
            size=100
        )
        missions = []
        for hit in result["hits"]["hits"]:
            src = hit["_source"]
            src["_elastic_id"] = hit["_id"]
            # remove private keys
            src = {k: v for k, v in src.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
            missions.append(src)
        return {"missions": missions}
    except Exception as e:
        return {"missions": []}

