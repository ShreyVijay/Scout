from app.mcp.schemas import error_response, success_response
from app.tools.budget_tools import (
    estimate_trip_cost as service_estimate_trip_cost,
    get_budget_status as service_get_budget_status
)


def get_budget_status(team: str):
    try:
        return success_response(service_get_budget_status(team))
    except Exception as exc:
        return error_response(exc)


def estimate_trip_cost(team: str):
    try:
        return success_response(service_estimate_trip_cost(team))
    except Exception as exc:
        return error_response(exc)
