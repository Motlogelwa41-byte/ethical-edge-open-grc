# In app/services/base.py
from app.database import SessionLocal # Adjust import path as needed

class BaseControlObserver:
    def safe_sync(self):
        """
        Transactional wrapper for database operations.
        Ensures atomicity for all compliance observations.
        """
        session = SessionLocal()
        try:
            # Pass the session to the child observer's specific logic
            self.sync_to_db(session)
            session.commit()
        except Exception as e:
            session.rollback()
            # Log the specific error for the audit trail
            raise e
        finally:
            session.close()

    def sync_to_db(self, session):
        """Must be implemented by child classes."""
        raise NotImplementedError("Child observers must implement sync_to_db")
