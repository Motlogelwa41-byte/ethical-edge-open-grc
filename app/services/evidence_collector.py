import os
import boto3
import requests
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Dict, Any
from abc import ABC, abstractmethod

# 1. Standardized Result Model
class ControlVerificationResult(BaseModel):
    control_reference: str
    control_name: str
    framework: str
    status: str = Field(..., description="PASSED or FAILED")
    evidence_payload: Dict[str, Any]
    remediation_steps: str = Field(..., description="Actionable fix for failures")
    checked_at: str

# 2. Base Observer Pattern
class BaseControlObserver(ABC):
    @abstractmethod
    def verify(self) -> ControlVerificationResult:
        pass

# 3. Telemetry Payload
class ComplianceTelemetryPayload(BaseModel):
    system_id: str
    timestamp: str
    results: List[ControlVerificationResult]
    calculated_attainment_rate: float

# 4. Evidence Engine
class GRCEvidenceEngine:
    def __init__(self, target_system_id: str):
        self.system_id = target_system_id
        self.checked_time = datetime.now(timezone.utc).isoformat()

    def verify_aws_mfa_control(self) -> ControlVerificationResult:
        try:
            iam_client = boto3.client('iam')
            users = iam_client.list_users()['Users']
            failed_users = [u['UserName'] for u in users if not iam_client.list_mfa_devices(UserName=u['UserName'])['MFADevices']]
            
            return ControlVerificationResult(
                control_reference="A.8.5",
                control_name="MFA Enforcement",
                framework="ISO/IEC 27001:2022",
                status="PASSED" if not failed_users else "FAILED",
                evidence_payload={"failed_users": failed_users},
                remediation_steps="Navigate to IAM console, select user, and enable MFA device.",
                checked_at=self.checked_time
            )
        except Exception as e:
            return ControlVerificationResult(
                control_reference="A.8.5",
                control_name="MFA Enforcement",
                framework="ISO/IEC 27001:2022",
                status="FAILED",
                evidence_payload={"error": str(e)},
                remediation_steps="Check AWS credentials and IAM permissions.",
                checked_at=self.checked_time
            )

    def verify_github_repository_privacy(self, org_name: str, github_token: str) -> ControlVerificationResult:
        headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
        url = f"https://api.github.com/orgs/{org_name}/repos?type=public"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            public_repos = response.json() if response.status_code == 200 else []
            
            return ControlVerificationResult(
                control_reference="PR.DS-01",
                control_name="Repository Privacy",
                framework="NIST CSF 2.0",
                status="PASSED" if not public_repos else "FAILED",
                evidence_payload={"public_repo_count": len(public_repos)},
                remediation_steps="Change repository visibility to PRIVATE in GitHub settings.",
                checked_at=self.checked_time
            )
        except Exception as e:
            return ControlVerificationResult(
                control_reference="PR.DS-01",
                control_name="Repository Privacy",
                framework="NIST CSF 2.0",
                status="FAILED",
                evidence_payload={"error": str(e)},
                remediation_steps="Verify GitHub API token and network connectivity.",
                checked_at=self.checked_time
            )

    def execute_pipeline(self, github_org: str, github_token: str) -> ComplianceTelemetryPayload:
        results = [self.verify_aws_mfa_control(), self.verify_github_repository_privacy(github_org, github_token)]
        attainment_rate = (sum(1 for r in results if r.status == "PASSED") / len(results)) * 100.0
        return ComplianceTelemetryPayload(system_id=self.system_id, timestamp=self.checked_time, results=results, calculated_attainment_rate=round(attainment_rate, 2))
        
