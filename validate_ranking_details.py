from models import Supplier, Capability, Region, CostModel, PerformanceRating, ContactInfo
from scoring import EvaluationCriteria
from ranking import rank_suppliers
from datetime import date

def test_ranking_details():
    s1 = Supplier(
        name="Detail Test Corp",
        contact_info=ContactInfo(email="test@example.com"),
        capabilities=[Capability(category="Manufacturing", services=["CNC"])],
        regions=[Region(country="USA", state_province="CA")],
        pricing=[CostModel(item_name="Widget", unit_cost=100.0, currency="USD")],
        ratings=[PerformanceRating(period_start=date(2023,1,1), period_end=date(2023,12,31), quality_score=9.0, timeliness_score=9.0, communication_score=9.0)],
        overall_score=9.0
    )

    criteria = EvaluationCriteria(
        required_capabilities=["CNC"],
        target_region=Region(country="USA", state_province="CA"),
        target_price=100.0,
        target_currency="USD",
        required_item="Widget"
    )

    ranked = rank_suppliers([s1], criteria)
    
    assert len(ranked) == 1
    result = ranked[0]
    
    print("Checking keys in result...")
    keys = result.keys()
    print(f"Keys found: {list(keys)}")
    
    assert "details" in result, "details key missing from ranking result"
    details = result["details"]
    
    assert details["name"] == "Detail Test Corp"
    assert details["contact_info"]["email"] == "test@example.com"
    
    print("Validation passed: 'details' field is present and correct.")

if __name__ == "__main__":
    test_ranking_details()
