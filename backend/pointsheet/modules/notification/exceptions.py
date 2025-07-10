from pointsheet.domain.exceptions.base import PointSheetException


class WebhookNotFoundException(PointSheetException):
    code = 404
    message = "Webhook not found"


class WebhookSubscriptionNotFoundException(PointSheetException):
    code = 404
    message = "Webhook subscription not found"


class InvalidWebhookConfigurationException(PointSheetException):
    code = 400
    message = "Invalid webhook configuration"


class DuplicateWebhookException(PointSheetException):
    code = 400
    message = "Webhook with the same name already exists"