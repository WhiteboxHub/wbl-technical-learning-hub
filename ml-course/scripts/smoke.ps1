# PowerShell smoke test for Fraud Detection MLOps API
param([string]$Base = "http://localhost:8000")

$fail = 0
function Check($Label, $Want, $Method, $Path, $Body = $null) {
    try {
        if ($Body) {
            $resp = Invoke-WebRequest -Uri "$Base$Path" -Method $Method -ContentType "application/json" -Body $Body -UseBasicParsing
        } else {
            $resp = Invoke-WebRequest -Uri "$Base$Path" -Method $Method -UseBasicParsing
        }
        $got = $resp.StatusCode
    } catch {
        $got = [int]$_.Exception.Response.StatusCode
    }
    if ($got -eq $Want) { Write-Host "PASS  $Label ($got)" -ForegroundColor Green }
    else { Write-Host "FAIL  $Label : wanted $Want, got $got" -ForegroundColor Red; $script:fail = 1 }
}

$valid = '{"amount":1250,"hour_of_day":2,"merchant_risk_score":0.85,"tx_velocity_24h":5,"distance_from_home_km":180,"is_international":1,"card_present":0,"account_age_days":45}'
$invalid = '{"amount":-50,"hour_of_day":28}'

Check "health endpoint"       200 "GET"  "/health"
Check "model info"            200 "GET"  "/v1/model-info"
Check "valid prediction"      200 "POST" "/v1/predict" $valid
Check "validation error"      422 "POST" "/v1/predict" $invalid
Check "drift monitor summary" 200 "GET"  "/v1/monitor/drift"
Check "prometheus metrics"    200 "GET"  "/metrics"

if ($fail -ne 0) { exit 1 }
Write-Host "ALL SMOKE CHECKS PASSED" -ForegroundColor Green
