def get_dashboard_summary(session, tenant_id):
    query = text("""
        SELECT 
            rg.gate_id, 
            rg.requirement_text, 
            COALESCE(cal.status, 'NOT_STARTED') as status,
            cal.last_updated
        FROM room_gates rg
        LEFT JOIN compliance_audit_log cal ON rg.gate_id = cal.gate_id 
            AND cal.tenant_id = :tenant_id
        WHERE rg.tenant_id = :tenant_id
        ORDER BY rg.order_index
    """)
    return session.execute(query, {"tenant_id": tenant_id}).mappings().all()
