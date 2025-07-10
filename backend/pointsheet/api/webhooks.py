from flask import Blueprint, jsonify, current_app
from flask_pydantic import validate

from modules.notification.commands.create_webhook import CreateWebhook
from modules.notification.commands.update_webhook import UpdateWebhook
from modules.notification.commands.delete_webhook import DeleteWebhook
from modules.notification.commands.toggle_webhook import ToggleWebhook
from modules.notification.commands.create_webhook_subscription import CreateWebhookSubscription
from modules.notification.commands.delete_webhook_subscription import DeleteWebhookSubscription
from modules.notification.domain.requests import WebhookCreate, WebhookUpdate, WebhookSubscriptionCreate
from modules.notification.queries.get_webhook import GetWebhook
from modules.notification.queries.get_all_webhooks import GetAllWebhooks
from modules.notification.queries.get_webhook_subscriptions import GetWebhookSubscriptions
from modules.notification.domain.value_objects import WebhookEventType, WebhookPlatform
from pointsheet.domain.responses import ResourceCreated

webhook_bp = Blueprint("webhooks", __name__, url_prefix="/webhooks")


# Create a new webhook
@webhook_bp.route("", methods=["POST"])
@validate()
def create_webhook(body: WebhookCreate):
    cmd = CreateWebhook(
        name=body.name,
        target_url=str(body.target_url),
        platform=body.platform,
        secret=body.secret,
        config=body.config
    )
    webhook = current_app.application.execute(cmd)
    return ResourceCreated(resource=str(webhook.id)).model_dump(), 201

# Get all webhooks
@webhook_bp.route("", methods=["GET"])
def get_webhooks():
    query = GetAllWebhooks()
    webhooks = current_app.application.execute(query)
    return jsonify([webhook.model_dump() for webhook in webhooks])

# Get a specific webhook
@webhook_bp.route("/<webhook_id>", methods=["GET"])
def get_webhook(webhook_id):
    query = GetWebhook(webhook_id=webhook_id)
    webhook = current_app.application.execute(query)
    return jsonify(webhook.model_dump())

# Update a webhook
@webhook_bp.route("/<webhook_id>", methods=["PATCH"])
@validate()
def update_webhook(webhook_id, body: WebhookUpdate):
    cmd = UpdateWebhook(
        webhook_id=webhook_id,
        name=body.name,
        target_url=str(body.target_url) if body.target_url else None,
        platform=body.platform,
        secret=body.secret,
        config=body.config,
        enabled=body.enabled
    )
    webhook = current_app.application.execute(cmd)
    return jsonify(webhook.model_dump())

# Delete a webhook
@webhook_bp.route("/<webhook_id>", methods=["DELETE"])
def delete_webhook(webhook_id):
    cmd = DeleteWebhook(webhook_id=webhook_id)
    current_app.application.execute(cmd)
    return "", 204

# Enable/disable a webhook
@webhook_bp.route("/<webhook_id>/toggle", methods=["POST"])
def toggle_webhook(webhook_id):
    cmd = ToggleWebhook(webhook_id=webhook_id)
    webhook_id, enabled = current_app.application.execute(cmd)
    return jsonify({"id": str(webhook_id), "enabled": enabled})

# Create a webhook subscription
@webhook_bp.route("/subscriptions", methods=["POST"])
@validate()
def create_subscription(body: WebhookSubscriptionCreate):
    cmd = CreateWebhookSubscription(
        webhook_id=body.webhook_id,
        event_type=body.event_type,
        resource_type=body.resource_type,
        resource_id=body.resource_id
    )
    subscription = current_app.application.execute(cmd)
    return ResourceCreated(resource=str(subscription.id)).model_dump(), 201

# Get subscriptions for a webhook
@webhook_bp.route("/<webhook_id>/subscriptions", methods=["GET"])
def get_webhook_subscriptions(webhook_id):
    query = GetWebhookSubscriptions(webhook_id=webhook_id)
    subscriptions = current_app.application.execute(query)
    return jsonify([subscription.model_dump() for subscription in subscriptions])

# Delete a subscription
@webhook_bp.route("/subscriptions/<subscription_id>", methods=["DELETE"])
def delete_subscription(subscription_id):
    cmd = DeleteWebhookSubscription(subscription_id=subscription_id)
    current_app.application.execute(cmd)
    return None, 204

# Get available event types
@webhook_bp.route("/event-types", methods=["GET"])
def get_event_types():
    event_types = [
        {"id": event_type.value, "name": event_type.name.replace('_', ' ').title()}
        for event_type in WebhookEventType
    ]
    return jsonify(event_types)

# Get available webhook platforms
@webhook_bp.route("/platforms", methods=["GET"])
def get_platforms():
    platforms = [
        {"id": platform.value, "name": platform.name}
        for platform in WebhookPlatform
    ]
    return jsonify(platforms)
