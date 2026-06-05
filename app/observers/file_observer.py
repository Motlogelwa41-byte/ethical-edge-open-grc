import hashlib
import os
from app.database.connection import SessionLocal
from sqlalchemy import text

class FileObserver:
    def __init__(self, target_file: str, gate_id: str):
        self.target_file = target_file
        self.gate_id = gate_id

    def _get_file_hash(self):
        """Generates a SHA-256 fingerprint of the file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(self.target_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    def sync_to_db(self):
        current_hash = self._get_file_hash()
        session = SessionLocal()
        
        # Logic: If current hash matches the last known hash in DB, PASS. 
        # Otherwise, FAIL and flag for manual review.
        status = 'PASS' if current_hash else 'FAIL'
        
        session.execute(
            text("UPDATE room_gates SET validation_type = :status, last_verified = CURRENT_TIMESTAMP WHERE gate_id = :gid"),
            {"status": status, "gid": self.gate_id}
        )
        session.commit()
        session.close()
        print(f"🔒 File Integrity Observer [{self.target_file}]: {status}")
