import requests
import os
from sqlalchemy import text
# Make sure this import path is correct for your project structure
from app.observers.base_observer import BaseControlObserver

class GitHubObserver(BaseControlObserver):
    def __init__(self, repo_name=None):
        self.token = os.getenv("GITHUB_TOKEN")
        # Default to a safe fallback if the env var is missing
        self.repo_name = repo_name or os.getenv("MOCK_CLIENT_GITHUB_ORG", "default-org/repo")
        self.headers = {
            "Authorization": f"token {self.token}"
        }

    def check_branch_protection(self, branch="main"):
        url = (
            f"https://api.github.com/repos/"
            f"{self.repo_name}/branches/{branch}/protection"
        )
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return False
            data = response.json()
            reviews = data.get("required_pull_request_reviews", {})
            status_checks = data.get("required_status_checks", {})
            return bool(reviews and status_checks)
        except Exception:
            return False

    def sync_to_db(self, session):
        # Everything here is now correctly indented inside the class
        is_compliant = self.check_branch_protection()
        status = "PASS" if is_compliant else "FAIL"

        session.execute(
            text(
                "UPDATE room_gates "
                "SET validation_type = :status "
                "WHERE gate_id = 'GATE-GITHUB-01'"
            ),
            {"status": status}
        )

        print(
            f"🐙 GitHub Observer "
            f"[Branch Protection]: {status}"
        )
