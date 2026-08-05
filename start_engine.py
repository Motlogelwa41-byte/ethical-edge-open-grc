import json
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Internal App Imports
from app.middleware.tier_guard import verify_account_tier, TenantProfile, TierGuard
from app.room_gates import RoomEngine  
from app.utils.llm_client import AIAuditorClient
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
    assessment_id: str = Form(...),
    gate_id: str = Form(...),
    requirement_text: str = Form(...),
    tenant: TenantProfile = Depends(verify_account_tier),
    db: Session = Depends(get_db_session)
):
    """
    Ingests unstructured corporate files, evaluates compliance using Gemini 2.5
    under strict tier guardrails, and records the gate assessment telemetry.
    """
    # Read file content safely to calculate the file's scale footprint
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    await file.seek(0)  # Reset stream pointer
    
    # 1. Enforce tier rules to protect backend API margins
    TierGuard.enforce_ai_auditor_access(tenant)
    TierGuard.enforce_upload_limits(tenant, incoming_payload_size_mb=file_size_mb)
    
    # 2. Extract textual data safely, handling varied document encodings
    try:
        document_text = content.decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unable to read file content encoding. Please upload a valid text document: {str(e)}"
        )
        
    if not document_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded verification document is empty."
        )

    # 3. Initialize and run the Gemini 2.5 Audit Engine
    try:
        auditor = AIAuditorClient()
        audit_result = await auditor.execute_document_audit(
            gate_id=gate_id,
            requirement_text=requirement_text,
            document_text=document_text
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Downstream compliance evaluation error: {str(e)}"
        )

    # 4. Initialize RoomEngine to commit the audit result into PostgreSQL (Table 14)
    try:
        engine = RoomEngine(db_session=db)
        
        # Determine the local reference path to act as the audit trace
        mock_telemetry_url = f"/uploads/proof/{file.filename}"
        
        engine.evaluate_single_gate_telemetry(
            assessment_id=assessment_id,
            gate_id=gate_id,
            check_passed=audit_result.get("is_passed", False),
            telemetry_url=mock_telemetry_url
        )
    except Exception as db_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Relational storage transaction failed: {str(db_err)}"
        )
    
    return {
        "status": "Audit Complete",
        "organization": tenant.name,
        "tier_validated": tenant.tier,
        "processed_file_footprint": f"{round(file_size_mb, 2)} MB",
        "evaluation_metrics": audit_result
    }


@router.get("/king-v/metrics", response_model=KingVAnalyticsResponse)
async def get_king_v_dashboard_metrics(db: Session = Depends(get_db_session)):
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

from room_manager import get_room_data

@router.get('/api/room/{room_key}')
async def api_room(room_key: str):
    return await get_room_data(room_key)
