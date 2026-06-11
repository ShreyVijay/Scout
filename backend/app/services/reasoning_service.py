from contracts.recommendation import ReasoningResponse
from app.services.recommendation_service import get_recommendation_bundle


def get_reasoning(team: str) -> ReasoningResponse | None:
    bundle = get_recommendation_bundle(team)
    reasoning = bundle.get("reasoning") if bundle else None

    if reasoning:
        reasoning["provenance"] = {
            "candidate_source": reasoning.get("candidate_source"),
            "retrieval_score": reasoning.get("retrieval_score"),
            "source_multiplier": reasoning.get("source_multiplier")
        }

    return ReasoningResponse.model_validate(reasoning) if reasoning else None
