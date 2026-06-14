from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

# Change this:
class BaseObserver(ABC):
# To this:
class BaseControlObserver(ABC):
    
    def safe_sync(self):
        from app.database.connection import SessionLocal

        session = SessionLocal()

        try:
            self.sync_to_db(session)
            session.commit()

        except Exception as e:
            session.rollback()
            logger.error(
                f"Transaction failed for {self.__class__.__name__}: {e}"
            )
            raise

        finally:
            session.close()

    @abstractmethod
    def sync_to_db(self, session):
        pass
