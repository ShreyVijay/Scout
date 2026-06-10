from app.services.retrieval_weight_service import (
    get_source_multiplier
)


def score_candidate(
    candidate,
    preferences,
    remaining_budget
):
    atmosphere_score = float(
        candidate.get(
            "atmosphere_score",
            0.0
        )
    )

    budget_score = float(
        candidate.get(
            "budget_score",
            0.0
        )
    )

    transport_score = float(
        candidate.get(
            "transport_score",
            0.0
        )
    )

    atmosphere_weight = float(
        preferences.get(
            "atmosphere_weight",
            0.0
        )
    )

    budget_weight = float(
        preferences.get(
            "budget_weight",
            0.0
        )
    )

    transport_weight = float(
        preferences.get(
            "transport_weight",
            0.0
        )
    )

    atmosphere_contrib = (
        atmosphere_score *
        atmosphere_weight
    )

    budget_contrib = (
        budget_score *
        budget_weight
    )

    transport_contrib = (
        transport_score *
        transport_weight
    )

    raw_score = (
        atmosphere_contrib +
        budget_contrib +
        transport_contrib
    )

    source_multiplier = (
        get_source_multiplier(
            candidate.get(
                "candidate_source"
            )
        )
    )

    final_score = (
        raw_score *
        source_multiplier
    )

    candidate_cost = float(
        candidate.get(
            "candidate_cost",
            0.0
        )
    )

    penalty_applied = False
    penalty_ratio = 1.0

    if remaining_budget <= 0:

        penalty_applied = True

        penalty_ratio = (
            candidate_cost / 1.0
            if candidate_cost > 0
            else 1.0
        )

        final_score = (
            final_score /
            penalty_ratio
        )

    elif candidate_cost > remaining_budget:

        penalty_applied = True

        penalty_ratio = (
            candidate_cost /
            remaining_budget
        )

        final_score = (
            final_score /
            penalty_ratio
        )

    scored = candidate.copy()

    scored["raw_score"] = raw_score
    scored["final_score"] = final_score

    scored["contributions"] = {
        "atmosphere": atmosphere_contrib,
        "budget": budget_contrib,
        "transport": transport_contrib
    }

    scored["score_metadata"] = {
        "raw_score": raw_score,
        "source_multiplier": source_multiplier,
        "budget_penalty_applied": penalty_applied,
        "penalty_ratio": penalty_ratio
    }

    return scored


def score_candidates(
    candidates,
    preferences,
    remaining_budget
):
    return [
        score_candidate(
            candidate,
            preferences,
            remaining_budget
        )
        for candidate in candidates
    ]