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
