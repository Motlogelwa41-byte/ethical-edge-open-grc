from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import os

# Database URL - Ensure this is set in your environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/grc_db")

# Create engine with a connection pool to manage concurrent tenant requests
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,       # Adjust based on expected concurrent tenants
    max_overflow=10
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency generator for FastAPI. 
    Provides a scoped session and ensures it closes to prevent leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
