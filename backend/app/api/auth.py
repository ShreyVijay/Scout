from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: str
    name: str

class LoginRequest(BaseModel):
    email: str

@router.post("/register")
def register(request: RegisterRequest):
    from app.db.mongodb import get_database
    from app.db.collections import USERS_COLLECTION
    db = get_database()
    
    user_doc = db[USERS_COLLECTION].find_one({"email": request.email}, {"_id": 0})
    if not user_doc:
        new_user = {"email": request.email, "name": request.name}
        db[USERS_COLLECTION].insert_one(new_user.copy())
        return {"success": True, "user": new_user}
    return {"success": True, "user": user_doc}

@router.post("/login")
def login(request: LoginRequest):
    from app.db.mongodb import get_database
    from app.db.collections import USERS_COLLECTION
    db = get_database()
    
    user_doc = db[USERS_COLLECTION].find_one({"email": request.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "user": user_doc}

@router.get("/me")
def get_me(email: str = Query(...)):
    from app.db.mongodb import get_database
    from app.db.collections import USERS_COLLECTION
    db = get_database()
    
    user_doc = db[USERS_COLLECTION].find_one({"email": email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    return user_doc
