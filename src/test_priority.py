from priority import calculate_priority


def run_test(name, severity, road_importance, traffic, location_risk):

    score, level = calculate_priority(
        severity,
        road_importance,
        traffic,
        location_risk
    )

    print(name)
    print("Severity:", severity)
    print("Road Importance:", road_importance)
    print("Traffic:", traffic)
    print("Location Risk:", location_risk)
    print("Priority Score:", round(score, 2))
    print("Priority Level:", level)
    print()


# Test 1: Minor damage on a quiet residential road
run_test(
    "Test 1: Low-risk road",
    20,
    25,
    25,
    20
)


# Test 2: Moderate damage on an important road
run_test(
    "Test 2: Medium-risk road",
    50,
    75,
    50,
    50
)


# Test 3: Serious damage on a busy major road
run_test(
    "Test 3: High-risk road",
    70,
    90,
    80,
    60
)


# Test 4: Very serious damage in a critical location
run_test(
    "Test 4: Critical road damage",
    90,
    100,
    100,
    100
)