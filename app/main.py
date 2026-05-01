from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Ethical Edge Open GRC Running"}

@app.get("/frameworks/")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()
