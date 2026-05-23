import json
import os

def analyze_governance_friction(audit_domain: str, process_delay_days: int, active_controls_count: int) -> dict:
    """Calculates operational friction scores against King V risk governance standards."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    checklist_path = os.path.join(base_dir, 'data', 'king_v_checklist.json')
    
    baseline_delay_weight = 2.5
    control_overhead_multiplier = 1.2
    raw_friction = (process_delay_days * baseline_delay_weight) + (active_controls_count * control_overhead_multiplier)
    friction_score = min(round(raw_friction, 2), 100.0)
    
    try:
        if not os.path.exists(checklist_path):
            return {"status": "Error", "message": "King V governance data configuration missing."}
            
        with open(checklist_path, 'r') as f:
            principles = json.load(f)
            
        matched_principle = next(
            (p for p in principles if p["name"].lower() in audit_domain.lower() or audit_domain.lower() in p["name"].lower()),
            principles[0] if principles else {"name": "General Governance"}
        )
        
        status = "🚨 HIGH FRICTION: Optimization Required" if friction_score > 50.0 else "✅ STREAMLINED: Optimal Velocity"
        
        return {
            "status": "Gates Foundation Due Diligence Analysis Complete",
            "evaluated_domain": audit_domain,
            "calculated_friction_score": friction_score,
            "operational_status": status,
            "mapped_king_v_metric": matched_principle
        }
    except Exception as e:
        return {"error": f"Gates Room logic validation failed: {str(e)}"}
