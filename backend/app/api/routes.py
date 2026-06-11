from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


# ── Request Models ──────────────────────────────────────────────

class MissionCreateRequest(BaseModel):
    team: str
    budget: int
    travel_style: str
    objective: str


class ChatRequest(BaseModel):
    message: str
    context: dict = Field(default_factory=dict)


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
    try:
        from app.services.city_search import get_all_cities
        cities = get_all_cities()
        return {"cities": cities}
    except Exception:
        return {"cities": []}


# ── GET /stadiums ───────────────────────────────────────────────

@router.get("/stadiums")
def get_stadiums_endpoint():
    try:
        from app.services.stadium_search import get_all_stadiums
        stadiums = get_all_stadiums()
        return {"stadiums": stadiums}
    except Exception:
        return {"stadiums": []}


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
def get_user_endpoint(email: str):
    from app.services.user_store import get_user
    user = get_user(email)
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
    user = get_user(request.email)
    if not user:
        user = {
            "user_id": request.email,
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


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    lower_message = message.lower()
    surface = request.context.get("surface", "Scout")
    saved_count = len(request.context.get("saved_recommendations", []))

    if "replan" in lower_message or "route" in lower_message:
        reply = (
            "Open the replanning flow for the active team, generate a recommendation, "
            "then compare the top ranked city against your budget and transport scores."
        )
        action = "open_replanning"
    elif "budget" in lower_message or "cost" in lower_message:
        reply = (
            "Check Budget Intelligence first: total budget, spent amount, projected "
            "remaining budget, and risk badge. If the badge is medium or higher, re-run "
            "the route before booking."
        )
        action = "review_budget"
    elif "city" in lower_message or "stadium" in lower_message:
        reply = (
            "Use City Intelligence for atmosphere, budget, transport, and fan-zone scores. "
            "Use Stadiums when venue capacity and host city context matter more than price."
        )
        action = "open_city_intelligence"
    else:
        reply = (
            "I can help you decide whether to monitor, replan, or save a recommendation. "
            f"You are currently on {surface}, with {saved_count} saved recommendations."
        )
        action = "explain_context"

    return {
        "reply": reply,
        "action": action,
        "context_used": {
            "surface": surface,
            "saved_recommendations": saved_count,
        },
    }
