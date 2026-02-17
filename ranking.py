from typing import List, Dict, Any
from models import Supplier
from scoring import EvaluationCriteria, calculate_fit_score

def rank_suppliers(suppliers: List[Supplier], criteria: EvaluationCriteria) -> List[Dict[str, Any]]:
    ranked_list = []
    
    for supplier in suppliers:
        # Ensure latest risk assessment
        risk_level = supplier.assess_risk()
        
        # Calculate scores
        scoring_result = calculate_fit_score(supplier, criteria)
        
        ranked_list.append({
            "supplier_name": supplier.name,
            "fit_score": scoring_result.total_score,
            "risk_level": risk_level,
            "cost_alignment": scoring_result.cost_alignment,
            "details": supplier.model_dump()
        })
    
    # Sort by fit_score descending
    ranked_list.sort(key=lambda x: x["fit_score"], reverse=True)
    
    return ranked_list
