from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseObserver(ABC):
    """Base observer with transactional database synchronization."""

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
