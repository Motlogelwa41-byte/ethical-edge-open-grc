from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # This imports the Base we just defined

# Example setup - adjust your database URL as needed
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
