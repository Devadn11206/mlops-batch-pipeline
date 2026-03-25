#!/usr/bin/env powershell
# MLOps Pipeline - Docker Build and Run Script
# Usage: powershell -ExecutionPolicy Bypass -File docker-run.ps1

param(
    [string]$ImageTag = "mlops-pipeline:v1",
    [string]$ContainerName = "mlops-test",
    [switch]$RemoveImage = $false,
    [switch]$Interactive = $false
)

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker is not installed!" -ForegroundColor Red
    Write-Host "Run: powershell -ExecutionPolicy Bypass -File docker-install.ps1" -ForegroundColor Yellow
    exit 1
}

# Verify Docker daemon is running
try {
    docker ps > $null
} catch {
    Write-Host "ERROR: Docker daemon is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MLOps Pipeline - Docker Build & Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Build the image
Write-Host "Building Docker image: $ImageTag" -ForegroundColor Yellow
Write-Host "Location: $scriptDir" -ForegroundColor Gray
Write-Host ""

Push-Location $scriptDir
try {
    docker build -t $ImageTag . --progress=plain
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
    Write-Host "Docker image built successfully!" -ForegroundColor Green
}
finally {
    Pop-Location
}

# Run the container
Write-Host ""
Write-Host "Running Docker container..." -ForegroundColor Yellow
Write-Host ""

if ($Interactive) {
    # Interactive mode with terminal
    docker run --rm -it `
        --name $ContainerName `
        -v "$($scriptDir):/app" `
        -w /app `
        $ImageTag `
        python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
} else {
    # Standard mode
    docker run --rm `
        --name $ContainerName `
        -v "$($scriptDir):/app" `
        -w /app `
        $ImageTag `
        python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
}

$exitCode = $LASTEXITCODE
Write-Host ""

if ($exitCode -eq 0) {
    Write-Host "Pipeline executed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Output files:" -ForegroundColor Yellow
    Write-Host "  - metrics.json" -ForegroundColor Gray
    Write-Host "  - run.log" -ForegroundColor Gray
    
    # Display metrics
    if (Test-Path "$scriptDir\metrics.json") {
        Write-Host ""
        Write-Host "Metrics:" -ForegroundColor Yellow
        Get-Content "$scriptDir\metrics.json" | ConvertFrom-Json | Format-Table -AutoSize
    }
} else {
    Write-Host "ERROR: Pipeline failed with exit code: $exitCode" -ForegroundColor Red
}

# Cleanup option
if ($RemoveImage) {
    Write-Host ""
    Write-Host "Removing image: $ImageTag" -ForegroundColor Yellow
    docker rmi $ImageTag --force > $null
    Write-Host "Image removed" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
exit $exitCode
