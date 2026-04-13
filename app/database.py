from sqlalchemy import create_all, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. Define where the database lives
# For now, it creates a local 'ethical_edge.db' file so you can test easily
SQLALCHEMY_DATABASE_URL = "sqlite:///./ethical_edge.db"

# 2. Create the Engine (The Connection)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a Session (The 'Borrowing' system)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base (The 'Blueprint' foundation)
Base = declarative_base()

# 5. The get_db function (Used by main.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
