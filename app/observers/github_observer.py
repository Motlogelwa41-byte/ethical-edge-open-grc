from app.observers.base_observer import BaseControlObserver
from app.database.models import ControlFinding

from app.observers.base_observer import BaseObserver

class GitHubObserver(BaseObserver):
    def sync_to_db(self, session):
        # Implement GitHub-specific logic here
        new_finding = ControlFinding(
            control_reference="GH-001",
            control_name="Repository Visibility",
            status="PASS",
            evidence_payload="Repo is private"
        )
        session.add(new_finding)

def safe_sync(self):
    try:
        findings = self.observe()
        self.sync_to_db(findings)
        return True
    except Exception as e:
        self.logger.error(f"GitHub sync failed: {e}")
        return False
