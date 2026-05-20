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


