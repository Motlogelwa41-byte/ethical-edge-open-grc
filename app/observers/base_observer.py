class BaseObserver:
    def check_status(self) -> bool:
        """Should return True if compliant, False if not."""
        raise NotImplementedError

class SystemFileObserver(BaseObserver):
    """Example: Checks if a critical config file exists."""
    def __init__(self, filepath: str):
        self.filepath = filepath

    def check_status(self) -> bool:
        return os.path.exists(self.filepath)
