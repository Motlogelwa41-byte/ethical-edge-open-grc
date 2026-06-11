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
def sync_to_db(self, findings):
    from database.db_manager import DBManager

    db = DBManager()

    for finding in findings:
        db.log_observation(
            source="AWS",
            data=finding
        )

or whatever logging method your DBManager uses.

Problem 2: GitHubObserver missing safe_sync()

Error:

'GitHubObserver' object has no attribute 'safe_sync'

This means orchestrator.py is calling:

observer.safe_sync()

but inside:

app/github_observer.py

there is no function called:

safe_sync()
Check orchestrator.py

Look for something like:

observer.safe_sync()

Then open:

app/github_observer.py

and add:

def safe_sync(self):
    try:
        findings = self.observe()
        self.sync_to_db(findings)
        return True
    except Exception as e:
        self.logger.error(f"GitHub sync failed: {e}")
        return False
Problem 3: FileObserver missing safe_sync()

Error:

'FileObserver' object has no attribute 'safe_sync'

Same issue.

Open:

app/file_observer.py

Add:

def safe_sync(self):
    try:
        findings = self.observe()
        self.sync_to_db(findings)
        return True
    except Exception as e:
        self.logger.error(f"File sync failed: {e}")
        return False
What I suspect happened

Looking at your GitHub history:

Update orchestrator.py (2 hours ago)
Update file_observer.py (31 minutes ago)
Update db_manager.py (4 days ago)

It looks like you recently upgraded the orchestrator to use a newer observer interface:

Old interface:

observe()

New interface:

safe_sync()
sync_to_db()

but the observer classes were not updated.

So now:

orchestrator.py

expects:

safe_sync()
sync_to_db()

while:

aws_observer.py
github_observer.py
file_observer.py

still implement only:

observe()
Fastest way to diagnose

Run:

find . -name "*.py" | xargs grep "safe_sync"

and:

find . -name "*.py" | xargs grep "sync_to_db"

If only orchestrator.py contains safe_sync, then that confirms the mismatch.

What I need from you

Please paste the contents of:

orchestrator.py

and

app/aws_observer.py

and

app/github_observer.py

and

app/file_observer.py

(or upload the files).

Then I can identify the exact lines causing the failure and provide the corrected code for Ethical Edge Open GRC.

Writing code? Meet

