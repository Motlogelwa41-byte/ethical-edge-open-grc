-- 1. Ensure Multi-Tenancy (Base structure)
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Consolidate Audit Log (Fixed)
DROP TABLE IF EXISTS audit_log;
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL, 
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    room VARCHAR(100) NOT NULL,
    metadata JSONB, -- Changed from TEXT to JSONB for better auditing
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);

-- 3. Standardize Evidence Ledger (Updating gate_evaluations)
-- This now captures the "Result" + "Proof" for every compliance check
ALTER TABLE gate_evaluations 
ADD COLUMN IF NOT EXISTS evidence_snapshot JSONB;

ALTER TABLE gate_evaluations 
ADD COLUMN IF NOT EXISTS auditor_notes TEXT;

