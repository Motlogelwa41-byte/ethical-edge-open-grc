from fastapi import FastAPI
from app.database.base import Base
from app.database.connection import engine

from app.routers import organizations, risks, auth

print(">>> MAIN.PY IS LOADED <<<")
print("AUTH MODULE LOADED")

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ethical Edge Open GRC")

# Register routers
app.include_router(organizations.router)
app.include_router(risks.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "Ethical Edge Open GRC Running"}
