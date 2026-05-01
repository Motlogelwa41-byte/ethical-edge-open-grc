from database import SessionLocal
from models import Framework

def load_standards():
    db = SessionLocal()
    
    standards = [
        # King V (Governance)
        {"name": "King V", "section": "Principle 1", "description": "The governing body should set the tone and lead ethically and effectively."},
        
        # ISO 27001:2022 (Information Security)
        {"name": "ISO 27001", "section": "A.5.1", "description": "Policies for information security shall be defined and approved by management."},
        
        # NIST CSF 2.0 (Cybersecurity)
        {"name": "NIST CSF 2.0", "section": "GV.OC-01", "description": "The organization’s mission is understood and informs cybersecurity risk management."}
    ]

    for item in standards:
        framework = Framework(**item)
        db.add(framework)
    
    db.commit()
    db.close()
    print("Standards ingested successfully.")

if __name__ == "__main__":
    load_standards()
