from abc import ABC


class PointSheetException(Exception, ABC):
    """Base exception class for application"""

    message = "Application error"
