import logging
from github_observer import GitHubObserver
# from aws_observer import AWSObserver  # You will import new observers here

class EngineOrchestrator:
    def __init__(self, tenant_id, db_connection):
        self.tenant_id = tenant_id
        self.db = db_connection
        # Register all active observers here
        self.observers = [
            GitHubObserver(tenant_id),
            # AWSObserver(tenant_id),
        ]

    def run_all(self):
        print(f"Starting compliance sync for Tenant: {self.tenant_id}")
        
        for observer in self.observers:
            print(f"Running collector: {observer.__class__.__name__}")
            try:
                # 1. Collect normalized data
                results = observer.collect()
                
                # 2. Persist to Database (The Ledger)
                for entry in results:
                    self._persist_to_ledger(entry)
                    
            except Exception as e:
                logging.error(f"Failed to run {observer.__class__.__name__}: {str(e)}")

    def _persist_to_ledger(self, entry):
        """
        Maps the unified evidence format to your database/init_schema.sql tables.
        """
        # SQL logic to insert into gate_evaluations
        query = """
            INSERT INTO gate_evaluations 
            (assessment_id, gate_id, is_passed, evidence_snapshot) 
            VALUES (%s, %s, %s, %s)
        """
        # self.db.execute(query, (self.tenant_id, entry['gate_id'], entry['is_passed'], entry['evidence_snapshot']))
        print(f"SUCCESS: Logged {entry['gate_id']} to Ledger.")

# Example Usage
if __name__ == "__main__":
    # In production, pass your actual DB connection here
    orchestrator = EngineOrchestrator(tenant_id="your-tenant-uuid", db_connection=None)
    orchestrator.run_all()
