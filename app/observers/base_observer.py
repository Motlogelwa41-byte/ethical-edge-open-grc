# In app/observers/base_observer.py

def safe_sync(self):
    """Template method to enforce transactional integrity."""
    session = db_session()
    try:
        self.sync_to_db(session)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction failed for {self.__class__.__name__}: {e}")
        raise
    finally:
        session.close()
