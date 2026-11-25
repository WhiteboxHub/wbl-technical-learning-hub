param([string]$Base = "http://localhost:8000")
Set-Location (Split-Path -Parent $PSScriptRoot)
"{}" | Set-Content -Encoding Ascii .fault_state.json
try { Invoke-RestMethod -Method Post -Uri "$Base/v1/monitor/reset" | Out-Null } catch {}
Write-Host "faults cleared; baseline Fraud Detection API restored" -ForegroundColor Green
