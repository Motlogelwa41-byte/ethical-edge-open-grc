import requests
import os
from app.database.connection import SessionLocal
from sqlalchemy import text

class GitHubObserver:
    def __init__(self, repo_name):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name # Format: "owner/repo"
        self.headers = {"Authorization": f"token {self.token}"}

    def check_branch_protection(self, branch="main"):
        """Checks if the branch has the required security gates enabled."""
        url = f"https://api.github.com/repos/{self.repo_name}/branches/{branch}/protection"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return False # Protection is likely not configured or API error
        
        data = response.json()
        # Verify core compliance requirements
        reviews = data.get("required_pull_request_reviews", {})
        status_checks = data.get("required_status_checks", {})
        
        return bool(reviews and status_checks)

    def sync_to_db(self):
        is_compliant = self.check_branch_protection()
        status = 'PASS' if is_compliant else 'FAIL'
        
        session = SessionLocal()
        session.execute(
            text("UPDATE room_gates SET validation_type = :status WHERE gate_id = 'GATE-GITHUB-01'"),
            {"status": status}
        )
        session.commit()
        session.close()
        print(f"🐙 GitHub Observer [Branch Protection]: {status}")
