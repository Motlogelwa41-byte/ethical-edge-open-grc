@app.post("/update-risk")
async def update_risk(data: RiskSchema, db: Session = Depends(get_db)):
    try:
        # Perform your business logic
        # ...
        
        # Log the action using the same session
        log_to_ledger(db, current_tenant_id.get(), user_id, "RISK_UPDATED", "CORE_GRC", {"risk_id": data.id})
        
        db.commit() # Commit once at the end
    except Exception:
        db.rollback()
        raise
