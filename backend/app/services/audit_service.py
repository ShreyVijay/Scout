from contracts.recommendation import AuditResponse
from app.services.recommendation_service import get_recommendation_bundle


def get_audit(team: str) -> AuditResponse | None:
    bundle = get_recommendation_bundle(team)
    audit = bundle.get("audit") if bundle else None
    return AuditResponse.model_validate(audit) if audit else None
