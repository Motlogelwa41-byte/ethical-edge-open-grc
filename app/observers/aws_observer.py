import boto3
from app.database.connection import SessionLocal
from sqlalchemy import text

class AWSObserver:
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

    def sync_to_db(self):
        is_compliant = self.check_ssh_port_access()
        status = 'PASS' if is_compliant else 'FAIL'
        
        session = SessionLocal()
        # Update your specific room gate in the database
        session.execute(
            text("UPDATE room_gates SET validation_type = :status WHERE gate_id = 'GATE-KINGV-01'"),
            {"status": status}
        )
        session.commit()
        session.close()
        print(f"📡 AWS Security Group Observer: Status updated to {status}")
