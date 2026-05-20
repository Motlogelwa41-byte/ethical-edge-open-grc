-- 1. ENABLE EXTENSION FOR AUTOMATED UNIQUE IDENTIFIERS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. CREATE THE ENTERPRISE USERS MULTI-TENANT TABLE
CREATE TABLE IF NOT EXISTS enterprise_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    company_tenant_id VARCHAR(100) NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'STANDARD_FREE',
    
    -- Feature Flag Access Controls (Monetization Gateways)
    can_access_king_v BOOLEAN DEFAULT TRUE,
    can_access_nist_cyber BOOLEAN DEFAULT FALSE,
    can_access_safeguard BOOLEAN DEFAULT FALSE,
    
    -- Audit & Temporal Compliance Tracking
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. OPTIMIZE INDEXING FOR FAST AUTHENTICATION LOOKUPS
CREATE INDEX IF NOT EXISTS idx_users_email ON enterprise_users(email);
CREATE INDEX IF NOT EXISTS idx_users_tenant ON enterprise_users(company_tenant_id);

-- 4. CREATE A TEMPORAL TRIGGER TO AUTOMATICALLY UPDATE TIMESTAMP ROWS
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_enterprise_users_modtime
BEFORE UPDATE ON enterprise_users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp_column();
