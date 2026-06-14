import requests
import os
from sqlalchemy import text
from app.services.base import BaseControlObserver

class GitHubObserver(BaseControlObserver):
    def __init__(self, repo_name):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name
        self.headers = {
            "Authorization": f"token {self.token}"
        }

    def check_branch_protection(self, branch="main"):
        url = (
            f"https://api.github.com/repos/"
            f"{self.repo_name}/branches/{branch}/protection"
        )

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return False

        data = response.json()

        reviews = data.get(
            "required_pull_request_reviews", {}
        )

        status_checks = data.get(
            "required_status_checks", {}
        )

        return bool(reviews and status_checks)

    def sync_to_db(self, session):

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
