import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import Base # Ensure your models are imported

class BaseRoom:
    def __init__(self, room_name: str, session: Session, tenant_id: str):
        self.room_name = room_name
        self.session = session
        self.tenant_id = tenant_id

    async def get_status(self):
        return {"status": "inactive"}

    async def to_json(self):
        return {
            "room": self.room_name,
            "timestamp": datetime.utcnow().isoformat(),
            "data": await self.get_status()
        }

class CoreGRCRoom(BaseRoom):
    async def get_status(self):
        # The 'before_compile' filter in base.py will automatically 
        # add "WHERE tenant_id = :tid" to any query here!
        return {
            "overall_compliance_score": 95,
            "tenant_context": self.tenant_id
        }

# Room Registry Factory
def get_room_instance(room_key: str, session: Session, tenant_id: str):
    registry = {
        "core": CoreGRCRoom("CORE GRC", session, tenant_id),
        "gate": BaseRoom("GATE FOUNDATION", session, tenant_id),
        "gougle": BaseRoom("GOUGLE", session, tenant_id),
        "isoc": BaseRoom("ISOC", session, tenant_id),
        "safeguard": BaseRoom("SAFEGUARD", session, tenant_id),
        "unicef": BaseRoom("UNICEF", session, tenant_id)
    }
    return registry.get(room_key.lower())

async def get_room_data_async(room_key: str, user_role: str, session: Session, tenant_id: str):
    # 1. Permission Check
    if room_key == "core" and user_role != "admin":
        return {"error": "Access Denied: Admin role required"}
    
    # 2. Get Instance
    room = get_room_instance(room_key, session, tenant_id)
    if not room:
        return {"error": "Room not found"}
        
    # 3. Async Execution
    return await room.to_json()
