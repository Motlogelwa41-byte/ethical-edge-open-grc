import time
import logging
from app.observers.aws_observer import AWSObserver
from sqlalchemy.exc import SQLAlchemyError

# Set up logging for audit trails
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def continuous_observation_loop():
    logger.info("👀 Observer Service Started. Monitoring AWS Security Groups...")
    observer = AWSObserver()
    
    while True:
        try:
            logger.info("🔍 Scanning AWS Security Groups...")
            observer.sync_to_db()
            logger.info("✅ Sync completed successfully.")
        except SQLAlchemyError as db_err:
            logger.error(f"❌ Database connection lost: {db_err}. Retrying in 300s...")
        except Exception as e:
            logger.error(f"❌ AWS Observer unexpected error: {e}")
        
        # Sleep for 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    continuous_observation_loop()

from app.observers.file_observer import FileObserver
import time

def continuous_observation_loop():
    # List of files you want to protect
    monitors = [
        FileObserver(".env", "GATE-ENV-SECURITY"),
        FileObserver("data/king_v_checklist.json", "GATE-KINGV-DATA")
    ]
    
    while True:
        for monitor in monitors:
            monitor.sync_to_db()
        time.sleep(60) # Scan every minute
