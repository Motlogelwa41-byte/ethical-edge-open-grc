from sqlalchemy.orm import Session
from app.models.audit import AuditLog

class AuditService:
    @staticmethod
    def log_event(db: Session, gate_id: str, event_type: str, prev: str, new: str, snapshot: dict = None):
        new_log = AuditLog(
            gate_id=gate_id,
            event_type=event_type,
            previous_status=prev,
            new_status=new,
            evidence_snapshot=snapshot
        )
        db.add(new_log)
        db.commit()
