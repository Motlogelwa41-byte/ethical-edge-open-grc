import time
from app.database.connection import SessionLocal
from sqlalchemy import text

def continuous_observation_loop():
    print("👀 Observer Service Started...")
    while True:
        session = SessionLocal()
        # Logic: Pull from AWS/System, verify against Gate, update DB
        # E.g., if SystemFileObserver().check_status() == True:
        #    session.execute(text("UPDATE room_gates SET status='PASS' WHERE ..."))
        
        print("🔍 Scanning infrastructure for compliance drift...")
        session.commit()
        session.close()
        time.sleep(60) # Wait 1 minute before next scan

if __name__ == "__main__":
    continuous_observation_loop()
