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
        return {"compliance_score": 95, "active_audits": 2}

class GateFoundationRoom(BaseRoom):
    def get_status(self):
        return {"controls_operational": True, "policy_version": "2.1"}

class GOUGLEけRoom(BaseRoom): # GOUGLE Room
    def get_status(self):
        return {"regulatory_feeds_active": True, "latest_alert": "None"}

class ISOCRoom(BaseRoom):
    def get_status(self):
        return {"standards_compliance": "High", "active_audits": 0}

class SafeguardRoom(BaseRoom):
    def get_status(self):
        return {"ethics_report_status": "Clean", "open_investigations": 0}

class UnicefRoom(BaseRoom):
    def get_status(self):
        return {"impact_score": 88, "grant_compliance": "Pending"}

# Unified access helper for the Dashboard
def get_room_data(room_name):
    rooms = {
        "core": CoreGRCRoom("CORE GRC"),
        "gate": GateFoundationRoom("GATE FOUNDATION"),
        "gougle": GOUGLEけRoom("GOUGLE"),
        "isoc": ISOCRoom("ISOC"),
        "safeguard": SafeguardRoom("SAFEGUARD"),
        "unicef": UnicefRoom("UNICEF")
    }
    room = rooms.get(room_name.lower())
    return room.to_json() if room else {"error": "Room not found"}
