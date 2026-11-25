# PowerShell Setup Script for Windows
Write-Host "=== ClaimFlow AI Windows Setup ===" -ForegroundColor Cyan

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3 is not found in PATH."
    exit 1
}

Write-Host "Python version: $(python --version)"

# Create Virtualenv
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment in .venv..."
    python -m venv .venv
}

# Activate
& .\.venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

Write-Host "Setup finished. Run 'powershell -File scripts/smoke.ps1' to verify." -ForegroundColor Green
