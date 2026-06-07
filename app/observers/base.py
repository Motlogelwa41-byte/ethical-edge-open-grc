from abc import ABC, abstractmethod
from datetime import datetime

class BaseObserver(ABC):
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id

    @abstractmethod
    def collect(self) -> dict:
        """Returns evidence dictionary: {resource_id, status, details, proof_data}"""
        pass

    def record_evidence(self, gate_id, result_dict):
        # Logic to insert into gate_evaluations and audit_log
        pass
