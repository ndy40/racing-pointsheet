from abc import ABC


class PointSheetException(Exception, ABC):
    """Base exception class for application"""

    message = "Application error"


class BusinessRuleValidationException(PointSheetException):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule)
