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

# Create or update systemd service files
cat > /tmp/pointsheet.service << EOF
[Unit]
Description=Pointsheet Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=$CURRENT_LINK/backend/pointsheet
Environment="PATH=$DEPLOY_DIR/venv/bin"
ExecStart=$CURRENT_LINK/bin/run_server.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Check if service files exist and compare hashes
for service in pointsheet ; do
    if [ -f "/etc/systemd/system/${service}.service" ]; then
        # Calculate hash of existing service file
        existing_hash=$(md5sum "/etc/systemd/system/${service}.service" | awk '{print $1}')
        # Calculate hash of new service file
        new_hash=$(md5sum "/tmp/${service}.service" | awk '{print $1}')

        # Compare hashes and only override if different
        if [ "$existing_hash" != "$new_hash" ]; then
            echo "Updating ${service}.service (files are different)"
            sudo mv "/tmp/${service}.service" "/etc/systemd/system/"
        else
            echo "Skipping ${service}.service (no changes detected)"
            rm "/tmp/${service}.service"
        fi
    else
        echo "Installing new ${service}.service"
        sudo mv "/tmp/${service}.service" "/etc/systemd/system/"
    fi
done

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
