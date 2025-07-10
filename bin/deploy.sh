#!/bin/bash
set -e

# Get version from argument
VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Error: Version number is required"
    exit 1
fi

DEPLOY_DIR="${DEPLOY_DIR:-/opt/deployments}"
APP_DIR="$DEPLOY_DIR/pointsheet-$VERSION"
CURRENT_LINK="$DEPLOY_DIR/current"
PREVIOUS_VERSION_FILE="$DEPLOY_DIR/previous_version"

# Check if the version directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "Error: Version directory $APP_DIR does not exist"
    exit 1
fi

# Save current version for potential rollback
if [ -L "$CURRENT_LINK" ]; then
    CURRENT_VERSION=$(basename $(readlink -f $CURRENT_LINK))
    echo $CURRENT_VERSION > $PREVIOUS_VERSION_FILE
fi

# Stop services before updating
echo "Stopping pointsheet.service and pointsheet-worker.service..."
sudo systemctl stop pointsheet.service pointsheet-worker.service

# Activate virtual environment and install dependencies
source $DEPLOY_DIR/venv/bin/activate
cd $APP_DIR/backend/pointsheet
python3 -m pip install poetry
poetry install

# Update the symlink to point to the new version
ln -sfn $APP_DIR $CURRENT_LINK

# Check if environment variables from .env are exported
echo "Checking environment variables..."
cd $APP_DIR/backend/pointsheet
ENV_FILE="$APP_DIR/backend/pointsheet/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Source the .env file to export variables
set -a
source "$ENV_FILE"
set +a

# Verify critical environment variables
REQUIRED_VARS=("DATABASE" "SECRET_KEY" "BROKER_URL" "RESULT_BACKEND")
MISSING_VARS=0

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set in .env file"
        MISSING_VARS=1
    fi
done

if [ $MISSING_VARS -eq 1 ]; then
    echo "Error: Missing required environment variables. Deployment aborted."
    exit 1
fi

# Run alembic migrations before starting services
echo "Running database migrations..."
$DEPLOY_DIR/venv/bin/python -m alembic upgrade head
cd $DEPLOY_DIR

# Caddy configuration is no longer included in the deployment package
# If you need to update Caddy configuration, do it manually or through another process

# Ensure log directory exists
sudo mkdir -p /var/logs/pointsheets
sudo chown www-data:www-data /var/logs/pointsheets
sudo chmod 755 /var/logs/pointsheets

# Function to process and install systemd service files
process_systemd_template() {
    local template_file="$1"
    local output_file="$2"

    # Process the template file, replacing placeholders with actual values
    sed -e "s|__CURRENT_LINK__|$CURRENT_LINK|g" \
        -e "s|__DEPLOY_DIR__|$DEPLOY_DIR|g" \
        "$template_file" > "/tmp/$(basename "$output_file")"

    # Check if the service file exists and compare hashes
    if [ -f "$output_file" ]; then
        # Calculate hash of existing service file
        existing_hash=$(md5sum "$output_file" | awk '{print $1}')
        # Calculate hash of new service file
        new_hash=$(md5sum "/tmp/$(basename "$output_file")" | awk '{print $1}')

        # Compare hashes and only override if different
        if [ "$existing_hash" != "$new_hash" ]; then
            echo "Updating $(basename "$output_file") (files are different)"
            sudo mv "/tmp/$(basename "$output_file")" "$output_file"
        else
            echo "Skipping $(basename "$output_file") (no changes detected)"
            rm "/tmp/$(basename "$output_file")"
        fi
    else
        echo "Installing new $(basename "$output_file")"
        sudo mv "/tmp/$(basename "$output_file")" "$output_file"
    fi
}

# Process and install pointsheet service
echo "Setting up pointsheet service..."
process_systemd_template "$CURRENT_LINK/bin/systemd/pointsheet.service.template" "/etc/systemd/system/pointsheet.service"

# Setup systemd service and timer for webhook processing
echo "Setting up systemd service and timer for webhook processing..."

# Process and install webhook processor service and timer
process_systemd_template "$CURRENT_LINK/bin/systemd/webhook-processor.service.template" "/etc/systemd/system/webhook-processor.service"
process_systemd_template "$CURRENT_LINK/bin/systemd/webhook-processor.timer.template" "/etc/systemd/system/webhook-processor.timer"

# Enable and start the timer
sudo systemctl enable webhook-processor.timer
sudo systemctl start webhook-processor.timer

# Reload systemd and start services
sudo systemctl daemon-reload
echo "Starting pointsheet.service and pointsheet-worker.service..."
sudo systemctl start pointsheet.service pointsheet-worker.service
sudo systemctl restart caddy

# Keep only the 2 most recent versions and their zip files
cd $DEPLOY_DIR

# Get the list of all version directories
ALL_DIRS=$(ls -td pointsheet-*/)

# Keep only the 2 most recent directories
KEEP_DIRS=$(echo "$ALL_DIRS" | head -n 2)

# Remove all directories except the ones to keep
for dir in $ALL_DIRS; do
    if ! echo "$KEEP_DIRS" | grep -q "$dir"; then
        rm -rf "$dir"
    fi
done

# Get the list of all zip files
ALL_ZIPS=$(ls -t pointsheet-*.zip 2>/dev/null || echo "")

# Keep only the zip files corresponding to the kept directories
for dir in $KEEP_DIRS; do
    # Extract version from directory name (remove trailing slash)
    version=$(basename "$dir" | sed 's/\/$//')
    # Add this zip file to the list of zips to keep
    KEEP_ZIPS="$KEEP_ZIPS $version.zip"
done

# Remove all zip files except the ones to keep
if [ -n "$ALL_ZIPS" ]; then
    for zip in $ALL_ZIPS; do
        if ! echo "$KEEP_ZIPS" | grep -q "$zip"; then
            rm -f "$zip"
        fi
    done
fi

echo "Deployment of version $VERSION completed successfully"
