from abc import ABC, abstractmethod

class BaseControlObserver(ABC):
    @abstractmethod
    def verify(self) -> ControlVerificationResult:
        pass

import os
import boto3
import requests
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Dict, Any

class ControlVerificationResult(BaseModel):
    control_reference: str
    control_name: str
    framework: str
    status: str = Field(..., description="PASSED or FAILED")
    evidence_payload: Dict[str, Any] = Field(..., description="Raw JSON data proving the state to auditors")
    checked_at: str

class ComplianceTelemetryPayload(BaseModel):
    system_id: str
    timestamp: str
    results: List[ControlVerificationResult]
    calculated_attainment_rate: float

class GRCEvidenceEngine:
    def __init__(self, target_system_id: str):
        self.system_id = target_system_id
        self.checked_time = datetime.now(timezone.utc).isoformat()

    def verify_aws_mfa_control(self) -> ControlVerificationResult:
        """
        Maps to ISO 27001:2022 A.8.5 & BDPA Access Control principles.
        Verifies if IAM Users have MFA active.
        """
        try:
            iam_client = boto3.client('iam')
            users = iam_client.list_users()['Users']
            
            failed_users = []
            total_users = len(users)

            for user in users:
                mfa_devices = iam_client.list_mfa_devices(UserName=user['UserName'])['MFADevices']
                if not mfa_devices:
                    failed_users.append(user['UserName'])

            status = "PASSED" if not failed_users else "FAILED"
            evidence = {
                "total_iam_users_scanned": total_users,
                "non_compliant_users": failed_users,
                "assessment_notes": "All users must have an active MFA token."
            }

            return ControlVerificationResult(
                control_reference="A.8.5",
                control_name="Multi-Factor Authentication Enforcement",
                framework="ISO/IEC 27001:2022",
                status=status,
                evidence_payload=evidence,
                checked_at=self.checked_time
            )
        except Exception as e:
            return ControlVerificationResult(
                control_reference="A.8.5",
                control_name="Multi-Factor Authentication Enforcement",
                framework="ISO/IEC 27001:2022",
                status="FAILED",
                evidence_payload={"error": str(e), "context": "AWS API Connection Failure"},
                checked_at=self.checked_time
            )

    def verify_github_repository_privacy(self, org_name: str, github_token: str) -> ControlVerificationResult:
        """
        Maps to NIST CSF 2.0 PR.DS-01 & POPIA / BDPA Information Protection.
        Ensures internal development assets aren't misconfigured as public.
        """
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }
        url = f"https://api.github.com/orgs/{org_name}/repos?type=public"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            public_repos = response.json() if response.status_code == 200 else []
            
            is_compliant = len(public_repos) == 0
            status = "PASSED" if is_compliant else "FAILED"
            
            evidence = {
                "public_repo_count": len(public_repos),
                "exposed_repositories": [repo['name'] for repo in public_repos][:5],
                "http_status_code": response.status_code
            }
            
            return ControlVerificationResult(
                control_reference="PR.DS-01",
                control_name="Data Repositories Protection & Leak Mitigation",
                framework="NIST CSF 2.0",
                status=status,
                evidence_payload=evidence,
                checked_at=self.checked_time
            )
        except Exception as e:
            return ControlVerificationResult(
                control_reference="PR.DS-01",
                control_name="Data Repositories Protection & Leak Mitigation",
                framework="NIST CSF 2.0",
                status="FAILED",
                evidence_payload={"error": str(e)},
                checked_at=self.checked_time
            )

    def execute_pipeline(self, github_org: str, github_token: str) -> ComplianceTelemetryPayload:
        """
        Executes all active continuous evidence scripts and calculates the attainment score.
        """
        results = [
            self.verify_aws_mfa_control(),
            self.verify_github_repository_privacy(github_org, github_token)
        ]
        
        passed_count = sum(1 for r in results if r.status == "PASSED")
        attainment_rate = (passed_count / len(results)) * 100.0 if results else 0.0

        return ComplianceTelemetryPayload(
            system_id=self.system_id,
            timestamp=self.checked_time,
            results=results,
            calculated_attainment_rate=round(attainment_rate, 2)
        )
