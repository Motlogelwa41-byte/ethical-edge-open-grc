from app.database import SessionLocal
from app.models import Framework

def load_data():
    db = SessionLocal()
    # Check if data exists
    if db.query(Framework).first():
        print("Frameworks already exist in database.")
        return

    data = [
        Framework(name="King V", section="Principle 1", description="Ethical leadership and corporate citizenship."),
        Framework(name="ISO 27001", section="A.5.1", description="Policies for information security."),
        Framework(name="NIST CSF 2.0", section="GV.OC-01", description="Organizational mission and risk management.")
    ]
    db.add_all(data)
    db.commit()
    db.close()
    print("Phase 1 Complete: GRC Frameworks Ingested.")

if __name__ == "__main__":
    load_data()
