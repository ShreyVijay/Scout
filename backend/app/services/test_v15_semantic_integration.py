from app.services import replanning_candidate_service as candidate_service


def run_semantic_integration_test():
    print("--- STARTING V1.5 SEMANTIC CANDIDATE INTEGRATION TEST ---")

    route_candidates = [
        {
            "city": "Miami",
            "match": "Quarter Final",
            "reason": "High-energy knockout atmosphere"
        },
        {
            "city": "Kansas City",
            "match": "Round of 16",
            "reason": "Lower hotel and travel costs"
        }
    ]

    semantic_city_candidates = [
        {
            "candidate_type": "city",
            "city": "Miami",
            "description": "Tropical football atmosphere.",
            "retrieval_score": 9.8
        },
        {
            "candidate_type": "city",
            "city": "Dallas",
            "description": "Major football culture.",
            "retrieval_score": 8.9
        }
    ]

    semantic_stadium_candidates = [
        {
            "candidate_type": "stadium",
            "stadium": "Lumen Field",
            "city": "Seattle",
            "description": "Loud matchday stadium.",
            "retrieval_score": 9.1
        },
        {
            "candidate_type": "stadium",
            "stadium": "AT&T Stadium",
            "city": "Dallas",
            "description": "Large football stadium.",
            "retrieval_score": 7.4
        }
    ]

    original_get_alternative_routes = candidate_service.get_alternative_routes
    original_retrieve_city_candidates = (
        candidate_service.retrieve_city_candidates
    )
    original_retrieve_stadium_candidates = (
        candidate_service.retrieve_stadium_candidates
    )

    calls = {
        "city_query": None,
        "city_size": None,
        "stadium_query": None,
        "stadium_size": None
    }

    def fake_get_alternative_routes():
        return route_candidates

    def fake_retrieve_city_candidates(query, size=10):
        calls["city_query"] = query
        calls["city_size"] = size
        return semantic_city_candidates

    def fake_retrieve_stadium_candidates(query, size=10):
        calls["stadium_query"] = query
        calls["stadium_size"] = size
        return semantic_stadium_candidates

    try:
        candidate_service.get_alternative_routes = fake_get_alternative_routes
        candidate_service.retrieve_city_candidates = (
            fake_retrieve_city_candidates
        )
        candidate_service.retrieve_stadium_candidates = (
            fake_retrieve_stadium_candidates
        )

        mission = {
            "team": "Egypt",
            "travel_style": "Comfort",
            "objective": "Support Egypt"
        }

        candidates = candidate_service.get_candidates(mission)

    finally:
        candidate_service.get_alternative_routes = original_get_alternative_routes
        candidate_service.retrieve_city_candidates = (
            original_retrieve_city_candidates
        )
        candidate_service.retrieve_stadium_candidates = (
            original_retrieve_stadium_candidates
        )

    print(f"Candidates: {candidates}")

    assert calls["city_query"] == "Egypt football atmosphere"
    assert calls["stadium_query"] == "Egypt football atmosphere"
    assert calls["city_size"] == 5
    assert calls["stadium_size"] == 5

    assert any(
        c["candidate_source"] == "route"
        for c in candidates
    ), "Expected route candidates to be returned"

    assert any(
        c["candidate_source"] == "semantic_city"
        for c in candidates
    ), "Expected semantic city candidates to be returned"

    assert any(
        c["candidate_source"] == "semantic_stadium"
        for c in candidates
    ), "Expected semantic stadium candidates to be returned"

    assert len(candidates) > len(route_candidates)

    city_keys = [
        c["city"].lower()
        for c in candidates
    ]
    assert len(city_keys) == len(set(city_keys)), "Expected duplicates removed"

    for candidate in candidates:
        assert "candidate_source" in candidate
        assert candidate["candidate_source"] in {
            "route",
            "semantic_city",
            "semantic_stadium"
        }
        assert "city" in candidate
        assert "match" in candidate
        assert "reason" in candidate
        assert "score" not in candidate
        assert "raw_score" not in candidate
        assert "final_score" not in candidate

    miami = next(
        c for c in candidates
        if c["city"] == "Miami"
    )
    assert miami["candidate_source"] == "semantic_city"
    assert miami["retrieval_score"] == 9.8

    dallas = next(
        c for c in candidates
        if c["city"] == "Dallas"
    )
    assert dallas["candidate_source"] == "semantic_city"
    assert dallas["retrieval_score"] == 8.9

    print(
        "--- V1.5 SEMANTIC CANDIDATE INTEGRATION TEST PASSED SUCCESSFULLY ---"
    )


if __name__ == "__main__":
    run_semantic_integration_test()
