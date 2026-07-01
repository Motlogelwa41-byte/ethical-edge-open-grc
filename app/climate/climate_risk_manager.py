from typing import Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ClimatePayload(BaseModel):
    location: str
    temperature_celsius: float = Field(..., alias="temp_c")
    flood_risk_level: str  # e.g., "Low", "Medium", "High"
    drought_index: float   # e.g., 0.0 to 5.0 scale
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

class ClimateRiskManager:
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    def ingest_api_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validated_data = ClimatePayload(**data)
            evaluation_packet = self._map_to_compliance_schema(validated_data)
            
            if self.orchestrator:
                compliance_result = self.orchestrator.route_to_rooms(evaluation_packet)
                return {
                    "status": "success",
                    "processed_at": datetime.utcnow().isoformat(),
                    "compliance_output": compliance_result
                }
                
            return {
                "status": "validated_and_mapped",
                "processed_at": datetime.utcnow().isoformat(),
                "data": evaluation_packet
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def _map_to_compliance_schema(self, payload: ClimatePayload) -> Dict[str, Any]:
        is_critical_temp = payload.temperature_celsius > 40.0
        is_high_flood = payload.flood_risk_level.upper() in ["HIGH", "CRITICAL"]
        
        return {
            "domain": "Environmental_Climate_Risk",
            "target_location": payload.location,
            "assessment_meta": {
                "temperature": payload.temperature_celsius,
                "flood_level": payload.flood_risk_level,
                "drought_score": payload.drought_index,
                "timestamp": payload.recorded_at.isoformat()
            },
            "triggers": {
                "business_continuity_alert": is_critical_temp or is_high_flood,
                "infrastructure_risk_score": round((payload.drought_index / 5.0) * 100, 2)
            }
        }
