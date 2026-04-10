import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For local development, we use a standard PostgreSQL URL format:
# postgresql://[user]:[password]@[host]:[port]/[database_name]
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ethical_edge_db")

# The Engine is the starting point for any SQLAlchemy application
engine = create_engine(DATABASE_URL)

# This is the session factory that our API will use for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
