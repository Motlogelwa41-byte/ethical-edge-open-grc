from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

# Initialize the FastAPI app
app = FastAPI(title="Ethical Edge GRC Platform")

# Create the database tables (if they don't exist)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {
        "message": "Ethical Edge GRC API is Online",
        "frameworks": ["King V", "ISO 31000", "Botswana DPA"],
        "status": "Ready for Ingest"
    }

@app.post("/ingest/")
def ingest_document(document_name: str, db: Session = Depends(database.get_db)):
    """
    Step 1 & 2: Ingest & Analyze (Placeholder)
    This endpoint will eventually receive your procurement contracts.
    """
    # Create an audit log entry for the action
    new_log = models.AuditLog(
        action_taken=f"Document Ingested: {document_name}",
        user_id="System AI"
    )
    db.add(new_log)
    db.commit()
    
    return {"status": "Success", "message": f"Document '{document_name}' received and logged."}
