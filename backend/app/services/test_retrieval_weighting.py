from app.services.candidate_scoring_service import (
    score_candidate
)

from app.services.replanning_reasoning_service import (
    generate_reasoning
)


def test_route_wins_equal_scores():

    preferences = {
        "atmosphere_weight": 1.0,
        "budget_weight": 0.0,
        "transport_weight": 0.0
    }

    route = {
        "candidate_source": "route",
        "atmosphere_score": 7,
        "budget_score": 0,
        "transport_score": 0,
        "candidate_cost": 0
    }

    semantic = {
        "candidate_source": "semantic_city",
        "atmosphere_score": 7,
        "budget_score": 0,
        "transport_score": 0,
        "candidate_cost": 0
    }

    route = score_candidate(
        route,
        preferences,
        1000
    )

    semantic = score_candidate(
        semantic,
        preferences,
        1000
    )

    assert (
        route["final_score"] >
        semantic["final_score"]
    )

    print(
        "Test 1 passed"
    )


def test_semantic_can_win():

    preferences = {
        "atmosphere_weight": 1.0,
        "budget_weight": 0.0,
        "transport_weight": 0.0
    }

    route = {
        "candidate_source": "route",
        "atmosphere_score": 7,
        "budget_score": 0,
        "transport_score": 0,
        "candidate_cost": 0
    }

    semantic = {
        "candidate_source": "semantic_city",
        "atmosphere_score": 10,
        "budget_score": 0,
        "transport_score": 0,
        "candidate_cost": 0
    }

    route = score_candidate(
        route,
        preferences,
        1000
    )

    semantic = score_candidate(
        semantic,
        preferences,
        1000
    )

    assert (
        semantic["final_score"] >
        route["final_score"]
    )

    print(
        "Test 2 passed"
    )


def test_score_metadata():

    candidate = score_candidate(
        {
            "candidate_source": "route",
            "atmosphere_score": 10,
            "budget_score": 5,
            "transport_score": 5,
            "candidate_cost": 0
        },
        {
            "atmosphere_weight": 0.5,
            "budget_weight": 0.3,
            "transport_weight": 0.2
        },
        1000
    )

    assert (
        "score_metadata"
        in candidate
    )

    assert (
        "source_multiplier"
        in candidate["score_metadata"]
    )

    print(
        "Test 3 passed"
    )


def test_reasoning():

    candidate = score_candidate(
        {
            "city": "Miami",
            "candidate_source": "route",
            "atmosphere_score": 10,
            "budget_score": 5,
            "transport_score": 5,
            "candidate_cost": 0
        },
        {
            "atmosphere_weight": 0.5,
            "budget_weight": 0.3,
            "transport_weight": 0.2
        },
        1000
    )

    reasoning = generate_reasoning(
        candidate,
        {}
    )

    assert (
        "source_multiplier"
        in reasoning
    )

    print(
        "Test 4 passed"
    )


if __name__ == "__main__":

    print(
        "--- STARTING RETRIEVAL WEIGHT TESTS ---"
    )

    test_route_wins_equal_scores()
    test_semantic_can_win()
    test_score_metadata()
    test_reasoning()

    print(
        "--- ALL TESTS PASSED ---"
    )