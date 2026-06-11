from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ToolMetadata(BaseModel):
    tool: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    latency_ms: float = 0
    version: str = "v1"


class ProvenanceMetadata(BaseModel):
    candidate_source: str | None = None
    retrieval_score: float | None = None
    source_multiplier: float | None = None
    rank: int | None = None


class ToolError(BaseModel):
    type: str
    message: str


class BaseToolResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: ToolError | None = None
    metadata: ToolMetadata


def success_response(tool: str, data: Any, latency_ms: float) -> dict:
    return BaseToolResponse(
        success=True,
        data=data,
        metadata=ToolMetadata(tool=tool, latency_ms=latency_ms),
    ).model_dump(mode="json", exclude_none=True)


def error_response(tool: str, error: Exception, latency_ms: float) -> dict:
    return BaseToolResponse(
        success=False,
        error=ToolError(type=type(error).__name__, message=str(error)),
        metadata=ToolMetadata(tool=tool, latency_ms=latency_ms),
    ).model_dump(mode="json", exclude_none=True)
