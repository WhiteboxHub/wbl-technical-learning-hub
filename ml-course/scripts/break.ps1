param(
    [Parameter(Mandatory=$true)][ValidateSet("data-drift","concept-drift","bad-schema","latency-spike")][string]$Fault,
    [string]$Base = "http://localhost:8000"
)
Set-Location (Split-Path -Parent $PSScriptRoot)
"{`"fault`":`"$Fault`"}" | Set-Content -Encoding Ascii .fault_state.json
if ($Fault -eq "data-drift") {
    Invoke-RestMethod -Method Post -Uri "$Base/v1/monitor/simulate" -ContentType "application/json" -Body '{"n":120,"data_drift":true,"seed":202}' | Out-Null
} elseif ($Fault -eq "concept-drift") {
    Invoke-RestMethod -Method Post -Uri "$Base/v1/monitor/simulate" -ContentType "application/json" -Body '{"n":120,"data_drift":false,"concept_drift":true,"seed":303}' | Out-Null
}
Write-Host "fault injected: $Fault" -ForegroundColor Yellow
