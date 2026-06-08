import time
import logging
import signal
import sys
from app.observers.aws_observer import AWSObserver
from app.observers.github_observer import GitHubObserver
from app.observers.file_observer import FileObserver

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("EthicalEdgeOrchestrator")

def handle_shutdown(signum, frame):
    logger.info("🛑 Shutdown signal received. Cleaning up...")
    sys.exit(0)

# Register signals for clean exits
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def run_orchestrator():
    logger.info("🛡️ Ethical Edge Master Orchestrator: Initializing sensors...")
    
    # Initialize sensors
    sensors = [
        AWSObserver(),
        GitHubObserver(repo_name="Motlogelwa41-byte/ethical-edge-open-grc"),
        FileObserver(target_file=".env", gate_id="GATE-ENV-01"),
        FileObserver(target_file="data/king_v_checklist.json", gate_id="GATE-KINGV-DATA")
    ]
    
    logger.info(f"✅ {len(sensors)} sensors ready.")
    
    while True:
        for sensor in sensors:
            try:
                name = sensor.__class__.__name__
                logger.info(f"🔍 Executing: {name}")
                sensor.sync_to_db()
            except Exception as e:
                logger.error(f"❌ Failure in {sensor.__class__.__name__}: {e}")
        
        logger.info("💤 Cycle complete. Sleeping for 300s.")
        time.sleep(300)

if __name__ == "__main__":
    run_orchestrator()

# Add this inside your while loop
sensor_health = {sensor.__class__.__name__: True for sensor in sensors}

# ... inside your for loop ...
except Exception as e:
    sensor_health[name] = False  # Mark as unhealthy
    logger.error(f"❌ Failure in {name}: {e}")
    # ALERT: You should trigger an internal notification here!
    
# ... Optional: Only run healthy sensors
if sensor_health[name]:
    sensor.sync_to_db()
