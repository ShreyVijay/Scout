from app.services import candidate_enrichment_service
from app.services.candidate_enrichment_service import enrich_candidate
from app.services.candidate_scoring_service import score_candidate
from app.services.replanning_decision_service import choose_candidate
from app.services.replanning_reasoning_service import generate_reasoning


def run_metadata_pipeline_test():
    print("--- STARTING METADATA PIPELINE TEST ---")

    original_get_city = candidate_enrichment_service.get_city

    def fake_get_city(city_name):
        return {
            "city": city_name,
            "country": "USA",
            "description": "Test city metadata.",
            "hotel_cost": 120,
            "transport_cost": 40,
            "food_cost": 40,
            "atmosphere_score": 9.0,
            "budget_score": 6.0,
            "transport_score": 8.0,
            "fan_zone_score": 9.0
        }

    candidate = {
        "city": "Dallas",
        "match": None,
        "reason": "Semantic city candidate.",
        "candidate_source": "semantic_city",
        "retrieval_score": 8.9,
        "retrieval_reason": "Matched football atmosphere query.",
        "candidate_origin": {
            "index": "cities"
        },
        "future_metadata": "preserve-me"
    }

    preferences = {
        "atmosphere_weight": 0.5,
        "budget_weight": 0.3,
        "transport_weight": 0.2
    }

    try:
        candidate_enrichment_service.get_city = fake_get_city

        enriched = enrich_candidate(
            candidate
        )
        scored = score_candidate(
            enriched,
            preferences,
            remaining_budget=100
        )
        decision = choose_candidate(
            [candidate],
            preferences,
            remaining_budget=100
        )
        winner = decision["winner"]
        reasoning = generate_reasoning(
            winner,
            preferences
        )

    finally:
        candidate_enrichment_service.get_city = original_get_city

    print(f"Enriched candidate: {enriched}")
    print(f"Scored candidate: {scored}")
    print(f"Winner: {winner}")
    print(f"Reasoning: {reasoning}")

    assert enriched["candidate_source"] == "semantic_city"
    assert enriched["retrieval_score"] == 8.9
    assert enriched["retrieval_reason"] == "Matched football atmosphere query."
    assert enriched["candidate_origin"] == {
        "index": "cities"
    }
    assert enriched["future_metadata"] == "preserve-me"

    assert scored["candidate_source"] == "semantic_city"
    assert scored["retrieval_score"] == 8.9
    assert "score_metadata" in scored
    assert scored["score_metadata"]["raw_score"] == scored["raw_score"]
    assert scored["score_metadata"]["budget_penalty_applied"] is True
    assert scored["score_metadata"]["penalty_ratio"] == 2.0

    assert winner["candidate_source"] == "semantic_city"
    assert winner["retrieval_score"] == 8.9
    assert "score_metadata" in winner
    assert winner["score_metadata"]["budget_penalty_applied"] is True

    assert decision["rankings"][0]["candidate_source"] == "semantic_city"
    assert decision["rankings"][0]["retrieval_score"] == 8.9
    assert "score_metadata" in decision["rankings"][0]

    assert reasoning["decision"] == "Dallas"
    assert reasoning["candidate_source"] == "semantic_city"
    assert reasoning["retrieval_score"] == 8.9
    assert "reasons" in reasoning
    assert "Selected by decision engine" in reasoning["reasons"]
    assert "Originated from semantic city retrieval" in reasoning["reasons"]
    assert "Highest final score among candidates" in reasoning["reasons"]
    assert "Budget penalty applied" in reasoning["reasons"]

    print("--- METADATA PIPELINE TEST PASSED SUCCESSFULLY ---")


if __name__ == "__main__":
    run_metadata_pipeline_test()
