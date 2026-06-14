from sqlalchemy import text
from app.observers.base_observer import BaseControlObserver

class AWSObserver(BaseControlObserver):
    # ... rest of your code ...
    def __init__(self, region="us-east-1"):
        self.region = region

    def sync_to_db(self, session):
        # 1. Logic to check AWS status
        # 2. Database update
        status = "PASS" # Replace with actual AWS check result
        
        session.execute(
            text(
                "UPDATE room_gates "
                "SET validation_type = :status "
                "WHERE gate_id = 'GATE-AWS-01'"
            ),
            {"status": status}
        )
        print(f"☁️ AWS Observer [Region: {self.region}]: {status}")

