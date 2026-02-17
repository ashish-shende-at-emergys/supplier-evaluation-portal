from datetime import date
from models import Supplier, Capability, Region, CostModel, PerformanceRating, ContactInfo
from scoring import EvaluationCriteria, calculate_fit_score

def test_scoring():
    # Setup Supplier
    supplier = Supplier(
        name="Test Supplier",
        contact_info=ContactInfo(email="test@example.com"),
        capabilities=[
            Capability(category="Manufacturing", services=["CNC", "Injection Molding"])
        ],
        regions=[
            Region(country="USA", state_province="CA")
        ],
        pricing=[
            CostModel(item_name="Widget", unit_cost=100.0, currency="USD")
        ],
        ratings=[
            PerformanceRating(
                period_start=date(2023,1,1), period_end=date(2023,12,31),
                quality_score=9.0, timeliness_score=9.0, communication_score=9.0
            ) # Average 9.0
        ]
    )
    supplier.calculate_overall_score() # Should be 9.0

    # Case 1: Perfect Match
    criteria_perfect = EvaluationCriteria(
        required_capabilities=["CNC", "Injection Molding"],
        target_region=Region(country="USA", state_province="CA"),
        target_price=110.0, # Higher than cost, so full score
        target_currency="USD",
        required_item="Widget"
    )
    
    score_perfect = calculate_fit_score(supplier, criteria_perfect).total_score
    expected_perfect = (100*0.4) + (100*0.3) + (100*0.2) + (90*0.1) # 40 + 30 + 20 + 9 = 99
    print(f"Perfect Match Score: {score_perfect} (Expected: {expected_perfect})")
    assert abs(score_perfect - expected_perfect) < 0.1, f"Expected {expected_perfect}, got {score_perfect}"

    # Case 2: Partial Capability, Higher Cost, Wrong Region
    criteria_mixed = EvaluationCriteria(
        required_capabilities=["CNC", "Welding"], # 50% match
        target_region=Region(country="Canada"), # 0% match
        target_price=80.0, # Cost (100) > Target (80) -> Score 80/100 * 100 = 80
        target_currency="USD",
        required_item="Widget"
    )

    score_mixed = calculate_fit_score(supplier, criteria_mixed).total_score
    
    # Cap: 50% * 0.4 = 20
    # Cost: 100 > 80 * 1.1 (88) -> Score 0 (Low Alignment)
    # Region: 0% * 0.2 = 0
    # Perf: 90% * 0.1 = 9
    # Total: 29
    expected_mixed = 20 + 0 + 0 + 9
    print(f"Mixed Match Score: {score_mixed} (Expected: {expected_mixed})")
    assert abs(score_mixed - expected_mixed) < 0.1, f"Expected {expected_mixed}, got {score_mixed}"

    # Case 3: Cost Logic Testing
    # Target Price = 100
    
    # 3a. High Alignment (Cost 100 <= Target 100) -> Score 100
    criteria_high = EvaluationCriteria(
        required_capabilities=[], target_region=Region(country="USA", state_province="CA"),
        target_price=100.0, target_currency="USD", required_item="Widget"
    )
    score_high = calculate_fit_score(supplier, criteria_high).total_score
    # Cap 100, Cost 100, Region 100, Perf 90
    # 40 + 30 + 20 + 9 = 99
    assert abs(score_high - 99.0) < 0.1, f"Expected 99.0, got {score_high}"

    # 3b. Medium Alignment (Cost 105 <= Target 100 * 1.1) -> Score 50
    # Supplier cost is 100. To test this, we need target price to be slightly less than supplier cost.
    # Supplier Cost = 100. 
    # If Target = 92. Supplier Cost (100) <= 92 * 1.1 (101.2). So Medium.
    criteria_med = EvaluationCriteria(
        required_capabilities=[], target_region=Region(country="USA", state_province="CA"),
        target_price=92.0, target_currency="USD", required_item="Widget"
    )
    score_med = calculate_fit_score(supplier, criteria_med).total_score
    # Cap 100, Cost 50, Region 100, Perf 90
    # 40 + 15 + 20 + 9 = 84
    assert abs(score_med - 84.0) < 0.1, f"Expected 84.0, got {score_med}"

    # 3c. Low Alignment (Cost 100 > Target 90 * 1.1 = 99) -> Score 0
    criteria_low = EvaluationCriteria(
        required_capabilities=[], target_region=Region(country="USA", state_province="CA"),
        target_price=90.0, target_currency="USD", required_item="Widget"
    )
    score_low = calculate_fit_score(supplier, criteria_low).total_score
    # Cap 100, Cost 0, Region 100, Perf 90
    # 40 + 0 + 20 + 9 = 69
    assert abs(score_low - 69.0) < 0.1, f"Expected 69.0, got {score_low}"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_scoring()
