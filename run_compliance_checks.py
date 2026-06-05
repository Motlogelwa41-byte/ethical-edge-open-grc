import os
from sqlalchemy import text
from app.database.connection import SessionLocal

def run_compliance_checks():
    print("--- 🔍 ETHICAL EDGE: COMPLIANCE AUDIT ENGINE ---")
    session = SessionLocal()
    
    try:
        # 1. Verify Database Connection
        session.execute(text("SELECT 1"))
        print("✅ Database connection established.")

        # 2. Check Table Integrity
        tables = ["compliance_categories", "compliance_principles", "room_gates"]
        for table in tables:
            count = session.execute(text(f"SELECT count(*) FROM {table}")).scalar()
            print(f"📊 Table '{table}' contains {count} records.")
            
            if count == 0:
                print(f"❌ Critical: Table '{table}' is empty. Check ingestion.")
        
        # 3. Validate specific Framework Data
        # Ensure we have data for the tenant we expect
        tenant_id = os.getenv("TARGET_TENANT_ID")
        val_check = session.execute(
            text("SELECT count(*) FROM compliance_categories WHERE tenant_id = :tid"),
            {"tid": tenant_id}
        ).scalar()
        
        if val_check > 0:
            print(f"🚀 SUCCESS: Tenant {tenant_id} has {val_check} categories ingested.")
        else:
            print(f"⚠️ Warning: No data found for Tenant {tenant_id}.")

    except Exception as e:
        print(f"❌ Audit Error: {e}")
    finally:
        session.close()
        print("--- 🏁 Audit Complete ---")

if __name__ == "__main__":
    run_compliance_checks()
