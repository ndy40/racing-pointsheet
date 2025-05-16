# Deployment Scripts

This directory contains scripts for deploying and managing the application on a server.

## Scripts

- `deploy.sh` - Deploys a specific version of the application
- `rollback.sh` - Rolls back to a previous version of the application

## GitHub Actions Deployment

The project uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/deploy.yml`.

### Required Environment Variables

The following environment variables must be set in GitHub Actions secrets:

- `DEPLOY_DIR` - The directory on the server where deployments will be stored (e.g., `/opt/deployments`)
- `SERVER_HOST` - The hostname or IP address of the server
- `SERVER_USER` - The username to use when connecting to the server
- `SERVER_KEY` - The SSH private key to use when connecting to the server

### Deployment Process

1. The GitHub Actions workflow builds and tests the application
2. It creates a versioned zip file of the application
3. The zip file is uploaded to the server and extracted
4. The `deploy.sh` script is executed on the server to deploy the application

### Rollback Process

If you need to roll back to a previous version:

```bash
ssh user@server "export DEPLOY_DIR=/opt/deployments && /opt/deployments/current/bin/rollback.sh"
```

## Server Setup

Before the first deployment, you need to set up the server:

1. Install required packages:

   ```bash
   sudo apt update
   sudo apt install -y python3-venv python3-pip libgl1 tesseract-ocr unzip
   ```

2. Install Caddy:

   ```bash
   sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
   sudo apt update
   sudo apt install caddy
   ```

3. Create directory structure:

   ```bash
   sudo mkdir -p /opt/deployments
   ```

4. Create Python virtual environment:
   ```bash
   sudo python3 -m venv /opt/deployments/venv
   sudo chown -R $USER:$USER /opt/deployments/venv
   ```

## Manual Deployment

If you need to deploy manually:

1. Build the zip file locally:

   ```bash
   VERSION=$(date +'%Y%m%d%H%M')-manual
   mkdir -p pointsheet-$VERSION
   cp -r backend pointsheet-$VERSION/
   cp -r docker pointsheet-$VERSION/
   cp -r bin pointsheet-$VERSION/
   echo $VERSION > pointsheet-$VERSION/VERSION
   zip -r pointsheet-$VERSION.zip pointsheet-$VERSION
   ```

2. Upload to server:

   ```bash
   scp pointsheet-$VERSION.zip user@server:/opt/deployments/
   ```

3. SSH into server and run:
   ```bash
   cd /opt/deployments
   unzip pointsheet-$VERSION.zip
   export DEPLOY_DIR=/opt/deployments
   ./pointsheet-$VERSION/bin/deploy.sh $VERSION
   ```
