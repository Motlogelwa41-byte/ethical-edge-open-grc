import hashlib
from sqlalchemy import text
from app.observers.base_observer import BaseControlObserver

class FileObserver(BaseControlObserver):

    def __init__(self, target_file, gate_id):
        self.target_file = target_file
        self.gate_id = gate_id

    def _get_file_hash(self):
        sha256_hash = hashlib.sha256()

        try:
            with open(self.target_file, "rb") as f:
                for block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(block)

            return sha256_hash.hexdigest()

        except FileNotFoundError:
            return None

    def sync_to_db(self, session):

        current_hash = self._get_file_hash()

        status = "PASS" if current_hash else "FAIL"

        session.execute(
            text(
                "UPDATE room_gates "
                "SET validation_type = :status, "
                "last_verified = CURRENT_TIMESTAMP "
                "WHERE gate_id = :gid"
            ),
            {
                "status": status,
                "gid": self.gate_id
            }
        )

        print(
            f"🔒 File Integrity Observer "
            f"[{self.target_file}]: {status}"
        )
Problem 3: AWSObse
