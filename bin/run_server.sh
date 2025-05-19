#!/bin/bash
set -e

# Load the virtual environment
echo "Loading virtual environment from /opt/deployments/venv..."
source /opt/deployments/venv/bin/activate

# Get the directory where the script is located
PROJECT_ROOT="/opt/deployments/current"
ENV_FILE="$PROJECT_ROOT/backend/pointsheet/.env"

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Export all variables from .env file
echo "Loading environment variables from $ENV_FILE"
set -a
source "$ENV_FILE"
set +a

# Change to the application directory
cd "$PROJECT_ROOT/backend/pointsheet"

# Run alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Check if migrations were successful
if [ $? -ne 0 ]; then
    echo "Error: Database migrations failed. Startup aborted."
    exit 1
fi

# Start the application using gunicorn
echo "Starting application with gunicorn..."
exec gunicorn --workers=1 --threads=2 --worker-class=gthread --bind=127.0.0.1:5000 --log-file=/var/logs/pointsheets/pointsheet.log --log-level=info "pointsheet:create_app()"
