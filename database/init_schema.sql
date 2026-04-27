-- ETHICAL EDGE GRC - POSTGRESQL INITIALIZATION SCRIPT

-- Enable UUID extension for secure identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: Risks (Powers "Risk Assessment & Management")
-- Aligned with ISO 31000 & COSO Framework
CREATE TABLE risks (
    risk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(50) NOT NULL, -- Financial, Operational, Strategic, Regulatory
    description TEXT NOT NULL,
    impact_score INT CHECK (impact_score BETWEEN 1 AND 5),
    likelihood_score INT CHECK (likelihood_score BETWEEN 1 AND 5),
    
    -- Inherent risk calculation (Impact x Likelihood)
    risk_rating INT GENERATED ALWAYS AS (impact_score * likelihood_score) STORED,
    
    -- NEW: Cognitive Engine Fields
    control_effectiveness FLOAT DEFAULT 0.0 CHECK (control_effectiveness BETWEEN 0.0 AND 1.0),
    residual_risk FLOAT, 
    
    status VARCHAR(20) DEFAULT 'Identified', -- Identified, Mitigated, Residual
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Compliance_Frameworks (Powers "Compliance Tracking")
CREATE TABLE compliance_frameworks (
    framework_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    framework_name VARCHAR(100) NOT NULL, 
    requirement_text TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Under Review', 
    last_assessment_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Audit_Logs (Powers "Audit & Reporting Tools")
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action_taken TEXT NOT NULL,
    user_id VARCHAR(100) NOT NULL, 
    table_affected VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INITIAL SEED DATA
INSERT INTO compliance_frameworks (framework_name, requirement_text, status) 
VALUES 
('King V', 'Ethical leadership and corporate citizenship requirements', 'Under Review'),
('Botswana DPA', 'Personal data processing and cross-border transfer restrictions', 'Under Review'),
('ISO 31000', 'Risk identification and treatment methodology', 'Compliant');
