#!/bin/bash
set -e

# Load the virtual environment
echo "Loading virtual environment from /opt/deployments/venv..."
source /opt/deployments/venv/bin/activate

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
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
    echo "Error: Missing required environment variables. Startup aborted."
    exit 1
fi

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
