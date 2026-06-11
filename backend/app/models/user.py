from pydantic import BaseModel, Field
from typing import List

class UserPreferences(BaseModel):
    atmosphere_weight: float = 0.5
    budget_weight: float = 0.3
    transport_weight: float = 0.2

class User(BaseModel):
    user_id: str
    email: str
    name: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    saved_missions: List[str] = Field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
