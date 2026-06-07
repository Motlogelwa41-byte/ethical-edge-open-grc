import boto3
from datetime import datetime, timezone
from app.services.base import BaseControlObserver
from app.services.evidence_collector import ControlVerificationResult

class AWSObserver(BaseControlObserver):
    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name='us-east-1')

    def check_ssh_port_access(self):
        """Scans Security Groups for open SSH (Port 22) access to 0.0.0.0/0."""
        sgs = self.ec2.describe_security_groups()
        for sg in sgs['SecurityGroups']:
            for permission in sg.get('IpPermissions', []):
                if permission.get('FromPort') == 22:
                    for ip_range in permission.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            return False  # Non-compliant
        return True  # Compliant

    def verify(self) -> ControlVerificationResult:
        is_compliant = self.check_ssh_port_access()
        
        return ControlVerificationResult(
            control_reference="AWS-SEC-01",
            control_name="SSH Port 22 Access",
            framework="ISO/IEC 27001:2022",
            status="PASSED" if is_compliant else "FAILED",
            evidence_payload={"ssh_open_to_world": not is_compliant},
            checked_at=datetime.now(timezone.utc).isoformat()
        )
