from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/grc",
    tags=["Normal GRC - RegTech Frameworks"]
)

@router.get("/status")
async def get_grc_status():
    """
    Returns the core status of the corporate RegTech compliance framework.
    """
    return {
        "room": "Normal GRC - RegTech",
        "engine_status": "ACTIVE",
        "governance_code": "King V Alignment Layer Activated",
        "region_scope": "Botswana Nationwide / SADC"
    }

@router.post("/evaluate-risk")
async def evaluate_business_risk(impact: int, probability: int):
    """
    Calculates standard corporate risk thresholds.
    """
    if not (1 <= impact <= 5) or not (1 <= probability <= 5):
        raise HTTPException(status_code=400, detail="Impact and Probability must be scores between 1 and 5.")
    
    inherent_risk_score = impact * probability
    return {
        "calculated_score": inherent_risk_score,
        "risk_category": "CRITICAL" if inherent_risk_score >= 15 else "MEDIUM" if inherent_risk_score >= 8 else "LOW"
    }
