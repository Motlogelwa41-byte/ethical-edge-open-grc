from app.observers.base_observer import BaseObserver
from app.database.models import ControlFinding

class GitHubObserver(BaseObserver):

    def sync_to_db(self, session):
        new_finding = ControlFinding(
            control_reference="GH-001",
            control_name="Repository Visibility",
            status="PASS",
            evidence_payload="Repo is private"
        )

        session.add(new_finding)
