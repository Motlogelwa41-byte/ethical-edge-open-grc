from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

router = APIRouter(
    prefix="/isoc",
    tags=["ISOC Challenge - Connectivity & Trust Infrastructure"]
)

# 1. NETWORK RESILIENCE AND MANRS INTAKE SCHEMAS
class CommunityNetworkAuditInput(BaseModel):
    network_identifier: str = Field(..., example="Kgalagadi_Community_Mesh_04")
    wpa3_encryption_enforced: bool = Field(..., description="Validates last-mile wireless encryption tier")
    manrs_anti_spoofing_active: bool = Field(..., description="MANRS Action 2: Filtering to prevent spoofed traffic")
    manrs_global_coordination_ready: bool = Field(..., description="MANRS Action 4: Up-to-date contact info in peering DBs")
    average_latency_ms: float = Field(..., ge=0.0)
    packet_loss_percentage: float = Field(..., ge=0.0, le=100.0)

# 2. APPLICATION LOGIC ENDPOINTS
@router.get("/status")
async def get_isoc_room_status():
    """
    Returns the real-time operational state of the ISOC network trust engine.
    """
    return {
        "room": "Internet Society (ISOC) Challenge Room",
        "engine_status": "ACTIVE",
        "focus": "Community Network Resilience & Global Routing Integrity",
        "core_framework": "MANRS (Mutually Assured Norms for Routing Security) Core Pillars",
        "operational_state": "PRODUCTION_READY"
    }

@router.post("/audit-network")
async def audit_network_trust_infrastructure(network: CommunityNetworkAuditInput):
    """
    Evaluates local infrastructure metrics against MANRS global routing safety norms.
    """
    # Evaluate explicit MANRS alignment vectors
    manrs_score = 0
    if network.manrs_anti_spoofing_active:
        manrs_score += 50
    if network.manrs_global_coordination_ready:
        manrs_score += 50

    # Determine structural connectivity performance
    is_performant = network.average_latency_ms <= 150.0 and network.packet_loss_percentage <= 2.0
    
    # Establish overall Network Trust Status
    if manrs_score == 100 and network.wpa3_encryption_enforced and is_performant:
        trust_tier = "SECURE & RESILIENT INFRASTRUCTURE"
        clearance_status = "APPROVED_FOR_ISOC_CONSORTIUM"
    elif manrs_score >= 50:
        trust_tier = "PARTIALLY COMPLIANT - ROUTING SECURITY REFORMS REQUIRED"
        clearance_status = "CONDITIONAL_HOLD"
    else:
        trust_tier = "CRITICAL NON-COMPLIANCE - VULNERABLE TO SPOOFING/INTERCEPTION"
        clearance_status = "REJECTED_GOVERNANCE_FAIL"

    return {
        "evaluation_timestamp": datetime.utcnow(),
        "network_node": network.network_identifier,
        "performance_telemetry": {
            "latency_status": "OPTIMAL" if network.average_latency_ms <= 100.0 else "ACCEPTABLE",
            "packet_loss_integrity": f"{100.0 - network.packet_loss_percentage}%"
        },
        "compliance_matrix": {
            "manrs_routing_score": f"{manrs_score}/100",
            "last_mile_encryption_secured": network.wpa3_encryption_enforced,
            "overall_trust_tier": trust_tier
        },
        "isoc_funding_eligibility": clearance_status
    }
