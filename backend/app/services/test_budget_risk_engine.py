from app.services.budget_risk_engine import calculate_budget_risk

def test_risk_engine():
    print("--- Testing Budget Risk Engine ---")

    # Test case 1: 100% remaining -> LOW
    r1 = calculate_budget_risk(1000, 1000)
    assert r1["risk_level"] == "LOW", f"Expected LOW, got {r1['risk_level']}"

    # Test case 2: 75% remaining -> LOW
    r2 = calculate_budget_risk(1000, 750)
    assert r2["risk_level"] == "LOW", f"Expected LOW, got {r2['risk_level']}"

    # Test case 3: 45% remaining -> MEDIUM
    r3 = calculate_budget_risk(1000, 450)
    assert r3["risk_level"] == "MEDIUM", f"Expected MEDIUM, got {r3['risk_level']}"

    # Test case 4: 15% remaining -> HIGH
    r4 = calculate_budget_risk(1000, 150)
    assert r4["risk_level"] == "HIGH", f"Expected HIGH, got {r4['risk_level']}"

    # Boundary test: exactly 50% -> LOW
    r5 = calculate_budget_risk(1000, 500)
    assert r5["risk_level"] == "LOW", f"Expected LOW, got {r5['risk_level']}"

    # Boundary test: exactly 20% -> MEDIUM
    r6 = calculate_budget_risk(1000, 200)
    assert r6["risk_level"] == "MEDIUM", f"Expected MEDIUM, got {r6['risk_level']}"

    # Boundary test: exactly 19.9% -> HIGH
    r7 = calculate_budget_risk(1000, 199)
    assert r7["risk_level"] == "HIGH", f"Expected HIGH, got {r7['risk_level']}"

    print("Risk Engine tests passed successfully!\n")

if __name__ == "__main__":
    test_risk_engine()
