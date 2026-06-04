from datetime import datetime

class BaseRoom:
    def __init__(self, room_name):
        self.room_name = room_name

    def get_status(self):
        return {"status": "inactive"}

    def to_json(self):
        return {
            "room": self.room_name,
            "timestamp": datetime.utcnow().isoformat(),
            "data": self.get_status()
        }

class CoreGRCRoom(BaseRoom):
    def get_status(self):
        # Your existing King V metrics logic goes here
        return {
            "overall_compliance_score": 95, 
            "trust_dividend_index": 88,
            "governing_functions": {
                "steering_direction": {"category_score": 92, "principles": []}
            }
        }

# Define other rooms
class GateFoundationRoom(BaseRoom): def get_status(self): return {"controls_operational": True}
class GougleRoom(BaseRoom): def get_status(self): return {"regulatory_feeds": "Active"}
class IsocRoom(BaseRoom): def get_status(self): return {"standards": "High"}
class SafeguardRoom(BaseRoom): def get_status(self): return {"ethics_status": "Clean"}
class UnicefRoom(BaseRoom): def get_status(self): return {"impact_score": 88}

def get_room_data(room_key):
    rooms = {
        "core": CoreGRCRoom("CORE GRC"),
        "gate": GateFoundationRoom("GATE FOUNDATION"),
        "gougle": GougleRoom("GOUGLE"),
        "isoc": IsocRoom("ISOC"),
        "safeguard": SafeguardRoom("SAFEGUARD"),
        "unicef": UnicefRoom("UNICEF")
    }
    return rooms.get(room_key.lower(), BaseRoom("Unknown")).to_json()

# Helper to check permissions
def check_permission(user_role, required_role):
    roles = {"guest": 1, "auditor": 2, "admin": 3}
    return roles.get(user_role, 0) >= roles.get(required_role, 0)

# Updated room access
def get_room_data(room_key, user_role):
    # Example: CORE GRC requires 'admin' role
    if room_key == "core" and not check_permission(user_role, "admin"):
        return {"error": "Access Denied: Admin role required"}
    
    # Existing logic...
    return rooms.get(room_key).to_json()

import sqlite3

def log_to_ledger(user_id, action, room_key):
    """Writes to your persistent ledger database."""
    conn = sqlite3.connect('compliance_ledger.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_log (timestamp, user_id, action, room)
        VALUES (?, ?, ?, ?)
    ''', (datetime.utcnow().isoformat(), user_id, action, room_key))
    conn.commit()
    conn.close()
