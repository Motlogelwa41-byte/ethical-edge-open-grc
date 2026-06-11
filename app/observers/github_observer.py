from app.observers.base_observer import BaseControlObserver
from app.database.models import ControlFinding

class GitHubObserver(BaseControlObserver):
    def sync_to_db(self, session):
        # Implement GitHub-specific logic here
        new_finding = ControlFinding(
            control_reference="GH-001",
            control_name="Repository Visibility",
            status="PASS",
            evidence_payload="Repo is private"
        )
        session.add(new_finding)
