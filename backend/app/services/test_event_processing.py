from app.services.tournament_evaluator import (
    process_latest_event
)

result = process_latest_event("Egypt")

print(result)

if "error" not in result:

    print(
        result["tournament_state"]
    )

    print(
        result["state_history"]
    )