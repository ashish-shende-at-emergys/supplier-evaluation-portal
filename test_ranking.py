from datetime import date
from models import Supplier, Capability, Region, CostModel, PerformanceRating, ContactInfo
from scoring import EvaluationCriteria
from ranking import rank_suppliers

def create_mock_supplier(name, cost, region_country, region_state, overall_score, unique_countries_count):
    # Helper to create suppliers with specific attributes
    regions = []
    if unique_countries_count == 1:
        regions = [Region(country=region_country, state_province=region_state)]
    else:
        # Add dummy regions to increase county count
        regions = [Region(country=region_country, state_province=region_state)]
        for i in range(unique_countries_count - 1):
             regions.append(Region(country=f"Country{i}", state_province=None))

    supplier = Supplier(
        name=name,
        contact_info=ContactInfo(email=f"contact@{name.replace(' ', '')}.com"),
        capabilities=[Capability(category="Manufacturing", services=["CNC"])],
        regions=regions,
        pricing=[CostModel(item_name="Widget", unit_cost=cost, currency="USD")],
        overall_score=overall_score # Pre-set score to avoid recalculation logic dependence for this test
    )
    return supplier

def test_ranking():
    # 1. Best Match: Good cost, good region, good score, low risk (many regions)
    s1 = create_mock_supplier("Best Corp", cost=100.0, region_country="USA", region_state="CA", overall_score=9.0, unique_countries_count=3)
    
    # 2. Medium Match: Higher cost (Medium align), correct region, okay score
    s2 = create_mock_supplier("Okay Corp", cost=105.0, region_country="USA", region_state="CA", overall_score=7.0, unique_countries_count=2)

    # 3. Poor Match: High cost (Low align), wrong region
    s3 = create_mock_supplier("Bad Corp", cost=120.0, region_country="Mexico", region_state=None, overall_score=4.0, unique_countries_count=1)

    suppliers = [s2, s3, s1] # Unordered

    criteria = EvaluationCriteria(
        required_capabilities=["CNC"],
        target_region=Region(country="USA", state_province="CA"),
        target_price=100.0,
        target_currency="USD",
        required_item="Widget"
    )

    ranked = rank_suppliers(suppliers, criteria)
    
    print("Ranking Results:")
    for r in ranked:
        print(r)

    # Verification
    assert len(ranked) == 3
    
    # Check Order
    assert ranked[0]["supplier_name"] == "Best Corp"
    assert ranked[1]["supplier_name"] == "Okay Corp"
    assert ranked[2]["supplier_name"] == "Bad Corp"

    # Check Attributes for Best Corp
    # Fit Score: 
    # Cap 100 * 0.4 = 40
    # Cost 100 * 0.3 = 30 (High Align)
    # Region 100 * 0.2 = 20
    # Perf 90 * 0.1 = 9
    # Total = 99.0
    assert ranked[0]["fit_score"] == 99.0
    assert ranked[0]["cost_alignment"] == "High"
    assert ranked[0]["risk_level"] == "Low" # 3 regions, 9.0 perf

    # Check Attributes for Okay Corp
    # Cost 105 <= 110 -> Medium Align (50) -> 0.3 * 50 = 15
    # Total ~ 84
    assert ranked[1]["cost_alignment"] == "Medium"
    
    print("All ranking tests passed!")

if __name__ == "__main__":
    test_ranking()
