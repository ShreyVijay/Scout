from contracts.recommendation import RecommendationResponse
from app.services.mission_store import get_latest_mission
from app.services.replanning_engine import run_replanning


def get_recommendation_bundle(team: str) -> dict | None:
    mission = get_latest_mission(team)
    return run_replanning(mission) if mission else None


def get_recommendation(team: str) -> RecommendationResponse | None:
    bundle = get_recommendation_bundle(team)
    recommendation = bundle.get("recommendation") if bundle else None

    if recommendation:
        # score_metadata is typically populated by candidate_scoring_service
        score_metadata = recommendation.get("score_metadata", {})
        recommendation["provenance"] = {
            "candidate_source": recommendation.get("candidate_source"),
            "retrieval_score": recommendation.get("retrieval_score"),
            "source_multiplier": score_metadata.get("source_multiplier") or recommendation.get("source_multiplier")
        }

    return RecommendationResponse.model_validate(recommendation) if recommendation else None
