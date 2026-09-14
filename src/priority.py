# Maintenance priority calculation


def calculate_priority(
    severity_score,
    road_importance,
    traffic_level,
    location_risk
):

    priority_score = (
        0.40 * severity_score
        + 0.25 * road_importance
        + 0.20 * traffic_level
        + 0.15 * location_risk
    )

    if priority_score <= 25:
        priority_level = "LOW"

    elif priority_score <= 50:
        priority_level = "MEDIUM"

    elif priority_score <= 75:
        priority_level = "HIGH"

    else:
        priority_level = "CRITICAL"

    return priority_score, priority_level


# --------------------------------
# Test
# --------------------------------

severity = 70
road_importance = 90
traffic = 80
location_risk = 60


score, level = calculate_priority(
    severity,
    road_importance,
    traffic,
    location_risk
)


print("Priority Score:",round(score,2))
print("Priority Level:", level)