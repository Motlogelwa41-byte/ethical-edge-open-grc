cat << 'EOF' > app/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base

# Default local database file location
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/grc_ledger.db")

# Ensure data directory exists
os.makedirs("./data", exist_ok=True)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Programmatically builds all schema tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI Dependency injection provider to handle safe connection pooling."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF
