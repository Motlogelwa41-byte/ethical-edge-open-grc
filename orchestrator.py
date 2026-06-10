import time
import logging
import signal
import sys
import os
import json
from app.observers.aws_observer import AWSObserver
from app.observers.github_observer import GitHubObserver
from app.observers.file_observer import FileObserver

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("EthicalEdgeOrchestrator")

def handle_shutdown(signum, frame):
    logger.info("🛑 Shutdown signal received. Cleaning up...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def validate_dpa_evidence(uploads_dir="uploads"):
    checklist_path = os.path.join("data", "dpa_checklist.json")
    if not os.path.exists(checklist_path):
        return {"error": "Checklist file not found"}
    
    with open(checklist_path, "r") as f:
        config = json.load(f)
    
    if not os.path.exists(uploads_dir):
        return {"error": "Uploads directory not found"}
        
    files = os.listdir(uploads_dir)
    results = []

    for control in config["controls"]:
        # Match evidence type (e.g., 'PDF' or 'CSV') in filenames
        evidence_type = control["evidence_type"].split('/')[0].lower()
        found = any(evidence_type in f.lower() for f in files)
        
        results.append({
            "id": control["id"],
            "domain": control["domain"],
            "status": "PASS" if found else "FAIL"
        })
    return results

def run_orchestrator():
    logger.info("🛡️ Ethical Edge Master Orchestrator: Initializing sensors...")
    
    sensors = [
        AWSObserver(),
        GitHubObserver(repo_name="Motlogelwa41-byte/ethical-edge-open-grc"),
        FileObserver(target_file=".env", gate_id="GATE-ENV-01"),
        FileObserver(target_file="data/king_v_checklist.json", gate_id="GATE-KINGV-DATA")
    ]
    
    sensor_health = {sensor.__class__.__name__: True for sensor in sensors}
    logger.info(f"✅ {len(sensors)} sensors ready.")
    
    while True:
        # 1. Run standard sensors
        for sensor in sensors:
            name = sensor.__class__.__name__
            if sensor_health.get(name, True):
                try:
                    logger.info(f"🔍 Executing: {name}")
                    sensor.safe_sync()
                except Exception as e:
                    sensor_health[name] = False
                    logger.error(f"❌ Critical failure in {name}: {e}. Disabling sensor.")
        
        # 2. Run DPA Compliance Check
        logger.info("⚖️ Running DPA Compliance Validation...")
        dpa_results = validate_dpa_evidence()
        if isinstance(dpa_results, list):
            for check in dpa_results:
                icon = "✅" if check["status"] == "PASS" else "❌"
                logger.info(f"   {icon} [{check['id']}] {check['domain']}: {check['status']}")
        else:
            logger.error(f"   ❌ DPA Validation Error: {dpa_results.get('error')}")
        
        logger.info("💤 Cycle complete. Sleeping for 300s.")
        time.sleep(300)

if __name__ == "__main__":
    run_orchestrator()
