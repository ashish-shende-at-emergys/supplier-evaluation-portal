from typing import List, Optional
from pydantic import BaseModel, Field
from models import Supplier, Region

class EvaluationCriteria(BaseModel):
    required_capabilities: List[str] = Field(..., description="List of required service capabilities")
    target_region: Region = Field(..., description="Target region for the supplier")
    target_price: float = Field(..., gt=0, description="Target price for the item")
    target_currency: str = Field(..., min_length=3, max_length=3, description="Currency of the target price")
    required_item: str = Field(..., description="Item or service to evaluate cost for")

class ScoringResult(BaseModel):
    total_score: float
    cost_alignment: str
    capability_score: float
    cost_score: float
    region_score: float
    performance_score: float

def calculate_fit_score(supplier: Supplier, criteria: EvaluationCriteria) -> ScoringResult:
    # 1. Capability Match (40%)
    supplier_services = set()
    for cap in supplier.capabilities:
        supplier_services.update(cap.services)
    
    required_services = set(criteria.required_capabilities)
    if not required_services:
        capability_score = 100.0
    else:
        intersection = supplier_services.intersection(required_services)
        capability_score = (len(intersection) / len(required_services)) * 100.0

    # 2. Cost Alignment (30%)
    cost_score = 0.0
    cost_alignment = "Low" # Default
    relevant_cost = next((c for c in supplier.pricing if c.item_name == criteria.required_item and c.currency == criteria.target_currency), None)
    
    if relevant_cost:
        if relevant_cost.unit_cost <= criteria.target_price:
            cost_score = 100.0
            cost_alignment = "High"
        elif relevant_cost.unit_cost <= criteria.target_price * 1.10:
            # Within 10% tolerance
            cost_score = 50.0
            cost_alignment = "Medium"
        else:
            # Low alignment
            cost_score = 0.0
            cost_alignment = "Low"
    else:
        # Penalize if item not found or currency mismatch (could implement currency conversion here)
        cost_score = 0.0
        cost_alignment = "None"

    # 3. Region Match (20%)
    region_score = 0.0
    for region in supplier.regions:
        if region.country == criteria.target_region.country:
            # If state is specified in criteria, it must match
            if criteria.target_region.state_province:
                if region.state_province == criteria.target_region.state_province:
                    region_score = 100.0
                    break
            else:
                region_score = 100.0
                break
    
    # 4. Performance Rating (10%)
    # supplier.overall_score is 0-10, scale to 0-100
    # Ensure overall_score is calculated
    if supplier.overall_score is None:
        supplier.calculate_overall_score()
    
    performance_score = (supplier.overall_score or 0.0) * 10.0

    # Weighted Average
    total_score = (
        (capability_score * 0.40) +
        (cost_score * 0.30) +
        (region_score * 0.20) +
        (performance_score * 0.10)
    )

    return ScoringResult(
        total_score=round(total_score, 2),
        cost_alignment=cost_alignment,
        capability_score=capability_score,
        cost_score=cost_score,
        region_score=region_score,
        performance_score=performance_score
    )
