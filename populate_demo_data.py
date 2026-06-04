import sqlite3
from datetime import datetime

conn = sqlite3.connect('compliance_ledger.db')
cursor = conn.cursor()

# Insert a dummy audit run
cursor.execute("INSERT INTO audit_run (tenant_id, timestamp, attainment_rate) VALUES (?, ?, ?)", 
               ("SME_STANDARD_001", datetime.now(), 85.5))
run_id = cursor.lastrowid

# Insert dummy findings
cursor.execute("INSERT INTO control_finding (audit_run_id, control_name, status) VALUES (?, ?, ?)", 
               (run_id, "King V Principle 1", "PASSED"))
cursor.execute("INSERT INTO control_finding (audit_run_id, control_name, status) VALUES (?, ?, ?)", 
               (run_id, "King V Principle 2", "PENDING"))

conn.commit()
conn.close()
print("Demo data injected successfully.")
