import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Import local modules using relative imports
from . import models, database

load_dotenv()

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "Ethical Edge API Active"}

@app.get("/frameworks/")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()

@app.post("/organizations/")
def create_org(name: str, reg_number: str, db: Session = Depends(get_db)):
    new_org = models.Organization(name=name, reg_number=reg_number)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org
