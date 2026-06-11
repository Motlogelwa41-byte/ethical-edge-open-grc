from app.services.base import BaseControlObserver
from app.database.models import ControlFinding

class AWSObserver(BaseControlObserver):
    """
    AWS Compliance Observer
    """

    def sync_to_db(self, session):
        """
        Called automatically by BaseControlObserver.safe_sync().
        The session is provided by the framework.
        """

        new_finding = ControlFinding(
            control_reference="AWS-001",
            control_name="S3 Public Access",
            status="FAIL",
            evidence_payload="Bucket is public"
        )

        session.add(new_finding)

        print("☁️ AWS Observer: Finding recorded")

