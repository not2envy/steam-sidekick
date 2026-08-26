class SensorNotFoundError(Exception):
    """Raised when a specific system hardware sensor cannot be located."""
    pass

class SensorReadingError(Exception):
    """Raised when a specific system hardware sensor cannot be read."""
    pass