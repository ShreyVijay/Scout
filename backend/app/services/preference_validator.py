def normalize_weights(atmosphere, budget, transport):
    """
    Normalizes three weight values so they sum exactly to 1.0.
    If all weights are zero, distributes evenly.
    """
    total = atmosphere + budget + transport
    if total == 0:
        return (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)

    norm_atm = atmosphere / total
    norm_bud = budget / total
    norm_tr = transport / total

    # Ensure exact sum = 1.0 by adjusting last weight
    norm_tr = 1.0 - norm_atm - norm_bud

    return (norm_atm, norm_bud, norm_tr)
