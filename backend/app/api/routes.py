from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


# ── Request Models ──────────────────────────────────────────────

class MissionCreateRequest(BaseModel):
    team: str
    budget: int
    travel_style: str
    objective: str
    email: str = None


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

        # Associate with user if email is provided
        if request.email:
            from app.services.user_store import get_user, save_user
            from app.db.mongodb import get_database
            from app.db.collections import USER_MISSIONS_COLLECTION
            from datetime import datetime

            user = get_user(request.email)
            if not user:
                user = {
                    "user_id": request.email,
                    "email": request.email,
                    "name": request.email.split("@")[0],
                    "mission_history": [],
                }

            if user.get("current_mission"):
                history = user.get("mission_history", [])
                if user["current_mission"] not in history:
                    history.append(user["current_mission"])
                user["mission_history"] = history

            user["current_mission"] = result["mission_id"]
            save_user(user)

            db = get_database()
            now = datetime.utcnow().isoformat()
            db[USER_MISSIONS_COLLECTION].update_one(
                {"email": request.email, "mission_id": result["mission_id"]},
                {
                    "$set": {
                        "email": request.email,
                        "user_id": request.email,
                        "mission_id": result["mission_id"],
                        "team": result["team"],
                        "is_current": True,
                        "updated_at": now,
                    },
                    "$setOnInsert": {"created_at": now},
                },
                upsert=True,
            )
            db[USER_MISSIONS_COLLECTION].update_many(
                {"email": request.email, "mission_id": {"$ne": result["mission_id"]}},
                {"$set": {"is_current": False}},
            )

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
def get_all_missions_endpoint(email: str = None):
    try:
        from app.services.user_store import get_user, es
        from app.db.mongodb import get_database
        from app.db.collections import USER_MISSIONS_COLLECTION
        if not es.indices.exists(index="missions"):
            return {"missions": []}
            
        if not email:
            return {"missions": []}
            
        user = get_user(email)
        if not user:
            return {"missions": []}
            
        current_id = user.get("current_mission")
        history_ids = user.get("mission_history", [])

        try:
            db = get_database()
            current_link = db[USER_MISSIONS_COLLECTION].find_one(
                {"email": email, "is_current": True},
                {"_id": 0},
            )
            if current_link:
                current_id = current_link.get("mission_id") or current_id

            linked_ids = [
                doc["mission_id"]
                for doc in db[USER_MISSIONS_COLLECTION].find(
                    {"email": email},
                    {"_id": 0, "mission_id": 1},
                )
                if doc.get("mission_id")
            ]
            if linked_ids:
                history_ids = [mission_id for mission_id in linked_ids if mission_id != current_id]
        except Exception:
            pass
        
        all_ids = []
        if current_id:
            all_ids.append(current_id)
        all_ids.extend(history_ids)
        
        if not all_ids:
            return {"missions": []}
            
        # Fetch those specific missions
        result = es.search(
            index="missions",
            query={"terms": {"mission_id.keyword": all_ids}},
            size=100
        )
        
        missions_by_id = {}
        for hit in result["hits"]["hits"]:
            src = hit["_source"]
            src["_elastic_id"] = hit["_id"]
            src = {k: v for k, v in src.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}
            missions_by_id[src.get("mission_id")] = src

        current_mission = missions_by_id.get(current_id)
        history_missions = [missions_by_id[mission_id] for mission_id in history_ids if mission_id in missions_by_id]
        missions = ([current_mission] if current_mission else []) + history_missions

        return {
            "missions": missions,
            "current_mission": current_mission,
            "history_missions": history_missions,
            "current_mission_id": current_id,
        }
    except Exception as e:
        return {"missions": []}


@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    lower_message = message.lower()
    surface = request.context.get("surface", "skaut")
    saved_count = len(request.context.get("saved_recommendations", []))

    import os

    blocked_terms = ["visa fraud", "fake ticket", "bypass security", "evade police"]
    if any(term in lower_message for term in blocked_terms):
        return {
            "reply": "I can help with safe travel, verified tickets, budgets, and route replanning, but I cannot assist with unsafe or illegal actions.",
            "action": "explain_context",
            "context_used": {
                "surface": surface,
                "saved_recommendations": saved_count,
            },
        }
    
    # Check if Gemini API key exists
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        return {"reply": "Gemini API key is not configured.", "action": "explain_context", "context_used": {}}
        
    try:
        from google import genai
        client = genai.Client(api_key=gemini_key)
    except Exception:
        client = None
    
    system_prompt = f"""You are skaut, an intelligent travel agent for the FIFA 2026 World Cup.
The 2026 World Cup features 48 teams, 104 matches, and a new Round of 32 format where top 2 + 8 best third-place teams advance.
Current surface: {surface}
Saved recommendations: {saved_count}
Answer briefly and proactively help them plan their World Cup travel. Recommending actions like 'open_replanning' or 'review_budget' is highly encouraged if relevant."""

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=system_prompt + "\n\nUser: " + message,
            )
            reply = response.text
        except Exception as e:
            reply = f"skaut AI could not reach Gemini right now. I can still route you through the built-in mission, map, budget, and replanning tools. Detail: {str(e)}"
    else:
        reply = "Gemini is not available in this backend environment yet. skaut can still help with mission maps, budget review, and replanning from the app data."
        
    action = "explain_context"
    if "replan" in lower_message or "route" in lower_message:
        action = "open_replanning"
    elif "budget" in lower_message or "cost" in lower_message:
        action = "review_budget"
    elif "city" in lower_message or "stadium" in lower_message:
        action = "open_city_intelligence"

    return {
        "reply": reply,
        "action": action,
        "context_used": {
            "surface": surface,
            "saved_recommendations": saved_count,
        },
    }
