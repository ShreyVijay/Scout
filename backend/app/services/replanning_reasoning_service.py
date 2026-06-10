def generate_reasoning(
    candidate,
    preferences
):
    if not candidate:
        return {
            "decision": None,
            "reasons": []
        }

    contributions = candidate.get(
        "contributions",
        {}
    )

    top_factors = sorted(
        contributions,
        key=lambda k: contributions[k],
        reverse=True
    )

    candidate_source = candidate.get(
        "candidate_source"
    )

    reasons = [
        "Selected by decision engine",
        "Highest final score among candidates"
    ]

    if candidate_source == "route":
        reasons.append(
            "Originated from alternative route retrieval"
        )

        reasons.append(
            "Route candidates receive higher confidence weighting"
        )

    elif candidate_source == "semantic_city":
        reasons.append(
            "Originated from semantic city retrieval"
        )

    elif candidate_source == "semantic_stadium":
        reasons.append(
            "Originated from semantic stadium retrieval"
        )

    score_metadata = candidate.get(
        "score_metadata",
        {}
    )

    if score_metadata.get(
        "budget_penalty_applied"
    ):
        reasons.append(
            "Budget penalty applied"
        )

    return {
        "decision": candidate.get(
            "city"
        ),

        "candidate_source": candidate_source,

        "retrieval_score": candidate.get(
            "retrieval_score"
        ),

        "source_multiplier": score_metadata.get(
            "source_multiplier",
            1.0
        ),

        "final_score": candidate.get(
            "final_score"
        ),

        "top_factors": top_factors,

        "reasons": reasons,

        "contributions": contributions
    }