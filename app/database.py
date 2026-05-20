import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. RETRIEVE ENVIRONMENT CORE CONNECTION STRING
# Aligned strictly with our Docker Compose network routing parameters
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://grc_admin:SuperSecurePassword2026!@db:5432/ethical_edge_grc_pool"
)

# 2. INITIALIZE ENGINE WITH CONNECTION POOL MANAGEMENT
# pool_size and max_overflow prevent connections from freezing during peak multi-tenant operations
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Automatically checks and revives dead database connections
)

# 3. CREATE LOCAL SESSION FACTORY
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. DEFINE BASE DECLARATIVE OBJECT FOR SCHEMAS
Base = declarative_base()

# 5. DEPENDENCY INJECTION FUNCTION FOR FASTAPI ROUTES
def get_db():
    """
    Yields a clean database session context per request and safely teardowns
    the connection once the API endpoint execution finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
