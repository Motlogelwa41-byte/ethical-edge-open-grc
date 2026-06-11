import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define your database URL (adjust for your specific database, e.g., PostgreSQL or SQLite)
# Example for local SQLite:
DATABASE_URL = "sqlite:///./app.db"

# Or if you use environment variables:
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create the engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} # Needed for SQLite only
)

# Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
