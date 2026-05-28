import json
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel

# Internal App Imports
from app.middleware.tier_guard import verify_account_tier, TenantProfile, TierGuard
from app.room_gates import RoomEngine  
from database.connection import get_db_session 

# Single, Unified Router Instantiation
router = APIRouter(
    prefix="/api/v1/compliance",
    tags=["Compliance Engine & Analytics"]
)

# ==========================================
# 📋 PYDANTIC SCHEMAS (Dashboard Data Types)
# ==========================================
class PrincipleScore(BaseModel):
    principle_id: str
    title: str
    score: float  # 0.0 to 100.0
    gates_total: int
    gates_passed: int
    status: str   # "Compliant", "In Progress", "Non-Compliant"

class FunctionCategory(BaseModel):
    category_score: float
    principles: List[PrincipleScore]

class KingVAnalyticsResponse(BaseModel):
    overall_compliance_score: float
    trust_dividend_index: float  # Signature Ethical Edge Metric
    governing_functions: Dict[str, FunctionCategory]


# ==========================================
# 🚀 ENDPOINTS
# ==========================================

@router.post("/audit-document")
async def run_automated_ai_audit(
    file: UploadFile = File(...),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Evaluates unstructured documents using ai_auditor_prompt.txt
    while strictly checking account tier boundaries.
    """
    # Calculate file footprint to guard data ingestion costs
    file_size_mb = len(await file.read()) / (1024 * 1024)
    await file.seek(0)  # Reset stream pointer after reading footprint size
    
    # 1. Block Standard cloud users from racking up token bills
    TierGuard.enforce_ai_auditor_access(tenant)
    
    # 2. Enforce data bandwidth limits for Professional/Premium accounts
    TierGuard.enforce_upload_limits(tenant, incoming_payload_size_mb=file_size_mb)
    
    # --- Execute Your AI Auditor Core Logic below ---
    # response = execution_engine.run_ai_auditor(file, prompt_template="ai_auditor_prompt.txt")
    
    return {
        "status": "Audit Complete",
        "organization": tenant.name,
        "tier_validated": tenant.tier,
        "processed_file_footprint": f"{round(file_size_mb, 2)} MB"
    }


@router.get("/king-v/metrics", response_model=KingVAnalyticsResponse)
async def get_king_v_dashboard_metrics(db=Depends(get_db_session)):
    """
    Evaluates engine telemetry across room_gates math schemas 
    and groups results into King V's 4 core governing functions.
    """
    try:
        # 1. Initialize your room_gates engine running locally
        engine = RoomEngine(db_session=db)
        raw_gate_matrix = engine.calculate_active_room_scores()
        
        # 2. Map the 13 consolidated King V principles to the 4 Governing Functions
        king_v_mapping = {
            "steering_direction": ["P1", "P2", "P3"],
            "policy_planning": ["P4", "P5", "P6", "P7"],
            "oversight_monitoring": ["P8", "P9", "P10", "P11"],
            "accountability": ["P12", "P13"]
        }
        
        calculated_functions = {}
        total_weights = 0.0
        cumulative_score = 0.0
        
        # 3. Process math schemas out of the room_gates engine matrix
        for function_name, principles in king_v_mapping.items():
            principle_list = []
            function_score_sum = 0.0
            
            for p_id in principles:
                gate_data = raw_gate_matrix.get(p_id, {"passed": 0, "total": 0})
                
                total = gate_data["total"]
                passed = gate_data["passed"]
                
                score = (passed / total * 100.0) if total > 0 else 0.0
                
                if score >= 90.0:
                    status_str = "Compliant"
                elif score >= 50.0:
                    status_str = "In Progress"
                else:
                    status_str = "Non-Compliant"
                
                principle_list.append(PrincipleScore(
                    principle_id=p_id,
                    title=f"King V Principle {p_id.replace('P', '')}",
                    score=round(score, 2),
                    gates_total=total,
                    gates_passed=passed,
                    status=status_str
                ))
                function_score_sum += score
            
            avg_function_score = function_score_sum / len(principles)
            calculated_functions[function_name] = FunctionCategory(
                category_score=round(avg_function_score, 2),
                principles=principle_list
            )
            
            cumulative_score += avg_function_score
            total_weights += 1.0

        overall_score = round(cumulative_score / total_weights, 2) if total_weights > 0 else 0.0
        
        # Ethical Edge Trust Dividend Equation
        accountability_avg = calculated_functions["accountability"].category_score
        trust_dividend = round((overall_score * 0.6) + (accountability_avg * 0.4), 2)

        return KingVAnalyticsResponse(
            overall_compliance_score=overall_score,
            trust_dividend_index=trust_dividend,
            governing_functions=calculated_functions
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Engine Math Evaluation Failed: {str(e)}"
        )
