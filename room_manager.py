# room_manager.py
from datetime import datetime

class BaseRoom:
    def __init__(self, room_name):
        self.room_name = room_name

    def get_status(self):
        # Override this in child classes
        return {"status": "inactive"}

    def to_json(self):
        return {
            "room": self.room_name,
            "timestamp": datetime.utcnow().isoformat(),
            "data": self.get_status()
        }

# Define your specific 6 rooms
class CoreGRCRoom(BaseRoom):
    def get_status(self):
        # Logic to query your persistent audit database
        return {"compliance_score": 95, "active_audits": 2}

class GateFoundationRoom(BaseRoom):
    def get_status(self):
        return {"controls_operational": True, "policy_version": "2.1"}

# ... Repeat for GOUGLE, ISOC, SAFEGUARD, UNICEF
