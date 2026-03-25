#!/usr/bin/env powershell
# Docker Desktop Installation Script for Windows
# Usage: powershell -ExecutionPolicy Bypass -File docker-install.ps1

param(
    [switch]$SkipWSL = $false,
    [switch]$AutoRestart = $false
)

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Desktop Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is already installed
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker is already installed!" -ForegroundColor Green
    docker --version
    exit 0
}

# Check Windows version
$osVersion = [System.Environment]::OSVersion.Version
Write-Host "Checking Windows version... ($($osVersion.Major).$($osVersion.Minor))" -ForegroundColor Yellow

if ($osVersion.Major -lt 10) {
    Write-Host "ERROR: Windows 10 or later required!" -ForegroundColor Red
    exit 1
}

# Install WSL2 if needed
if (!$SkipWSL) {
    Write-Host ""
    Write-Host "Installing WSL2..." -ForegroundColor Yellow
    wsl --install
    Write-Host "WSL2 installation initiated. A restart may be required." -ForegroundColor Green
}

# Download Docker Desktop
Write-Host ""
Write-Host "Downloading Docker Desktop..." -ForegroundColor Yellow
$installerUrl = "https://desktop.docker.com/win/stable/Docker%20Desktop%20System%20Installers/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerInstaller.exe"

try {
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -ErrorAction Stop
    Write-Host "✓ Download complete!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to download Docker Desktop" -ForegroundColor Red
    Write-Host "Please download manually from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Install Docker Desktop
Write-Host ""
Write-Host "Installing Docker Desktop..." -ForegroundColor Yellow
$process = Start-Process -FilePath $installerPath -ArgumentList "install" -PassThru -Wait
if ($process.ExitCode -eq 0) {
    Write-Host "✓ Docker Desktop installed successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
    exit 1
}

# Cleanup
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

# Restart prompt
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Your computer must be restarted for Docker to work." -ForegroundColor Yellow

if ($AutoRestart) {
    Write-Host "Restarting in 30 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    Restart-Computer -Force
} else {
    Write-Host "Run this command to restart: restart-computer -Force" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "After restart, verify installation with: docker --version" -ForegroundColor Green
}
