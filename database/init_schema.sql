-- 0. CORE TENANCY (Required for Multi-tenant SaaS)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 1-10: [KEEP YOUR EXISTING TABLES: network_telemetry, climate_risk_assessments, 
-- vendor_integrity_audits, health_facility_surveillance, governance_assessments, 
-- ai_cyber_threat_logs HERE]

-- 11-13: [KEEP YOUR EXISTING TABLES: compliance_categories, compliance_principles, room_gates HERE]

-- 14. GRANULAR GATE ATTESTATION EXECUTION MATRIX (The Evidence Ledger)
CREATE TABLE IF NOT EXISTS gate_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL, 
    gate_id VARCHAR(50) NOT NULL, 
    is_passed BOOLEAN DEFAULT FALSE,
    telemetry_proof_url TEXT,
    evidence_snapshot JSONB, -- Added for audit-ready snapshots
    auditor_notes TEXT,      -- Added for manual review tracking
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_assessment FOREIGN KEY (assessment_id) REFERENCES governance_assessments(id) ON DELETE CASCADE,
    CONSTRAINT fk_gate FOREIGN KEY (gate_id) REFERENCES room_gates(gate_id) ON DELETE CASCADE
);

-- 15. SECURE AUDIT LOG LEDGER
DROP TABLE IF EXISTS audit_log;
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL, 
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    room VARCHAR(100) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- OPTIMIZE INDEXES
CREATE INDEX IF NOT EXISTS idx_audit_tenant_time ON audit_log(tenant_id, created_at);
CREATE INDEX IF NOT EXISTS idx_eval_assessment ON gate_evaluations(assessment_id);
CREATE INDEX IF NOT EXISTS idx_eval_gate ON gate_evaluations(gate_id);
