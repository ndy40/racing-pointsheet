# Racing Pointsheet Setup Guide

This document provides detailed instructions for setting up and deploying the Racing Pointsheet application.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A virtual environment tool (recommended)
- Git

### Local Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/racing-pointsheet.git
   cd racing-pointsheet
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:

   ```
   APP_ENV=development
   SECRET_KEY=your-secret-key-for-development
   ```

5. Initialize the database:

   ```bash
   cd backend
   python -m pointsheet.main migrate
   python -m pointsheet.main load-tracks
   ```

6. Run the application:

   ```bash
   python -m pointsheet.main run-server
   ```

7. Access the application at http://localhost:5000

### Running Tests

```bash
cd backend
pytest
```

## Production Deployment

### Prerequisites

- A server with Python 3.8 or higher
- A web server (e.g., Nginx, Apache)
- A WSGI server (e.g., Gunicorn, uWSGI)
- A database server (optional, SQLite is used by default)

### Deployment Steps

1. Clone the repository on your server:

   ```bash
   git clone https://github.com/yourusername/racing-pointsheet.git
   cd racing-pointsheet
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:

   ```
   APP_ENV=production
   SECRET_KEY=your-secure-secret-key
   ```

5. Initialize the database:

   ```bash
   cd backend
   python -m pointsheet.main migrate
   python -m pointsheet.main load-tracks
   ```

6. Set up a WSGI server (example with Gunicorn):

   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 "pointsheet:create_app()"
   ```

7. Configure your web server to proxy requests to the WSGI server.

   Example Nginx configuration:

   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/racing-pointsheet/backend/pointsheet/static;
       }
   }
   ```

8. Set up a process manager (e.g., Supervisor) to keep the application running.

   Example Supervisor configuration:

   ```ini
   [program:racing-pointsheet]
   command=/path/to/venv/bin/gunicorn --bind 0.0.0.0:8000 "pointsheet:create_app()"
   directory=/path/to/racing-pointsheet/backend
   user=www-data
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/racing-pointsheet/error.log
   stdout_logfile=/var/log/racing-pointsheet/access.log
   ```

## Docker Deployment

### Prerequisites

- Docker
- Docker Compose

### Deployment Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/racing-pointsheet.git
   cd racing-pointsheet
   ```

2. Create a `.env` file in the root directory with the following variables:

   ```
   APP_ENV=production
   SECRET_KEY=your-secure-secret-key
   ```

3. Build and run the Docker containers:

   ```bash
   docker-compose up -d
   ```

4. Initialize the database:

   ```bash
   docker-compose exec app python -m pointsheet.main migrate
   docker-compose exec app python -m pointsheet.main load-tracks
   ```

5. Access the application at http://localhost:5000

## Troubleshooting

### Common Issues

1. **Database initialization fails**

   - Make sure you have the correct permissions to create and write to the database file
   - Check that the database path is correctly configured

2. **Application fails to start**

   - Check the logs for error messages
   - Verify that all required environment variables are set
   - Ensure that the required ports are available

3. **Static files not loading**
   - Check the web server configuration for the static files path
   - Verify that the static files exist in the specified directory

### Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the project's issue tracker on GitHub
2. Consult the documentation in the `docs` directory
3. Reach out to the project maintainers
