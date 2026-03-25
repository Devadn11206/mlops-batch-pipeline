# Docker Installation Guide - Windows

## Quick Install (Recommended)

### Step 1: Enable WSL2
Run this in PowerShell (as Administrator):

```powershell
wsl --install
# Restart your computer
```

### Step 2: Download Docker Desktop

**Option A: Direct Download (Easiest)**
1. Visit: https://www.docker.com/products/docker-desktop
2. Click **Download for Windows**
3. Double-click the installer
4. Follow the installation wizard
5. **Restart your computer**

**Option B: Command Line (PowerShell as Admin)**
```powershell
# Download
$url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20System%20Installers/Docker%20Desktop%20Installer.exe"
$output = "$env:TEMP\DockerInstaller.exe"
Invoke-WebRequest -Uri $url -OutFile $output

# Install
& $output install

# Restart
Restart-Computer -Force
```

### Step 3: Verify Installation

After restart, open PowerShell and run:

```powershell
docker --version
docker run hello-world
```

If you see version info and "Hello from Docker!", you're ready!

## Build and Run MLOps Pipeline

```powershell
cd c:\Users\ddnan\primetrade.ai\mlops-task

# Build the Docker image
docker build -t mlops-pipeline:v1 .

# Run the container
docker run --rm -v ${PWD}:/app mlops-pipeline:v1
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "docker: command not found" | Docker Desktop not installed or not in PATH |
| "Cannot connect to Docker daemon" | Start Docker Desktop from Start Menu |
| "WSL2 backend is not running" | Run `wsl --install` and restart |
| "Access Denied" | Run PowerShell as Administrator |

## System Requirements

- Windows 10 (Build 18362+) or Windows 11
- Virtualization enabled in BIOS
- 4GB RAM minimum (8GB+ recommended)
- 10GB free disk space

Once Docker is installed, the pipeline will run automatically in a container!
