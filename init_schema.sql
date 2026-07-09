-- Create database initialization schema script for Ethical Edge Open GRC Engine

-- 1. Create the Historical Event Transaction Log
CREATE TABLE IF NOT EXISTS compliance_audit_log (
    log_id SERIAL PRIMARY KEY,
    gate_id VARCHAR(50),
    event_type VARCHAR(20),
    previous_status VARCHAR(20),
    new_status VARCHAR(20),
    actor VARCHAR(50) DEFAULT 'SYSTEM',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evidence_snapshot JSONB
);

-- 2. Create the Executive Compliance Runs Table
CREATE TABLE IF NOT EXISTS audit_runs (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    attainment_rate DEFAULT 0.0
);

-- 3. Create the Granular Control Findings Table
CREATE TABLE IF NOT EXISTS control_findings (
    id SERIAL PRIMARY KEY,
    audit_run_id INTEGER NOT NULL,
    control_reference VARCHAR(50) NOT NULL,
    control_name VARCHAR(150) NOT NULL,
    framework VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    evidence_payload JSONB,
    CONSTRAINT fk_audit_run
        FOREIGN KEY(audit_run_id) 
        REFERENCES audit_runs(id) 
        ON DELETE CASCADE
);

-- Index targeted search allocations for fast dashboard compilation performance
CREATE INDEX IF NOT EXISTS idx_audit_runs_tenant ON audit_runs(tenant_id);
CREATE INDEX IF NOT EXISTS idx_control_findings_run ON control_findings(audit_run_id);
CREATE INDEX IF NOT EXISTS idx_control_findings_framework ON control_findings(framework);
