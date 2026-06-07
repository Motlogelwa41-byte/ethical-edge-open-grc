from abc import ABC, abstractmethod
from datetime import datetime

class BaseObserver(ABC):
    """
    All data collectors MUST inherit from this class to ensure 
    they report data in a format the Database Ledger expects.
    """
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id

    @abstractmethod
    def collect(self) -> list:
        """
        Must return a list of dictionaries.
        Each dictionary MUST contain: 'gate_id', 'is_passed', 'evidence_snapshot'
        """
        pass

    def save_to_ledger(self, data: dict):
        """
        Standardized method to push evidence into the gate_evaluations table.
        """
        # Logic to connect to your database and perform an INSERT
        # into gate_evaluations (gate_id, is_passed, evidence_snapshot, evaluated_at)
        print(f"DEBUG: Saving to ledger for Tenant {self.tenant_id}...")
