# PowerShell setup script for Week 2 PM Production ML course (Windows)
param(
    [switch]$Local,
    [switch]$Stop
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if ($Stop) {
    docker compose down
    exit 0
}

if ($Local) {
    Write-Host "== Setting up local Python .venv ==" -ForegroundColor Cyan
    if (!(Test-Path ".venv")) { python -m venv .venv }
    & .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python -m fraud_system.data_gen --version v1 --out data/transactions.csv
    python -m fraud_system.train --data data/transactions.csv --params params.yaml
    Write-Host "READY (local venv). Start API: uvicorn fraud_system.serve:app --port 8000" -ForegroundColor Green
    exit 0
}

Write-Host "== Checking Docker ==" -ForegroundColor Cyan
if (!(Get-Command docker -ErrorAction SilentlyContinue)) { Write-Error "Docker not found."; exit 10 }
docker info | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Error "Docker daemon is not running."; exit 11 }

if (!(Test-Path ".fault_state.json")) { "{}" | Set-Content -Encoding Ascii .fault_state.json }

Write-Host "== Starting MLflow (:5000) + Fraud API (:8000) ==" -ForegroundColor Cyan
docker compose up --build -d
if ($LASTEXITCODE -ne 0) { Write-Error "docker compose up failed"; exit 13 }

for ($i = 0; $i -lt 40; $i++) {
    try {
        $r = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2
        if ($r.status -eq "ok") { break }
    } catch {}
    Start-Sleep -Seconds 2
}

powershell -File scripts/smoke.ps1
Write-Host "`nREADY! Console: http://localhost:8000 | MLflow: http://localhost:5000" -ForegroundColor Green
