# PowerShell Baseline Restorer
Write-Host "Checking ClaimFlow AI baseline health..." -ForegroundColor Cyan
try {
    $res = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "System status: $($res.status) ($($res.service))" -ForegroundColor Green
} catch {
    Write-Host "System is not responding at http://localhost:8000" -ForegroundColor Red
}
