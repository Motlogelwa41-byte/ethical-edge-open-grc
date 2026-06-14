from app.database.connection import SessionLocal
from sqlalchemy import text

try:
    db = SessionLocal()
    # Query to count the gates
    results = db.execute(text("SELECT count(*) FROM room_gates")).scalar()
    print(f"Total gates found in database: {results}")
except Exception as e:
    print(f"Database error: {e}")
finally:
    db.close()
