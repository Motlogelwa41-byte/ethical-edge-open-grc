from base_observer import BaseObserver

class GitHubObserver(BaseObserver):
    def collect(self):
        # Your existing logic to fetch GitHub data goes here
        # ...
        
        # Now, normalize it to the required format
        return [
            {
                "gate_id": "GITHUB_MFA_ENABLED",
                "is_passed": True,  # Calculated from your logic
                "evidence_snapshot": {"raw_json": "..."} # The actual API response
            }
        ]
