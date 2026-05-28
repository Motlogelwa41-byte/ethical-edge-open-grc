-- 5. CREATE NETWORK TELEMETRY INSTRUMENTATION TABLE
CREATE TABLE IF NOT EXISTS network_telemetry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id VARCHAR(50) NOT NULL,
    district VARCHAR(100) NOT NULL,
    packet_loss_percentage REAL NOT NULL,
    latency_ms REAL NOT NULL,
    bandwidth_mbps REAL NOT NULL,
    manrs_violations_count INTEGER DEFAULT 0,
    solar_battery_voltage REAL,
    solar_panel_output_watts REAL,
    ambient_temperature_celsius REAL,
    local_weather_anomaly VARCHAR(255) DEFAULT 'NORMAL',
    custom_telemetry_payload JSONB,
    captured_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- OPTIMIZE TELEMETRY DATA INDEXES FOR RESEARCH CLUSTER QUERYING
CREATE INDEX IF NOT EXISTS idx_telemetry_node ON network_telemetry(node_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_district ON network_telemetry(district);
CREATE INDEX IF NOT EXISTS idx_telemetry_time ON network_telemetry(captured_at);

-- 6. CREATE CLIMATE RISK ASSESSMENT TRACKING TABLE
CREATE TABLE IF NOT EXISTS climate_risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district VARCHAR(100) NOT NULL,
    hazard_type VARCHAR(100) NOT NULL,
    environmental_hazard_score REAL NOT NULL,
    infrastructure_vulnerability_index REAL NOT NULL,
    calculated_impact_rating VARCHAR(50) NOT NULL,
    modeled_parameters JSONB,
    assessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- OPTIMIZE INDEXES FOR REGIONAL CLIMATE RESEARCH ALGORITHMS
CREATE INDEX IF NOT EXISTS idx_climate_district ON climate_risk_assessments(district);
CREATE INDEX IF NOT EXISTS idx_climate_hazard ON climate_risk_assessments(hazard_type);

-- 7. CREATE VENDOR INTEGRITY AUDIT TRACKING TABLE
CREATE TABLE IF NOT EXISTS vendor_integrity_audits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(100),
    country_of_origin VARCHAR(100) DEFAULT 'Botswana',
    pep_status_verified BOOLEAN DEFAULT FALSE,
    sanction_list_collision BOOLEAN DEFAULT FALSE,
    calculated_integrity_score REAL NOT NULL,
    vetting_decision VARCHAR(50) NOT NULL,
    audit_metadata JSONB,
    audited_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_vendor_name ON vendor_integrity_audits(entity_name);
CREATE INDEX IF NOT EXISTS idx_vendor_decision ON vendor_integrity_audits(vetting_decision);

-- 8. CREATE EPIDEMIC SURVEILLANCE DATA LOOP TABLE
CREATE TABLE IF NOT EXISTS health_facility_surveillance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    facility_name VARCHAR(255) NOT NULL,
    district VARCHAR(100) NOT NULL,
    network_latency_ms REAL NOT NULL,
    data_payload_size_kb REAL NOT NULL,
    reporting_delay_minutes INTEGER NOT NULL,
    surveillance_urgency_tier VARCHAR(50) NOT NULL,
    system_status_summary VARCHAR(255) NOT NULL,
    synchronized_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_facility_name ON health_facility_surveillance(facility_name);
CREATE INDEX IF NOT EXISTS idx_health_district ON health_facility_surveillance(district);

-- 9. CREATE CORE GOVERNANCE AND REGTECH COMPLIANCE TABLE
CREATE TABLE IF NOT EXISTS governance_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    framework_standard VARCHAR(50) DEFAULT 'KING_V',
    transparency_score REAL NOT NULL,
    accountability_index REAL NOT NULL,
    overall_compliance_percentage REAL NOT NULL,
    compliance_status VARCHAR(50) NOT NULL,
    assessment_metadata JSONB,
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gov_company ON governance_assessments(company_name);
CREATE INDEX IF NOT EXISTS idx_gov_standard ON governance_assessments(framework_standard);

-- 10. CREATE AI CYBERSECURITY ANOMALY REPOSITORY TABLE
CREATE TABLE IF NOT EXISTS ai_cyber_threat_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    target_endpoint VARCHAR(255) NOT NULL,
    detected_anomaly_type VARCHAR(100) NOT NULL,
    ai_confidence_score REAL NOT NULL,
    nist_impact_rating VARCHAR(50) NOT NULL,
    model_inference_payload JSONB,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_threat_anomaly ON ai_cyber_threat_logs(detected_anomaly_type);
CREATE INDEX IF NOT EXISTS idx_threat_nist ON ai_cyber_threat_logs(nist_impact_rating);

-- =========================================================================
-- 11. CREATE MASTER COMPLIANCE CATEGORIES TABLE (King V Governing Functions)
-- =========================================================================
CREATE TABLE IF NOT EXISTS compliance_categories (
    category_id VARCHAR(100) PRIMARY KEY,
    display_name VARCHAR(255) NOT NULL,
    weight REAL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================================
-- 12. CREATE MASTER COMPLIANCE PRINCIPLES TABLE (The 13 King V Principles)
-- =========================================================================
CREATE TABLE IF NOT EXISTS compliance_principles (
    principle_id VARCHAR(50) PRIMARY KEY,
    category_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES compliance_categories(category_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_principles_category ON compliance_principles(category_id);

-- =========================================================================
-- 13. CREATE THE CORE OPERATIONAL ROOM GATES CHECKPOINT TABLE
-- =========================================================================
CREATE TABLE IF NOT EXISTS room_gates (
    gate_id VARCHAR(50) PRIMARY KEY,
    principle_id VARCHAR(50) NOT NULL,
    requirement_text TEXT NOT NULL,
    validation_type VARCHAR(50) DEFAULT 'automated', -- 'automated' or 'manual_upload'
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_principle FOREIGN KEY (principle_id) REFERENCES compliance_principles(principle_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_gates_principle ON room_gates(principle_id);

-- =========================================================================
-- 14. CREATE GRANULAR GATE ATTESTATION EXECUTION MATRIX (Links Engine to Assets)
-- =========================================================================
CREATE TABLE IF NOT EXISTS gate_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID NOT NULL, -- Links back to Section 9: governance_assessments.id
    gate_id VARCHAR(50) NOT NULL, -- Links to Section 13: room_gates.gate_id
    is_passed BOOLEAN DEFAULT FALSE,
    telemetry_proof_url TEXT, -- Point of reference proof (or path to logs)
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_assessment FOREIGN KEY (assessment_id) REFERENCES governance_assessments(id) ON DELETE CASCADE,
    CONSTRAINT fk_gate FOREIGN KEY (gate_id) REFERENCES room_gates(gate_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_eval_assessment ON gate_evaluations(assessment_id);
CREATE INDEX IF NOT EXISTS idx_eval_gate ON gate_evaluations(gate_id);


