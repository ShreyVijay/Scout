from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/saved-missions", tags=["saved-missions"])

class SavedMissionCreateRequest(BaseModel):
    email: str
    mission_id: str

@router.post("")
def create_saved_mission(request: SavedMissionCreateRequest):
    from app.db.mongodb import get_database
    from app.db.collections import SAVED_MISSIONS_COLLECTION
    from datetime import datetime
    import uuid
    
    db = get_database()
    doc = {
        "id": str(uuid.uuid4()),
        "email": request.email,
        "mission_id": request.mission_id,
        "created_at": datetime.utcnow().isoformat()
    }
    db[SAVED_MISSIONS_COLLECTION].insert_one(doc.copy())
    return {"success": True, "saved_mission": doc}

@router.get("")
def get_saved_missions(email: str = Query(...)):
    from app.db.mongodb import get_database
    from app.db.collections import SAVED_MISSIONS_COLLECTION
    
    db = get_database()
    cursor = db[SAVED_MISSIONS_COLLECTION].find({"email": email}, {"_id": 0})
    return {"success": True, "saved_missions": list(cursor)}

@router.delete("/{id}")
def delete_saved_mission(id: str):
    from app.db.mongodb import get_database
    from app.db.collections import SAVED_MISSIONS_COLLECTION
    
    db = get_database()
    result = db[SAVED_MISSIONS_COLLECTION].delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Saved mission not found")
    return {"success": True}
