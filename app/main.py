from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

# This creates the database tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

# Database connection helper
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Welcome to Ethical Edge GRC API", "status": "Online"}

@app.get("/frameworks/")
def get_frameworks(db: Session = Depends(get_db)):
    # This pulls King V, ISO, etc. from your database
    return db.query(models.Framework).all()
