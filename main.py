from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import date
import os

from models import Supplier, Capability, Region, CostModel, PerformanceRating, ContactInfo
from scoring import EvaluationCriteria
from ranking import rank_suppliers

app = FastAPI(title="Supplier Evaluation API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

class SupplierQuery(BaseModel):
    component_type: str = Field(..., description="Type of component required, e.g., 'Widget'")
    volume: int = Field(..., gt=0, description="Required volume (for potential bulk discount logic)")
    region_country: str = Field(..., description="Target country")
    region_state: Optional[str] = Field(None, description="Target state/province")
    target_cost: float = Field(..., gt=0, description="Target unit cost")
    currency: str = Field("USD", min_length=3, max_length=3, description="Currency code")

def get_mock_suppliers() -> List[Supplier]:
    # Generate some mock data
    s1 = Supplier(
        name="Global Manufacturing Ltd",
        contact_info=ContactInfo(email="sales@globalmfg.com"),
        capabilities=[Capability(category="Manufacturing", services=["Widget", "Gadget"])],
        regions=[Region(country="China"), Region(country="Vietnam"), Region(country="India")],
        pricing=[CostModel(item_name="Widget", unit_cost=5.0, currency="USD", bulk_discount_available=True)],
        ratings=[PerformanceRating(period_start=date(2023,1,1), period_end=date(2023,12,31), quality_score=8.5, timeliness_score=8.0, communication_score=7.5)],
        overall_score=8.0
    )
    
    s2 = Supplier(
        name="Local Precision Inc",
        contact_info=ContactInfo(email="info@localprecision.com"),
        capabilities=[Capability(category="Manufacturing", services=["Widget"])],
        regions=[Region(country="USA", state_province="CA")],
        pricing=[CostModel(item_name="Widget", unit_cost=8.0, currency="USD", bulk_discount_available=False)],
        ratings=[PerformanceRating(period_start=date(2023,1,1), period_end=date(2023,12,31), quality_score=9.5, timeliness_score=9.5, communication_score=9.0)],
        overall_score=9.33
    )

    s3 = Supplier(
        name="Budget Parts Co",
        contact_info=ContactInfo(email="sales@budgetparts.com"),
        capabilities=[Capability(category="Manufacturing", services=["Widget"])],
        regions=[Region(country="Mexico")],
        pricing=[CostModel(item_name="Widget", unit_cost=4.5, currency="USD", bulk_discount_available=True)],
        ratings=[PerformanceRating(period_start=date(2023,1,1), period_end=date(2023,12,31), quality_score=6.0, timeliness_score=5.0, communication_score=6.0)],
        overall_score=5.67
    )
    
    return [s1, s2, s3]

@app.post("/rank")
def rank_suppliers_endpoint(query: SupplierQuery):
    suppliers = get_mock_suppliers()
    
    # Map API query to internal criteria
    # Note: We assume 'component_type' implies the required service capability for now
    criteria = EvaluationCriteria(
        required_capabilities=[query.component_type], 
        target_region=Region(country=query.region_country, state_province=query.region_state),
        target_price=query.target_cost,
        target_currency=query.currency,
        required_item=query.component_type # Assuming item name matches component type for simplicity
    )
    
    ranked_results = rank_suppliers(suppliers, criteria)
    
    return ranked_results

@app.get("/suppliers")
def get_all_suppliers():
    suppliers = get_mock_suppliers()
    results = []
    
    for s in suppliers:
        # Calculate derived fields if needed
        s.assess_risk()
        if s.overall_score is None:
            s.calculate_overall_score()
            
        results.append({
            "supplier_name": s.name,
            "fit_score": 0.0, # Placeholder
            "risk_level": s.risk_level,
            "cost_alignment": "N/A", # Placeholder
            "details": s.model_dump()
        })
        
    return results
