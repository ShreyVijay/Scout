from pydantic import BaseModel, ConfigDict


class ScoutDTO(BaseModel):
    model_config = ConfigDict(extra="allow")
