"""
Ethical Edge Open GRC Engine - Cognitive Extension Module
File: climate_risk_manager.py
Objective: Ingest climate metrics, calculate facility vulnerability indices, 
           and compute child impact metrics for schools and health facilities.
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field

# ==========================================
# 1. DATA SANITIZATION PIPELINE
# ==========================================

def sanitize_environmental_payload(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes incoming local community climate telemetry payloads.
    Strips explicit administrative names, removes granular coordinates, 
    and applies regional boundary mapping to ensure non-identifiability.
    """
    # Create a local copy to preserve the original payload inputs safely
    sanitized_source = raw_payload.copy()
    
    # Enforce strict field isolation: remove specific point coordinates or local names
    sanitized_source.pop("exact_latitude", None)
    sanitized_source.pop("exact_longitude", None)
    sanitized_source.pop("school_or_facility_name", None)
    sanitized_source.pop("facility_name", None)  # Broaden stripping target to match master pipelines
    
    # Generate a cryptographically secure, non-invertible token for the region
    regional_salt = sanitized_source.get("regional_catchment_id", "SADC-ZONE-DEFAULT")
    secure_token = uuid.uuid5(uuid.NAMESPACE_DNS, f"{regional_salt}-2026-climate")
    
    sanitized_payload = {
        "telemetry_id": str(secure_token),
        "coarse_bounding_zone": sanitized_source.get("normalized_district_code", "SADC-REG-01"),
        "environmental_metrics": {
            "heat_index_celsius": float(sanitized_source.get("ambient_temp", sanitized_source.get("current_hazard_severity_score", 0.5) * 40)),
            "pm25_concentration": float(sanitized_source.get("particulate_matter", 0.0)),
            "uv_index": float(sanitized_source.get("uv_exposure", 0.0))
        },
        "vulnerability_context": {
            "aggregated_demographic_density_score": sanitized_source.get("density_bracket"),
            "infrastructure_resilience_class": sanitized_source.get("resilience_rating")
        }
    }
    return sanitized_payload


# ==========================================
# 2. DATA CONTRACTS (PYDANTIC SCHEMAS)
# ==========================================

class ClimateTelemetryInput(BaseModel):
    """Validates raw incoming weather or climate sensor metrics."""
    facility_id: str = Field(..., example="FAC-BWP-052")
    facility_type: str = Field(..., example="school", description="Must be 'school' or 'clinic'")
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    temperature_celsius: float = Field(..., example=41.5)
    flood_water_level_meters: float = Field(..., example=0.2)
    drought_index_spi: float = Field(..., example=-1.8, description="Standardized Precipitation Index")
    active_power_outage: bool = Field(default=False)

class ResilienceParameters(BaseModel):
    """Validates local operational infrastructure variables."""
    student_or_patient_count: int = Field(..., example=450)
    has_active_cooling: bool = Field(default=False)
    has_clean_water_reserve: bool = Field(default=True)
    has_offgrid_power_backup: bool = Field(default=False)


# ==========================================
# 3. THE COGNITIVE RISK COMPENSATOR ENGINE
# ==========================================

class ClimateRiskManager:
    """Processes incoming data feeds and generates concrete GRC audit tracking."""
    
    @staticmethod
    def calculate_hazard_severity(telemetry: ClimateTelemetryInput) -> Dict[str, Any]:
        """
        Translates raw physical parameters into categorical risk thresholds.
        Moves data from metric visualization to risk governance.
        """
        scores = {"heatwave": 0.0, "flood": 0.0, "drought": 0.0}
        
        # Heatwave scoring threshold logic
        if telemetry.temperature_celsius >= 40.0:
            scores["heatwave"] = 1.0  # Critical
        elif telemetry.temperature_celsius >= 35.0:
            scores["heatwave"] = 0.6  # High
        else:
            scores["heatwave"] = 0.2  # Low
            
        # Flood level threshold logic
        if telemetry.flood_water_level_meters >= 0.5:
            scores["flood"] = 1.0
        elif telemetry.flood_water_level_meters > 0.0:
            scores["flood"] = 0.5
            
        # Drought stress calculation (negative SPI indices indicate severe dry spans)
        if telemetry.drought_index_spi <= -1.5:
            scores["drought"] = 0.9
            
        # Identify absolute highest active threat matrix vector
        dominant_hazard = max(scores, key=scores.get)
        return {
            "hazard_scores": scores,
            "dominant_hazard_type": dominant_hazard,
            "raw_severity_value": scores[dominant_hazard]
        }

    @classmethod
    def evaluate_facility_governance_score(
        cls, telemetry: ClimateTelemetryInput, infrastructure: ResilienceParameters
    ) -> Dict[str, Any]:
        """
        Combines hazard severity with local vulnerability variables.
        Outputs an actionable GRC preparedness tier score (0.0 to 1.0).
        """
        hazard_analysis = cls.calculate_hazard_severity(telemetry)
        base_severity = hazard_analysis["raw_severity_value"]
        dominant_type = hazard_analysis["dominant_hazard_type"]
        
        # Start matching data vectors against infrastructural defenses
        vulnerability_modifier = 1.0
        
        if dominant_type == "heatwave" and infrastructure.has_active_cooling:
            vulnerability_modifier -= 0.4  # Risk drops if infrastructure is hardened
            
        if dominant_type == "flood" and infrastructure.has_offgrid_power_backup:
            vulnerability_modifier -= 0.2  
            
        if telemetry.active_power_outage and not infrastructure.has_offgrid_power_backup:
            vulnerability_modifier += 0.3  # Risk compounds dynamically upon grid failures

        # Boundary controls to restrict total risk limits
        final_risk_coefficient = min(max(base_severity * vulnerability_modifier, 0.0), 1.0)
        
        # Calculate Child / Vulnerable Group Impact Factor
        child_impact_weight = "stable_baseline"
        if final_risk_coefficient >= 0.7 and infrastructure.student_or_patient_count > 200:
            child_impact_weight = "critical_escalation"
        elif final_risk_coefficient >= 0.4:
            child_impact_weight = "medium_monitoring"

        # Explicitly enforce clean-room anonymization output contracts to avoid assertion PII leaks
        anonymized_id = f"ANON-FAC-{uuid.uuid5(uuid.NAMESPACE_DNS, telemetry.facility_id).hex[:8].upper()}"

        return {
            "anonymized_id": anonymized_id,
            "calculated_at": datetime.utcnow().isoformat(),
            "target_vulnerability_index": round(final_risk_coefficient, 2),
            "dominant_threat_vector": dominant_type,
            "impact_mitigation_classification": child_impact_weight,
            "system_recommendation": cls.generate_remediation_text(dominant_type, final_risk_coefficient)
        }

    @staticmethod
    def generate_remediation_text(hazard: str, score: float) -> str:
        """Outputs explicit, audit-ready governance actions based on risk tiers."""
        if score >= 0.7:
            if hazard == "heatwave":
                return "CRITICAL: Trigger early school closure protocols or relocate clinical activities to primary thermal shelters."
            if hazard == "flood":
                return "CRITICAL: Deploy emergency backup power blocks. Activate decentralized offline administrative data staging."
        if score >= 0.4:
            return "WARNING: Initiate structural monitoring updates. Verify local clean water reservoirs are filled."
        return "STABLE: System operating within acceptable adaptive baseline constraints."
