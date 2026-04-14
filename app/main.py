from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database

# Initialize the Ethical Edge Engine
app = FastAPI(title="Ethical Edge GRC Platform")

# This tells the code to look in the 'templates' folder for your dashboard
templates = Jinja2Templates(directory="templates")

# Create the database tables automatically
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {
        "message": "Ethical Edge GRC API is Online",
        "frameworks": ["King V", "ISO 31000", "Botswana DPA"],
        "status": "Ready for Ingest"
    }

@app.get("/dashboard")
def get_dashboard(request: Request):
    """
    Renders the professional King V Governance Dashboard.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/ingest/")
def ingest_document(document_name: str, db: Session = Depends(database.get_db)):
    # Logs the action in your audit trail
    new_log = models.AuditLog(
        action_taken=f"Document Ingested: {document_name}",
        user_id="System AI"
    )
    db.add(new_log)
    db.commit()
    
    return {"status": "Success", "message": f"Document '{document_name}' received."}
