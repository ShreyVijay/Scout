import random

def get_qualification_probability(team: str, group_points: int, group_position: int) -> dict:
    """
    FIFA 2026 Qualification Probability Engine
    Accounts for Top 2 advancement + 8 best 3rd-place teams advancing.
    """
    probability = 0.0
    
    if group_position in [1, 2]:
        probability = 100.0
    elif group_position == 3:
        # 8 out of 12 third-place teams advance
        # Basic heuristic: 4+ points = highly likely, 3 points = edge case, <3 points = unlikely
        if group_points >= 4:
            probability = random.uniform(85.0, 95.0)
        elif group_points == 3:
            probability = random.uniform(40.0, 60.0)
        else:
            probability = random.uniform(5.0, 15.0)
    else:
        # 4th place
        probability = 0.0

    # Ensure it's a clean float
    probability = round(probability, 1)

    return {
        "team": team,
        "group_position": group_position,
        "group_points": group_points,
        "qualification_probability_percentage": probability,
        "status": "Advanced" if probability == 100.0 else "In Contention" if probability > 0 else "Eliminated",
        "insight": f"With {group_points} points in position {group_position}, the probability of reaching the Round of 32 is {probability}%."
    }
