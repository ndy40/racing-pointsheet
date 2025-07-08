# Racing Point Sheet

A simple app for managing sim racing events and keep track of points and scores.

# System Requirements

1. Docker
2. Node and Npm

# Setup

1. Clone the repository.
2. Update your hosts file to point to `pointsheet-app.com`. This is currently used by the `nginx.conf` file. Feel free to modify at will.

```ini
127.0.0.1 pointsheet-app.com
127.0.0.1 api.pointsheet-app.com
```

# Run application.

1. Change into the project directory - `racing-pointsheet`
2. Run `docker compose up`

# Initialize application database

1. Connect into the backend docker container. `docker container exec -it pointsheet-api`
2. Run the command to create db migration `alembic upgrade head`
3. This will create a database file in the folder `backend/pointsheet/instance/point_sheet.db.sqlite`
4. Open the db file in your favourite db view tool.

# Webhook CLI

The application includes a command-line interface for managing webhook notifications. These commands allow you to process pending webhook notifications, list webhook logs, and retry failed webhook deliveries.

To run these commands, you need to connect to the backend docker container:

```bash
docker container exec -it pointsheet-api bash
```

Then you can run the following commands:

## Process Pending Webhooks

Process pending webhook notifications:

```bash
python -m pointsheet.main webhook process
```

Options:
- `--limit INTEGER`: Maximum number of webhooks to process (default: 50)
- `--timeout INTEGER`: HTTP request timeout in seconds (default: 10)
- `--dry-run`: Don't actually send webhooks, just log what would be sent

Example:
```bash
# Process up to 20 webhooks with a 5-second timeout
python -m pointsheet.main webhook process --limit 20 --timeout 5

# Dry run to see what would be sent without actually sending
python -m pointsheet.main webhook process --dry-run
```

## List Webhook Logs

List webhook delivery logs:

```bash
python -m pointsheet.main webhook list
```

Options:
- `--limit INTEGER`: Maximum number of logs to show (default: 20)
- `--succeeded BOOLEAN`: Filter by success status (True/False)
- `--webhook-id TEXT`: Filter by webhook ID
- `--days INTEGER`: Show logs from the last N days (default: 1)

Example:
```bash
# Show failed webhook deliveries from the last 7 days
python -m pointsheet.main webhook list --succeeded False --days 7

# Show logs for a specific webhook
python -m pointsheet.main webhook list --webhook-id YOUR_WEBHOOK_ID
```

## Retry Failed Webhooks

Retry failed webhook deliveries:

```bash
python -m pointsheet.main webhook retry --all
```

Options:
- `--id TEXT`: Retry a specific webhook log by ID
- `--all`: Retry all failed webhooks
- `--limit INTEGER`: Maximum number of webhooks to retry (default: 10)
- `--timeout INTEGER`: HTTP request timeout in seconds (default: 10)

Example:
```bash
# Retry a specific webhook delivery
python -m pointsheet.main webhook retry --id YOUR_WEBHOOK_LOG_ID

# Retry all failed webhooks with a 15-second timeout
python -m pointsheet.main webhook retry --all --timeout 15
```

# URLs:

1. [pointsheet-app.com](pointsheet-app.com) is used for the Frontend powered by nextjs.
2. [api.poiintsheet-app.com](api.pointsheet-app.com) is the backend rest api. The root path `/` contains OpenAPI spec for testing the URL.

### TODO:

- [x] Add simple scripts for running routine commands for project.
- [x] Add click to make it easy to run commands in the container
- [x] Add linter checks - using ruff
- [x] Add pre-commit hooks
- [ ] Add github workflow
