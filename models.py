from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator


class Capability(BaseModel):
    category: str = Field(..., description="Category of capability, e.g., Manufacturing, Logistics")
    services: List[str] = Field(default_factory=list, description="List of specific services offered")
    certifications: List[str] = Field(default_factory=list, description="List of certifications, e.g., ISO 9001")


class Region(BaseModel):
    country: str = Field(..., description="Country of operation")
    state_province: Optional[str] = Field(None, description="State or province, if applicable")
    service_radius_km: Optional[float] = Field(None, description="Service radius in kilometers")


class CostModel(BaseModel):
    item_name: str = Field(..., description="Name of the item or service")
    unit_cost: float = Field(..., gt=0, description="Cost per unit")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code, e.g., USD")
    bulk_discount_available: bool = Field(False, description="Whether bulk discounts are available")


class PerformanceRating(BaseModel):
    period_start: date = Field(..., description="Start date of the rating period")
    period_end: date = Field(..., description="End date of the rating period")
    quality_score: float = Field(..., ge=0, le=10, description="Quality score (0-10)")
    timeliness_score: float = Field(..., ge=0, le=10, description="Timeliness score (0-10)")
    communication_score: float = Field(..., ge=0, le=10, description="Communication score (0-10)")
    reviewer_comments: Optional[str] = Field(None, description="Optional comments from the reviewer")

    @field_validator('period_end')
    def end_date_must_be_after_start_date(cls, v, info):
        if 'period_start' in info.data and v < info.data['period_start']:
            raise ValueError('period_end must be after period_start')
        return v


class ContactInfo(BaseModel):
    email: EmailStr = Field(..., description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    address: Optional[str] = Field(None, description="Physical address")


class Supplier(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the supplier")
    name: str = Field(..., min_length=1, description="Name of the supplier")
    contact_info: ContactInfo = Field(..., description="Contact information for the supplier")
    capabilities: List[Capability] = Field(default_factory=list, description="List of supplier capabilities")
    regions: List[Region] = Field(default_factory=list, description="Regions where the supplier operates")
    pricing: List[CostModel] = Field(default_factory=list, description="Pricing models for items/services")
    ratings: List[PerformanceRating] = Field(default_factory=list, description="Performance ratings over time")
    overall_score: Optional[float] = Field(None, description="Calculated overall score")
    risk_level: Optional[str] = Field(None, description="Calculated risk level: Low, Medium, High")

    def calculate_overall_score(self):
        if not self.ratings:
            return None
        
        total_score = 0
        for rating in self.ratings:
            # Simple average of the three scores for each rating
            period_average = (rating.quality_score + rating.timeliness_score + rating.communication_score) / 3
            total_score += period_average
        
        self.overall_score = round(total_score / len(self.ratings), 2)
        return self.overall_score

    def assess_risk(self):
        # 1. Performance Risk
        if self.overall_score is None:
            self.calculate_overall_score()
        
        if self.overall_score is None or self.overall_score < 5.0:
            perf_risk = "High"
        elif self.overall_score < 8.0:
            perf_risk = "Medium"
        else:
            perf_risk = "Low"

        # 2. Region Concentration Risk
        unique_countries = {r.country for r in self.regions}
        num_countries = len(unique_countries)

        if num_countries <= 1:
            region_risk = "High"
        elif num_countries == 2:
            region_risk = "Medium"
        else:
            region_risk = "Low"

        # Overall Risk (Max of the two)
        risk_map = {"Low": 1, "Medium": 2, "High": 3}
        max_risk_val = max(risk_map[perf_risk], risk_map[region_risk])
        
        # Reverse map
        inv_risk_map = {1: "Low", 2: "Medium", 3: "High"}
        self.risk_level = inv_risk_map[max_risk_val]
        return self.risk_level
