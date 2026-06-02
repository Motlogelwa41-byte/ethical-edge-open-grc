from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict

class RoomEngine:
    def __init__(self, db_session: Session):
        self.session = db_session

    def calculate_active_room_scores(self) -> Dict[str, Dict[str, int]]:
        """Queries the database to calculate total gates vs. passed gates."""
        query = text("""
            SELECT 
                rg.principle_id,
                COUNT(rg.gate_id) as total_gates,
                SUM(CASE WHEN ge.is_passed = TRUE THEN 1 ELSE 0 END) as passed_gates
            FROM room_gates rg
            LEFT JOIN gate_evaluations ge ON rg.gate_id = ge.gate_id
            GROUP BY rg.principle_id;
        """)
        
        result = self.session.execute(query)
        gate_matrix = {f"P{i}": {"passed": 0, "total": 0} for i in range(1, 14)}
        
        for row in result:
            p_id = row.principle_id
            if p_id in gate_matrix:
                gate_matrix[p_id] = {
                    "passed": int(row.passed_gates or 0),
                    "total": int(row.total_gates or 0)
                }
        return gate_matrix

    def evaluate_single_gate_telemetry(self, assessment_id: str, gate_id: str, check_passed: bool, telemetry_url: str = None):
        """Saves or updates an idempotent point-in-time gate evaluation result."""
        # FIX: Targets the compound unique constraint pairing
        query = text("""
            INSERT INTO gate_evaluations (id, assessment_id, gate_id, is_passed, telemetry_proof_url)
            VALUES (uuid_generate_v4(), :assessment_id, :gate_id, :is_passed, :telemetry_proof_url)
            ON CONFLICT (assessment_id, gate_id) DO UPDATE SET
                is_passed = EXCLUDED.is_passed,
                telemetry_proof_url = EXCLUDED.telemetry_proof_url,
                evaluated_at = CURRENT_TIMESTAMP;
        """)
        
        self.session.execute(query, {
            "assessment_id": assessment_id,
            "gate_id": gate_id,
            "is_passed": check_passed,
            "telemetry_proof_url": telemetry_url
        })
        self.session.commit()
