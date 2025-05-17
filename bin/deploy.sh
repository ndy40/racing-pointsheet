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

# Activate virtual environment and install dependencies
source $DEPLOY_DIR/venv/bin/activate
cd $APP_DIR/backend/pointsheet
python3 -m pip install poetry
poetry install

# Update the symlink to point to the new version
ln -sfn $APP_DIR $CURRENT_LINK

# Caddy configuration is no longer included in the deployment package
# If you need to update Caddy configuration, do it manually or through another process

# Create or update systemd service files
cat > /tmp/pointsheet.service << EOF
[Unit]
Description=Pointsheet Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=$CURRENT_LINK/backend/pointsheet
Environment="PATH=$DEPLOY_DIR/venv/bin"
EnvironmentFile=$CURRENT_LINK/backend/pointsheet/.env
ExecStart=$DEPLOY_DIR/venv/bin/gunicorn --workers=2 --threads=2 --worker-class=gthread --bind=127.0.0.1:5000 "pointsheet:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

cat > /tmp/pointsheet-worker.service << EOF
[Unit]
Description=Pointsheet Celery Worker
After=network.target

[Service]
User=www-data
WorkingDirectory=$CURRENT_LINK/backend/pointsheet
Environment="PATH=$DEPLOY_DIR/venv/bin"
EnvironmentFile=$CURRENT_LINK/backend/pointsheet/.env
ExecStart=$DEPLOY_DIR/venv/bin/celery -A pointsheet.celery_worker worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Move service files to systemd directory
sudo mv /tmp/pointsheet.service /etc/systemd/system/
sudo mv /tmp/pointsheet-worker.service /etc/systemd/system/

# Reload systemd, restart services
sudo systemctl daemon-reload
sudo systemctl restart pointsheet pointsheet-worker
sudo systemctl restart caddy

# Keep only the 5 most recent versions (adjust as needed)
cd $DEPLOY_DIR
ls -t | grep 'pointsheet-' | tail -n +6 | xargs -r rm -rf

echo "Deployment of version $VERSION completed successfully"
