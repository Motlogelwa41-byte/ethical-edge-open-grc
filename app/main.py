from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

# Create the tables in the database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Ethical Edge API is LIVE", "version": "1.0"}

@app.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()
