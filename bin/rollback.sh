#!/bin/bash
set -e

DEPLOY_DIR="${DEPLOY_DIR:-/opt/deployments}"
CURRENT_LINK="$DEPLOY_DIR/current"
PREVIOUS_VERSION_FILE="$DEPLOY_DIR/previous_version"

# Check if we have a previous version to roll back to
if [ ! -f "$PREVIOUS_VERSION_FILE" ]; then
    echo "Error: No previous version found for rollback"
    exit 1
fi

PREVIOUS_VERSION=$(cat $PREVIOUS_VERSION_FILE)
PREVIOUS_APP_DIR="$DEPLOY_DIR/$PREVIOUS_VERSION"

# Check if the previous version directory exists
if [ ! -d "$PREVIOUS_APP_DIR" ]; then
    echo "Error: Previous version directory $PREVIOUS_APP_DIR does not exist"
    exit 1
fi

# Update the symlink to point to the previous version
ln -sfn $PREVIOUS_APP_DIR $CURRENT_LINK

# Restart services
sudo systemctl restart pointsheet pointsheet-worker
sudo systemctl restart caddy

echo "Rolled back to version $PREVIOUS_VERSION successfully"

# Save the current rollback operation for potential "roll-forward"
CURRENT_VERSION=$(basename $(readlink -f $CURRENT_LINK))
echo $CURRENT_VERSION > $DEPLOY_DIR/rollback_version

echo "Rollback to version $PREVIOUS_VERSION completed successfully"
