@remediation_router.post("/remediate/{control_reference}")
async def apply_remediation(
    control_reference: str,
    db: Session = Depends(get_db), # Ensure this session is injected
    tenant: TenantProfile = Depends(verify_account_tier)
):
    engine = RemediationEngine(tenant_id=tenant.token)
    
    # 1. Execute the fix
    result = engine.execute_fix(control_reference)
    
    if result.get("status") == "SUCCESS":
        # 2. LOG THE AUDIT EVENT (This is your hook)
        from app.services.audit_service import AuditService
        
        AuditService.log_event(
            db=db, 
            gate_id=control_reference, 
            event_type="REMEDIATION_TRIGGERED",
            prev="FAILED",
            new="PASSED"
        )
        
        return {"message": "Remediation applied and audited.", "status": "fixed"}
    
    # ... handle failures ...
