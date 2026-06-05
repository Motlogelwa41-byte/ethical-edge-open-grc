from app.database.connection import SessionLocal
from sqlalchemy import text

def run_all_checks():
    session = SessionLocal()
    print("🔍 Running System Compliance Checks...")
    
    # Example: Check if we have principles ingested
    result = session.execute(text("SELECT count(*) FROM compliance_principles")).scalar()
    
    if result > 0:
        print(f"✅ Success: {result} compliance principles found in the ledger.")
        print("📊 Running Audit Logic...")
        # Add your audit logic here
    else:
        print("❌ Alert: No compliance principles found. Ingestion failed.")
    
    session.close()

if __name__ == "__main__":
    run_all_checks()
