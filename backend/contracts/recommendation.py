from typing import Any

from pydantic import Field

from contracts.base import ScoutDTO
from scout_mcp.schemas.base import ProvenanceMetadata


class RecommendationResponse(ScoutDTO):
    city: str | None = None
    match: str | None = None
    reason: str | None = None
    rank: int | None = None
    raw_score: float | None = None
    final_score: float | None = None
    score_metadata: dict[str, Any] = Field(default_factory=dict)
    contributions: dict[str, float] = Field(default_factory=dict)
    provenance: ProvenanceMetadata | None = None


class ReasoningResponse(ScoutDTO):
    decision: str | None = None
    reasons: list[str] = Field(default_factory=list)
    top_factors: list[str] = Field(default_factory=list)
    contributions: dict[str, float] = Field(default_factory=dict)
    provenance: ProvenanceMetadata | None = None


class AuditResponse(ScoutDTO):
    winner: str | None = None
    audit: list[dict[str, Any]] = Field(default_factory=list)
    factor_breakdown: dict[str, Any] = Field(default_factory=dict)
