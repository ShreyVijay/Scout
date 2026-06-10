from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class MissionResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class CityResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class StadiumResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class BudgetResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class PreferenceResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class RecommendationResponse:
    success: bool
    data: Any = None
    error: str | None = None


@dataclass
class ToolResponse:
    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def success_response(data, metadata=None):
    return asdict(
        ToolResponse(
            success=True,
            data=data,
            metadata=metadata or {}
        )
    )


def error_response(error):
    return asdict(
        ToolResponse(
            success=False,
            error=str(error)
        )
    )
