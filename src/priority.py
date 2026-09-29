"""Maintenance priority calculation."""


def calculate_priority(severity_score, road_importance, traffic_level, location_risk):
    values = [severity_score, road_importance, traffic_level, location_risk]
    if any(value < 0 or value > 100 for value in values):
        raise ValueError("Priority inputs must be between 0 and 100")

    score = round(
        0.40 * severity_score
        + 0.25 * road_importance
        + 0.20 * traffic_level
        + 0.15 * location_risk,
        2,
    )
    level = "LOW" if score <= 25 else "MEDIUM" if score <= 50 else "HIGH" if score <= 75 else "CRITICAL"
    return score, level


if __name__ == "__main__":
    print(calculate_priority(70, 90, 80, 60))
