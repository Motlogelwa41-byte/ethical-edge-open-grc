import time
import logging
from app.observers.aws_observer import AWSObserver
from app.observers.github_observer import GitHubObserver
from app.observers.file_observer import FileObserver

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EthicalEdgeOrchestrator")

def run_orchestrator():
    logger.info("🚀 Starting Ethical Edge Master Orchestrator...")
    
    # Initialize your sensors
    sensors = [
        AWSObserver(),
        GitHubObserver("your-org/your-repo"),
        FileObserver(".env", "GATE-ENV-01"),
        FileObserver("data/king_v_checklist.json", "GATE-KINGV-DATA")
    ]
    
    while True:
        for sensor in sensors:
            try:
                sensor_name = sensor.__class__.__name__
                logger.info(f"🔍 Running {sensor_name}...")
                sensor.sync_to_db()
            except Exception as e:
                logger.error(f"❌ {sensor.__class__.__name__} failed: {e}")
        
        logger.info("💤 Sleeping for 300 seconds...")
        time.sleep(300)

if __name__ == "__main__":
    run_orchestrator()
