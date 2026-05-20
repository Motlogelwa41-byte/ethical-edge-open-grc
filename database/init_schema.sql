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
