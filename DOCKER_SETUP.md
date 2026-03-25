# Docker Setup for Windows

## Option 1: Docker Desktop (Recommended)

### Prerequisites
- Windows 10/11 Pro, Enterprise, or Education (or Home with WSL2)
- 4GB RAM minimum (8GB+ recommended)
- Virtualization enabled in BIOS

### Installation Steps

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Choose chip: Intel/AMD or Apple Silicon

2. **Install Docker Desktop**
   ```powershell
   # Run the installer
   .\Docker Desktop Installer.exe install
   
   # Wait for installation to complete
   # Restart your computer when prompted
   ```

3. **Verify Installation**
   ```powershell
   docker --version
   docker run hello-world
   ```

4. **Build and Run the MLOps Pipeline**
   ```powershell
   cd c:\Users\ddnan\primetrade.ai\mlops-task
   
   # Build the image
   docker build -t mlops-pipeline:v1 .
   
   # Run the container
   docker run --rm -v ${PWD}:/app mlops-pipeline:v1
   ```

## Option 2: Manual Setup Script

Run this PowerShell script to automate Docker setup:

```powershell
# Save as: docker-setup.ps1
# Run with: powershell -ExecutionPolicy Bypass -File docker-setup.ps1

$dockerInstallerUrl = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerInstaller.exe"

Write-Host "Downloading Docker Desktop..." -ForegroundColor Green
Invoke-WebRequest -Uri $dockerInstallerUrl -OutFile $installerPath

Write-Host "Installing Docker Desktop..." -ForegroundColor Green
& $installerPath install

Write-Host "Docker installation complete! Restart your computer." -ForegroundColor Yellow
```

## Quick Docker Commands

After installation:

```powershell
# Build image
docker build -t mlops-pipeline:v1 .

# Run container
docker run --rm mlops-pipeline:v1

# Run with output volume
docker run --rm -v ${PWD}/outputs:/app/outputs mlops-pipeline:v1

# List images
docker images

# Remove image
docker rmi mlops-pipeline:v1
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| WSL2 not installed | Run: `wsl --install` and restart |
| Docker daemon not running | Start Docker Desktop from Start Menu |
| Permission denied | Run PowerShell as Administrator |
| Port already in use | Change port: `docker run -p 8080:80 mlops-pipeline:v1` |

## Next Steps

Once Docker is installed:

```powershell
cd c:\Users\ddnan\primetrade.ai\mlops-task
docker build -t mlops-pipeline:v1 .
docker run --rm mlops-pipeline:v1
```

The output will be displayed in your terminal.
