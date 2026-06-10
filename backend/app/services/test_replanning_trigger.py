from app.services.replanning_trigger import (
    needs_replanning
)

print(
    needs_replanning(
        "round_of_16",
        "quarter_final"
    )
)

print(
    needs_replanning(
        "quarter_final",
        "quarter_final"
    )
)

print(
    needs_replanning(
        "semi_final",
        "eliminated"
    )
)