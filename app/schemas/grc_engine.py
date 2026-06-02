from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from enum import Enum
import uuid

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TreatmentStrategy(str, Enum):
    AVOID = "Avoid"
    MITIGATE = "Mitigate"
    TRANSFER = "Transfer"
    ACCEPT = "Accept"

class FrameworkType(str, Enum):
    ISO27001 = "ISO/IEC 27001:2022"
    ISO31000 = "ISO 31000:2018"
    NIST_CSF = "NIST CSF 2.0"
    BDPA = "Botswana Data Protection Act (BDPA)"
    POPIA = "POPIA (South Africa)"
    KING_V = "King V Corporate Governance"

class ControlMapping(BaseModel):
    framework: FrameworkType
    control_reference: str = Field(..., description="e.g., Annex A 5.15 or BDPA Sec 22")
    control_name: str
    is_automated: bool = False

class RiskCreate(BaseModel):
    title: str = Field(..., max_length=150, description="Clear, concise risk title")
    description: str = Field(..., description="Full threat context scenario")
    likelihood: int = Field(..., ge=1, le=5, description="Scale 1 (Rare) to 5 (Almost Certain)")
    impact: int = Field(..., ge=1, le=5, description="Scale 1 (Insignificant) to 5 (Catastrophic)")
    control_effectiveness: float = Field(
        0.0, ge=0.0, le=1.0, 
        description="Percentage value (0.0 to 1.0) representing how much this control reduces the risk"
    )
    strategy: TreatmentStrategy
    controls: List[ControlMapping] = []

class RiskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    likelihood: int
    impact: int
    inherent_score: int
    residual_score: int
    inherent_level: RiskLevel
    residual_level: RiskLevel
    control_effectiveness: float
    strategy: TreatmentStrategy
    controls: List[ControlMapping]

    @model_validator(mode="before")
    @classmethod
    def calculate_grc_metrics(cls, data: dict) -> dict:
        # 1. Calculate Inherent Risk (Likelihood x Impact)
        likelihood = data.get("likelihood", 1)
        impact = data.get("impact", 1)
        inherent_score = likelihood * impact
        data["inherent_score"] = inherent_score
        
        # Determine Inherent Level based on ISO standard matrix bands
        data["inherent_level"] = cls._get_risk_level(inherent_score)

        # 2. Calculate Residual Risk accounting for Control Effectiveness
        eff = data.get("control_effectiveness", 0.0)
        residual_score = round(inherent_score * (1.0 - eff))
        data["residual_score"] = residual_score
        data["residual_level"] = cls._get_risk_level(residual_score)

        return data

    @staticmethod
    def _get_risk_level(score: int) -> RiskLevel:
        if score >= 20: return RiskLevel.CRITICAL
        if score >= 15: return RiskLevel.HIGH
        if score >= 8:  return RiskLevel.MEDIUM
        return RiskLevel.LOW
