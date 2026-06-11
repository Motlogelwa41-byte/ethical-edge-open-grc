from app.observers.base_observer import BaseControlObserver
from app.database.models import ControlFinding # Assuming this is your model

class AWSObserver(BaseControlObserver):
    def sync_to_db(self, session):
        """
        The BaseControlObserver provides the 'session'. 
        You use this 'session' to add data to your database.
        """
        # Example logic
        new_finding = ControlFinding(
            control_reference="AWS-001",
            control_name="S3 Public Access",
            status="FAIL",
            evidence_payload="Bucket is public"
        )
        session.add(new_finding)
        # No need to commit or close! The base_observer does that for you.
