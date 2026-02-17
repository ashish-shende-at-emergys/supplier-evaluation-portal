from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rank_endpoint():
    # 1. Test Case: High Cost Target (Expect Local Precision to win despite high cost due to region/quality?)
    # Query: Widget, Vol 100, Country USA, State CA, Target $10.00
    
    payload = {
        "component_type": "Widget",
        "volume": 100,
        "region_country": "USA",
        "region_state": "CA",
        "target_cost": 10.00,
        "currency": "USD"
    }
    
    response = client.post("/rank", json=payload)
    assert response.status_code == 200
    results = response.json()
    
    print("API Response:", results)
    
    assert len(results) == 3
    # Local Precision (USA, CA) should be top due to Region Match (20%) + High Cost Align (100% since 8 < 10) + High Perf (9.33)
    assert results[0]["supplier_name"] == "Local Precision Inc"
    assert results[0]["cost_alignment"] == "High"

def test_rank_endpoint_low_cost():
    # 2. Test Case: Low Cost Target
    # Query: Widget, Vol 1000, Country China, Target $5.00
    
    payload = {
        "component_type": "Widget",
        "volume": 1000,
        "region_country": "China",
        "region_state": None,
        "target_cost": 5.00,
        "currency": "USD"
    }
    
    response = client.post("/rank", json=payload)
    assert response.status_code == 200
    results = response.json()
    
    # Global Manufacturing (China) -> Region Match, Cost Match (5.0 <= 5.0).
    # Budget Parts (Mexico) -> Region Mismatch. Cost Match (4.5 <= 5.0).
    
    assert results[0]["supplier_name"] == "Global Manufacturing Ltd"
    assert results[0]["cost_alignment"] == "High"

if __name__ == "__main__":
    test_rank_endpoint()
    test_rank_endpoint_low_cost()
    print("API Tests Passed!")
