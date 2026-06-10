def build_recommendation_audit(
    rankings
):
    if not rankings:
        return {
            "winner": None,
            "audit": []
        }

    audit = []

    for candidate in rankings:

        contributions = candidate.get(
            "contributions",
            {}
        )

        atmosphere = contributions.get(
            "atmosphere",
            0
        )

        budget = contributions.get(
            "budget",
            0
        )

        transport = contributions.get(
            "transport",
            0
        )

        top_factor = max(
            [
                (
                    "atmosphere",
                    atmosphere
                ),
                (
                    "budget",
                    budget
                ),
                (
                    "transport",
                    transport
                )
            ],
            key=lambda x: x[1]
        )

        reason = (
            f"Top factor: "
            f"{top_factor[0]} "
            f"({round(top_factor[1], 2)})"
        )

        audit.append(
            {
                "city": candidate.get(
                    "city"
                ),

                "rank": candidate.get(
                    "rank"
                ),

                "final_score": candidate.get(
                    "final_score"
                ),

                "candidate_source": candidate.get(
                    "candidate_source"
                ),

                "reason": reason,

                "audit_details": {
                    "atmosphere": atmosphere,
                    "budget": budget,
                    "transport": transport
                }
            }
        )

    return {
        "winner": rankings[0].get(
            "city"
        ),

        "audit": audit
    }