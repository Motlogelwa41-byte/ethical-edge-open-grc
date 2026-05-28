from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Optional
import json

# Assuming these exist within your local app architecture
from app.room_gates import RoomEngine  
from database.connection import get_db_session 

router = APIRouter(
    prefix="/api/v1/compliance",
    tags=["King V Analytics"]
)

# --- Pydantic Schemas for Dashboard Type Safety ---
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
    trust_dividend_index: float  # Ethical Edge unique metric
    governing_functions: Dict[str, FunctionCategory]

# --- Core Router Endpoint ---
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
        # This keeps the repository completely aligned with the 2026 King V Framework
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
                # Fetching matching gate math metrics computed by test_multi_room / room_gates logic
                gate_data = raw_gate_matrix.get(p_id, {"passed": 0, "total": 0})
                
                total = gate_data["total"]
                passed = gate_data["passed"]
                
                # Prevent division by zero if a gate or room isn't initialized yet
                score = (passed / total * 100.0) if total > 0 else 0.0
                
                # Determine operational threshold status
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

        # Calculate final aggregated governance engine scores
        overall_score = round(cumulative_score / total_weights, 2) if total_weights > 0 else 0.0
        
        # Ethical Edge Competitive Edge: Calculate your signature "Trust Dividend" metric
        # Derived from algorithmic accountability gates (P11, P12, P13)
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
